import os, sys
import argparse
from pathlib import Path
import pandas as pd

def main(argv):
    parser = argparse.ArgumentParser(description='Remove Media and Environment speakers and split sentences'
                                                 'per corpora.')
    parser.add_argument('--input', type=str, default='data/transcripts/sentences.csv',
                        help='Path to the .csv file containing sentences.')
    parser.add_argument('--out', type=str, default='data/transcripts/text',
                        help='Path where to store the output .txt files')
    args = parser.parse_args(argv)
    args.out = Path(args.out)
    args.out.mkdir(parents=True, exist_ok=True)

    unused_speakers = ['Media', 'Environment']
    sentences = pd.read_csv(args.input)
    sentences = sentences[~sentences.speaker_role.isin(unused_speakers)]

    for corpora in sentences.corpus_name.unique():
        sub_sentences = sentences[sentences.corpus_name == corpora]
        list_of_sentences = sub_sentences.gloss
        out_path = args.out / (corpora + '_childes.txt')
        list_of_sentences.to_csv(out_path, sep='\n', index=False, header=False)

    metadata_path = args.out / 'metadata.csv'
    file_paths = [args.out.resolve() / (corpora + '_childes.txt') for corpora in sentences.corpus_name.unique()]
    book_ids = [file_path.stem for file_path in file_paths]
    family_ids = [0]*len(file_paths)
    language = ['en']*len(file_paths)
    metadata = pd.DataFrame({'text_path': file_paths, 'family_id': family_ids,
                             'book_id': book_ids, 'language': language})
    metadata.to_csv(metadata_path, sep=',', index=False)


if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)