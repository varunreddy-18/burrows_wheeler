# Burrows-Wheeler Compression Pipeline Project

This python project implements the complete Burrows-Wheeler data compression pipeline components adhering strictly to clean object-oriented concepts.

## What is BWT?

The **Burrows-Wheeler Transform (BWT)** breaks text configurations intelligently to formulate clusters of exact sequences and groupings minimizing overall entropy. It fundamentally restructures the original string cyclically, sorting all rotational array outcomes alphanumerically. As a result, identical contextual chars drift toward identical regions continuously, dramatically enhancing compressability without destroying uncompressed structures.

## What is Move-To-Front (MTF)?

**Move-To-Front (MTF)** encoding takes extreme advantage of local repetition formulated perfectly by BWT structures tracking identical consecutive sequences smoothly. It translates common local alphabet elements dynamically to very small values. Whenever character components appear, their index routes map integer streams towards `0`. As redundancy maximizes predictably, bits map overwhelmingly into minimized domains preparing them fully for efficient scaling configurations.

## How to Run the Project
To observe tests end-to-end matching standard testing formats execute perfectly from terminal:

python main.py
