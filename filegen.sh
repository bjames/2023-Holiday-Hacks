#!/bin/bash

# Check if the word list exists
WORD_LIST="/usr/share/dict/words"

for i in {1..333}; do
    # Generate a random filename
    FILE_NAME=$(shuf -n 1 "$WORD_LIST")

    # Create a file with random bytes from /dev/random
    head -c $((RANDOM)) /dev/random > "$FILE_NAME"

    # Compress the file with gzip
    gzip "$FILE_NAME"
done

for i in {1..333}; do
    # Generate a random filename
    FILE_NAME=$(shuf -n 1 "$WORD_LIST")

    # Create a file with an empty image
    cp ~/Documents/not_secret.png "$FILE_NAME"
    # pad with some random bytes to change the size
    head -c $((RANDOM)) /dev/random >> "$FILE_NAME"

    # Compress the file with gzip
    gzip "$FILE_NAME"
done

for i in {1..333}; do
    # Generate a random filename
    FILE_NAME=$(shuf -n 1 "$WORD_LIST")

    fortune | cowsay > "$FILE_NAME"
    for i in $(seq 1 $((RANDOM))); do
        printf "\u00A0" >> "$FILE_NAME"
    done

    # Compress the file with gzip
    gzip "$FILE_NAME"
done
