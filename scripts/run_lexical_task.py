from typing import Dict
from argparse import ArgumentParser
import pandas as pd
from paraphone.ngrams_tools import NGramComputer
from paraphone.utils import consecutive_pairs

def wuggy_pairs_accuracy(fake_real_words_df,
                            ngram_computer: NGramComputer,
                            ngram_pribabilities: Dict[str, float]) -> float:
    good_classifications = 0
    total_pairs = 0
    for real_word, fake_word in zip(fake_real_words_df["word_pho"],
                                    fake_real_words_df["fake_word_pho"]) :
        total_pairs += 1
        real_word_ngrams = list(consecutive_pairs(real_word.split(" ")))
        fake_word_ngrams = list(consecutive_pairs(fake_word.split(" ")))
        real_word_logprob = ngram_computer.to_ngram_logprob(real_word_ngrams, ngram_pribabilities)
        fake_word_logprob = ngram_computer.to_ngram_logprob(fake_word_ngrams, ngram_pribabilities)
        good_classifications += int(real_word_logprob > fake_word_logprob)
    return good_classifications / total_pairs

def main(args) -> None:
    """Run the test on tasks and print the accuracy"""

    loaded_phones_frequency = pd.read_csv(args.phones_frequency_csv)
    phones_frequency_dict = {tuple(phones.split(" ")) : freq for phones, freq\
                                in zip(loaded_phones_frequency["phones"],
                                        loaded_phones_frequency["frequency"])}

    ngram_model = NGramComputer(phones_frequency_dict)
    ngram_probabilities = ngram_model.bigrams(bounded=True)
    wuggy_pairs = pd.read_csv(args.wuggy_pairs_csv,
                                index_col=False,
                                sep="\t")
    accuracy = wuggy_pairs_accuracy(wuggy_pairs,
                        ngram_model,
                        ngram_probabilities)
                        
    print(accuracy)

if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("--phones_frequency_csv",
                        type=str,
                        help="The csv containing phonemized words\
                            and their frequencies.",
                        required=True)
    parser.add_argument("--wuggy_pairs_csv",
                        type=str,
                        help="The wuggy pairs csv on which the ngram\
                            model will be tested.",
                        required=True)
    
    main(parser.parse_args())

