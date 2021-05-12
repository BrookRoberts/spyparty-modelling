import json
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TripleAgentTimelineEvent:
    action_test: str
    actor: str
    books: List  # Can be length 2 with e.g. "Blue" "Yellow" "Green"
    cast_name: List
    category: List
    elapsed_time: float
    event: str
    mission: str
    role: List
    time: float

    @staticmethod
    def null_event():
        return TripleAgentTimelineEvent("", "", [], [], [], 0.0, "NULL EVENT", "", [], 0.0)


@dataclass
class TripleAgentReplay:
    event: Optional[str]
    game_type: str  # e.g. a2/4, k2, p2/3
    completed_missions: List
    division: Optional[str]
    duration: int
    guest_count: Optional[int]
    picked_missions: List
    selected_missions: List
    sniper: str
    sniper_username: str  # This is the one that might be s85845847/steam
    spy: str
    spy_username: str  # This is the one that might s338738743874/steam
    start_clock_seconds: Optional[int]
    start_time: str
    timeline: List[TripleAgentTimelineEvent]  # Can pass in the json and __post_init__ will convert to this
    uuid: str
    venue: str
    week: Optional[int]
    win_type: List  # Could be tuple, but list to match triple agent exactly
    winner: str

    def __post_init__(self):
        self.timeline = [TripleAgentTimelineEvent(**event) for event in self.timeline]


def replay_from_replay_file(game_file):
    with open(game_file) as f:
        data = json.load(f)
    del data["py/object"]
    replay = TripleAgentReplay(**data)
    return replay
