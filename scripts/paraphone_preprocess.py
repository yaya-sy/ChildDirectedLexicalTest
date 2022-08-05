from typing import Dict
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd

from paraphone.tasks.workspace_init import WorkspaceInitTask
from paraphone.workspace import Workspace
from paraphone.tasks.tokenize import TokenizeEnglishTask
from paraphone.tasks.phonemize import PhonemizeEnglishTask
from paraphone.tasks.dictionaries import CMUENSetupTask, CelexSetupTask, PhonemizerSetupTask

def tokenize(workspace: Path) -> None:
    """Run the paraphone tokenizer"""
    # paraphone requires a workspace
    WorkspaceInitTask(language="en").run(workspace)
    # the paraphon's tokenizer needs these dictionaries in order to only keep some words of the
    # raw text corpora (providence corpus in our case). Maybe this is not adapted in
    # our case, since adult utterances directed to children use very
    # specific vocabulary. Removing these words would result in a vocabulary more closer\
    # to the spot the word task corpus than to the real providence corpus.
    setups = [CMUENSetupTask(),
                CelexSetupTask("/scratch1/data/raw_data/CELEX2/english/epw/epw.cd"),
                PhonemizerSetupTask()]
    for setup in setups :
        setup.run(workspace)
    TokenizeEnglishTask().run(workspace)

def phonemize(workspace: Path) -> None:
    """Run the paraphone phonemizer"""
    PhonemizeEnglishTask().run(workspace)

def get_phonemized_words_and_their_frequencies(workspace) -> Dict[str, int]:
    """Create csv file containing the phonemized words\
        and their frequencies."""
    phonemized_words = pd.read_csv(workspace.phonemized / "all.csv",
                                    sep="\t")
    tokenized_words = pd.read_csv(workspace.tokenized / "all.csv",
                                    sep="\t")
    phonemized_words = dict(zip(phonemized_words["word"], phonemized_words["phones"]))
    tokenized_words = dict(zip(tokenized_words["word"], tokenized_words["count"]))
    phones_frequencies = {phonemized_words[word] : tokenized_words[word]\
                            for word in tokenized_words}

    pd.DataFrame(phones_frequencies.items(),
                columns=['phones', 'frequency']).to_csv(
                    workspace.phonemized / "phones_frequency.csv",
                    index=None)

if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("--workspace",
                        help="The workspace directory",
                        required=True)
    args = parser.parse_args()

    workspace = Workspace(Path(args.workspace))
    tokenize(workspace)
    phonemize(workspace)
    get_phonemized_words_and_their_frequencies(workspace)