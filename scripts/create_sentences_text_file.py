""""""
from typing import List
import pandas as pd
from pathlib import Path
import pylangacq
from tqdm import tqdm

def create_sentences_file(csvs_directory: str,
                            out_directory: str,
                            adults: List[str]=["Mother", "Father"]) -> None:
    """
    Create a text file containing all utterances\
    produced by all the adults (Mother and Father)\
    from all the six families of the providence corpus.

    Parameters
    ----------
    - csvs_directory : str
        Directory where the csv files of the providence corpus\
        are stored.
    - out_directory : str
        Directory whre the text file produced by this script\
        will be stored.
    - speaker_roles : list
        The speaker roles to be considered as adults
    """
    input_directory = Path(csvs_directory)
    output_directoty = Path(out_directory)
    output_directoty.mkdir(parents=True, exist_ok=True)
    output_file = output_directoty / Path("providence.txt")
    csv_files = list(input_directory.glob("*.csv"))
    total_csv_files = len(csv_files)
    with output_file.open(mode="w", encoding="utf-8") as output_text_file:
        for csv_file in tqdm(input_directory.glob("*.csv"), total=total_csv_files):
            csv = pd.read_csv(csv_file)
            adult_utterances = csv.loc[csv.speaker_role.isin(adults)]
            for utterance in adult_utterances["gloss"] :
                if not isinstance(utterance, str) :
                    continue
                cleaned_utterance = pylangacq.chat._clean_utterance(utterance=utterance)
                if not cleaned_utterance : 
                    continue
                output_text_file.write(f"{cleaned_utterance}\n")

if __name__ == "__main__" :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--csvs_directory",
                        help="The directory containing the csv files.",
                        required=True)
    parser.add_argument("--out_directory_name",
                        help="The directory where outputs will be stored.",
                        required=True)
    args = parser.parse_args()
    create_sentences_file(args.csvs_directory, args.out_directory_name)