#!/bin/bash

GIST_CONTENT=$(curl -s https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw)

# Use sed to replace the "Related Tools" section in README.md with the fetched Gist content
sed -i '/^## Related Tools$/,/^##/c\'"$GIST_CONTENT" README.md
