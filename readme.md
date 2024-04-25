# One File Code Combiner for AI Assistance

This Python script combines all supported code files (`.py`, `.c`, `.cpp`, `.h`, `.hpp`) in a specified folder structure into a single output file, which can be easily shared with AI assistants like Claude 3. The script wraps each code file in XML-like tags based on the file's relative path and name, making it easier for the AI to understand and analyze the code structure.

## Features

- Combines code files into a single output file for use with AI assistants
- Supports Python, C, C++, and header files
- Wraps each code file in XML-like tags for easy code structure identification
- Calculates token count and line count of the output file
- Customizable output folder and filename
- Option to skip specific folder names during processing
- Uses pipenv for virtual environment management

## Requirements

- Python 3.6+


## Setup

1. Clone the repository:

```
git clone https://github.com/yourusername/onefile.git
cd onefile
```

2. Install pipenv if you haven't already:

```
pip install pipenv
```

3. Create a virtual environment and install the required dependencies:

```
pipenv install
```

## Quick Start

To quickly combine your code files, run the following command:

```
pipenv run python onefile.py --combine --folder_path /path/to/your/code/folder
```

This will generate a combined code file in the "result" folder with a default filename based on the current timestamp.

## Usage

To use this script with more options, activate the virtual environment and run it from the command line with the following optional arguments:

```
pipenv run python ./onefile/onefile.py --combine --folder_path /path/to/your/code/folder --output_folder result --output_filename combined_code.py --skip_foldername skip_folder1 skip_folder2
```

- `--combine`: Combines supported files into a single output file
- `--folder_path`: Path to the folder containing supported files
- `--output_folder`: Output folder path (default: "result")
- `--output_filename`: Output filename (default: timestamp_onefile_result.py)
- `--skip_foldername`: List of folder names to skip during processing

You can also calculate the token count and line count of a single file:

```
pipenv run python ./onefile/onefile.py --calc_token --file_path /path/to/your/file.py
```

- `--calc_token`: Calculates file token count
- `--file_path`: File path for token calculation

## Example

Given the following folder structure:

```
project/
├── main.py
├── utils/
│   ├── helper.py
│   └── constants.py
└── lib/
    ├── core.cpp
    └── header.h
```

Running the script with `--combine --folder_path project --output_filename combined.py` will generate a `combined.py` file in the "result" folder with the following content:

```xml
<main.py>
# main.py content
</main.py>

<utils|helper.py>
# helper.py content
</utils|helper.py>

<utils|constants.py>
# constants.py content
</utils|constants.py>

<lib|core.cpp>
// core.cpp content
</lib|core.cpp>

<lib|header.h>
// header.h content
</lib|header.h>
```

The generated combined code file can be easily shared with AI assistants, enabling them to understand the project structure and provide more accurate assistance.
