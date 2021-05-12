import argparse
import json
from pathlib import Path

from alive_progress import alive_bar

from spyparty_modelling.game_state_classes import LightsStatus, GameStateFeatures
from spyparty_modelling.triple_agent_classes import TripleAgentReplay, replay_from_replay_file


NUMBER_OF_STATES_IN_DUMMY_TEST_SET = 28198
NUMBER_OF_STATES_IN_TEST_SET = 96604


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_data_folder", type=Path)
    parser.add_argument("model_number", type=int)
    parser.add_argument("--pdb", action="store_true")
    args = parser.parse_args()

    test_data_folder = args.test_data_folder

    chosen_model = {
        0: model_zero,
        1: model_one,
    }[args.model_number]

    predictions = {}

    if args.pdb:
        for triple_agent_data_path in test_data_folder.iterdir():
            triple_agent_data = replay_from_replay_file(triple_agent_data_path)
            predictions[triple_agent_data.uuid] = chosen_model(triple_agent_data)
    else:
        with alive_bar(NUMBER_OF_STATES_IN_TEST_SET) as bar:
            for triple_agent_data_path in test_data_folder.iterdir():
                triple_agent_data = replay_from_replay_file(triple_agent_data_path)
                predictions[triple_agent_data.uuid] = chosen_model(triple_agent_data)
                bar()

    output_file = Path(f"model_{args.model_number}_predictions.json")

    with open(output_file, "w+") as file:
        json.dump(predictions, file)


def model_zero(_: 'TripleAgentReplay'):
    return 0.45


# Need a way to make stats for the entire set?


def model_one(replay: 'TripleAgentReplay'):
    features = GameStateFeatures(replay)

    if features.spy_light_status == LightsStatus.HIGHLIT:
        return 0.3
    elif features.spy_light_status == LightsStatus.NEUTRAL_LIT:
        return 0.45
    elif features.spy_light_status == LightsStatus.LOWLIT:
        return 0.8
    raise ValueError


def reference_strategy(triple_agent_data: 'TripleAgentReplay'):
    # Taken from SPF for SCL season 6
    spy_win_percentages_by_venue = {
        "Aquarium": 0.49,
        "Balcony": 0.52,
        "Ballroom": 0.38,
        "Courtyard": 0.42,
        "Gallery": 0.41,
        "High-Rise": 0.47,
        "Library": 0.39,
        "Moderne": 0.39,
        "Pub": 0.44,
        "Redwoods": 0.52,
        "Teien": 0.48,
        "Terrace": 0.49,
        "Veranda": 0.35,
    }

    return spy_win_percentages_by_venue[triple_agent_data.venue]


if __name__ == "__main__":
    main()
