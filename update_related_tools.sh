#!/bin/bash

# Fetch the Gist content and save it to a temporary file
curl -s https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/ > temp_gist_content.txt

# Use sed to replace the content between the tags in README.md with the content from the temporary file
sed -i '/<!--START_TAG-->/, /<!--END_TAG-->/!b; /<!--START_TAG-->/!d; r temp_gist_content.txt' README.md

# Clean up the temporary file
rm temp_gist_content.txt
