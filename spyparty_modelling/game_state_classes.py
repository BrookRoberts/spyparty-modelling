from enum import Enum, auto

from spyparty_modelling.triple_agent_classes import TripleAgentReplay
from spyparty_modelling.utils import only


class LightsStatus(Enum):
    HIGHLIT = auto()
    NEUTRAL_LIT = auto()
    LOWLIT = auto()


class GameStateFeatures:
    def __init__(self, replay: TripleAgentReplay):
        self.time_elapsed = replay.duration
        cast_to_roles = {}
        for event in replay.timeline:
            if "Cast" in event.category:
                cast_to_roles[only(event.cast_name)] = event.role[0]
                if event.event == "spy cast.":
                    self.spy = only(event.cast_name)

        lights_status = {character: LightsStatus.NEUTRAL_LIT for character in cast_to_roles}

        for event in replay.timeline:
            if "SniperLights" in event.category:
                if event.event[-16:] == "less suspicious.":
                    lights_status[only(event.cast_name)] = LightsStatus.LOWLIT
                elif event.event[-18:] == "neutral suspicion.":
                    lights_status[only(event.cast_name)] = LightsStatus.NEUTRAL_LIT
                else:
                    lights_status[only(event.cast_name)] = LightsStatus.HIGHLIT

        self.lights_status = lights_status

    @property
    def number_of_highlights(self):
        return len([character for character, light in self.lights_status if light == LightsStatus.HIGHLIT])

    @property
    def number_of_lowlights(self):
        return len([character for character, light in self.lights_status if light == LightsStatus.LOWLIT])

    @property
    def spy_light_status(self):
        return self.lights_status[self.spy]
