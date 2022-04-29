# Spot-the-word task for child-directed speech

### What's the spot-the-word task?

In this task, the participant (be it a human or a machine) receives two spoken (or written) stimuli that form a minimal pair of (word, non-word).
For instance: `brick` and `blick`. The participant is then asked to decide which of the two stimuli is the word. If the latter fails, it obtains a score of 0, if it succeeds a score of 1.
The accuracy is computed as the proportion of trials for which the participant succeeded in finding the right word.

When considering a machine participant, one has to extract the probability of the stimulus, which is expected to be higher for the word than for the non-word (how to extract this measure of probability is one of the numerous design choice the programmer is faced with) 

### How non-words are picked up?

WIP

### Getting started

1. [Install](./docs/installation.md)
2. [Create the evaluation set](./docs/build_evaluation.md)
3. [Compute the accuracy](./docs/compute_accuracy.md)