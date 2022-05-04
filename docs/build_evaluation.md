## Download and prepare CHILDES transcriptions

1) Download transcripts from CHILDES:

```bash
python childes/download_transcript.py
```

This will create a file `data/transcripts/sentences.csv` that contain all sentences of American English CHILDES.

2) Split sentences by corpora in `.txt` files and remove unused speakers

```bash
python childes/split_and_prepare.py
```

## Create non-words

The entirety of the codebase to generate non-words come from [here](https://gitlab.cognitive-ml.fr/htiteux/paraphone).
In my fork, I only adapted the code to generate non-words from CHILDES.

```bash
# Initialize workspace
python -m paraphone.cli child_workspace/ init --lang en

# This imports the CHILDES sentences
python -m paraphone.cli child_workspace/ import dataset data/transcripts/text/ --type childes --copy

# Import and build the corpus family
python -m paraphone.cli child_workspace/ import families data/transcripts/text/metadata.csv

# Set-up dictionary
python -m paraphone.cli child_workspace/ dict-setup --celex_path /scratch1/data/raw_data/CELEX2/english/epw/epw.cd

# Tokenization: text files are cleaned, parsed, and that found a match in the dictionaries
# are collected and stored in a csv file
python -m paraphone.cli child_workspace/ tokenize

# Phonemization to IPA using the dictionaries (and phonemizer as a fallback), 
# as well as the folding rules
module load espeak # otherwise you'll have to install espeak on your system
python -m paraphone.cli child_workspace/ phonemize

# Syllabification
python -m paraphone.cli child_workspace/ syllabify

# Syllabic forms are used by wuggy in its lexicon to generate
# real word/ fake word pairs (20 of them for each real word in this case)
python -m paraphone.cli child_workspace/ wuggy --num-candidates 20

# 0) Most of these pairs are trash. We'll need to filter them in some consecutive steps:
# first, init the filtering "subpipeline"
python -m paraphone.cli child_workspace/ filter init

# 1) Removing pairs where the phonetic form of the real word == phonetic form of fake word
python -m paraphone.cli child_workspace/ filter equals

# 2) Removing homophones for real words. Only the most frequent of homophone is kept
python -m paraphone.cli child_workspace/ filter homophones

# 3) Removing wuggy non-words that are homophones to dictionnary words
python -m paraphone.cli child_workspace/ filter wuggy-homophones

# 4) Filtering out pairs that have a phonetic levenshtein edit distance > 2
python -m paraphone.cli child_workspace/ filter levenshtein --threshold 2

# 5) Last filter: it computes ngram scores using the full dataset as a basis,
# then, for each corpus, balances its candidate pairs using Tu Anh's algorithm
python -m paraphone.cli child_workspace/ corpora generate
python -m paraphone.cli child_workspace/ filter ngram --corpus 1 --num-to-keep 10

# Then we can go on with synthesis test (you might want to check 
# that all the phonemes are properly rendered in workspaces/synth/test/
python -m paraphone.cli child_workspace/ synth test

# Then the actual synthesis
python -m paraphone.cli child_workspace/ synth corpora
```

Before synthetizing audio, you should make sure you have a file `credentials.json` in `child_workspace/synth` to be able to authenticate to the Google TTS API (see [documentation](https://cloud.google.com/docs/authentication), [here](https://cloud.google.com/docs/authentication/production) in particular).
You can test if requests to the Google TTS work well by running `python test_synth.py`.