#!/bin/bash

GIST_CONTENT=$(curl -s https://gist.githubusercontent.com/yourusername/gistid/raw/)

# Use sed to replace the "Related Tools" section in README.md with the fetched Gist content
sed -i '/^## Related Tools$/,/^##/c\'"$GIST_CONTENT" README.md
