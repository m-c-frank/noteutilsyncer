# noteutilsyncer

`noteutilsyncer` is a utility designed to centralize and synchronize the "Related Tools" section across the Note Utilities Ecosystem. By maintaining a single source of truth for all project READMEs, it ensures consistency and ease of management across the ecosystem. Whenever a new tool is added or an existing one is updated, `noteutilsyncer` automates the process of updating the "Related Tools" section in all associated repositories.

## Features

- Central repository for all READMEs in the Note Utilities Ecosystem.
- Automated synchronization of the "Related Tools" section across repositories.
- Streamlined process for adding or updating tools in the ecosystem.
- Python-based script for easy integration and modification.

## Directory Structure

```bash
.
├── LICENCE.md                # License for noteutilsyncer
├── README.md                 # Documentation for noteutilsyncer
├── readme/                   # Directory containing all tool READMEs in the ecosystem
│   ├── conceptsplitter.md
│   ├── contenttree.md
│   └── textdownloader.md
├── repo                      # (Description based on its purpose)
├── requirements.txt          # Python dependencies for the project
├── src/                      # Source code directory
│   ├── __init__.py
│   └── sync.py               # Python script to synchronize the "Related Tools" section
└── tests/                    # Tests for the project
    └── test_sync.py
```

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/m-c-frank/noteutilsyncer
    cd noteutilsyncer
    ```

2. Add or update the README of a tool in the `readmes/` directory.

## Usage

1. Run the `sync.py` script:

   ```bash
   python sync.py
   ```

2. The script will extract the "Related Tools" section from each README, and then update the respective repositories, creating pull requests for the changes.

## Related Tools

<!--START_TAG-->
**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.

- **noteutilsyncer**: Centralizes and synchronizes the "Related Tools" section across the ecosystem.
- **[workflowlibrary](https://github.com/m-c-frank/workflowlibrary)**: A curated catalog of GitHub Actions workflows.
- **[conceptsplitter](https://github.com/m-c-frank/conceptsplitter)**: Extract atomic concepts from a given text using the OpenAI API.
- **[textdownloader](https://github.com/m-c-frank/textdownloader)**: A browser extension to automatically generate text dumps for processing.
<!--END_TAG-->

## Contributing

Contributions to the `noteutilsyncer` project or the Note Utilities Ecosystem are welcome. If you have ideas for improvements or new features, please feel free to submit issues, suggestions, or pull requests in this repository or contact me!

## License

The `noteutilsyncer` project is open-source and available under the [GOS License](LICENSE.md).

## Credits

The `noteutilsyncer` project is developed and maintained by [Martin Christoph Frank](https://github.com/m-c-frank). If you have any questions or need assistance, please contact [martin7.frank7@gmail.com](martin7.frank7@gmail.com).
