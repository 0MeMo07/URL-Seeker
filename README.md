# URL Seeker

URL Seeker is an advanced dorking tool that allows you to search for URLs associated with the target domain using various dorks and search engine pages. SQL injection scanning will be added very soon.

![URL Seeker](https://github.com/0MeMo07/URL-Seeker/assets/103096364/6c887dd5-3af5-4e02-a939-24911324dec8)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Introduction

URL Seeker is a Python-based tool designed to simplify the process of discovering URLs associated with a target domain. It leverages enhanced dorking techniques and supports multithreading for faster results.

## Features

- Enhanced dorking with random selection of dorks.
- Output options to save sorted and unsorted URLs to a file.
- User-friendly command-line interface.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/0MeMo07/URL-Seeker.git
    ```

2. Change into the project directory:

    ```bash
    cd URL-Seeker
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use URL Seeker, run the following command:

```bash
python url_seeker.py
```
## Follow the On-Screen Prompts

Follow the on-screen prompts to configure the scan parameters and initiate the scan.

## Options

URL Seeker uses `argparse` for command-line argument parsing. Here are the available options:

- `--sites`: Target Domain (e.g., .com, .org, .net)
- `--dorks`: Number of Dorks (0 for all, default: 0)
- `--threads`: Number of Threads (recommended range: 50-500)
- `--pages`: Pages per Dork (between 25 and 100 at 25 increments)
- `--rdork`: 'Y' if you want the dorks to be randomly selected, 'N' if not
- `--S`: URL or .txt file
- `--O`: Automatically perform SQL injection scanning

**Example usage:**

### Dork Search
```bash
python url_seeker.py --sites .com --dorks 10 --threads 50 --pages 50 --rdork Y
```
### for sql injection scanning automatically after the dork scan is finished --O

```bash
python url_seeker.py --sites .com --dorks 10 --threads 50 --pages 50 --rdork Y --O
```
or

```bash
python url_seeker.py --O
```
### Sql injection scan
If you enter --S url or .txt it scans for sql injection

```bash
python url_seeker.py --S url or .txt
```
## if you want to run it with input:

```bash
python url_seeker.py
```
## Output

After the scan, you can choose from the following output options:

1. Save current sorted URLs to a file.
2. Save current unsorted URLs to a file.
3. Print all unsorted URLs.
4. Print all sorted URLs.
5. SQL injection scanning sorted URLs.
6. SQL injection scanning unsorted URLs.

Choose an option by entering the corresponding number.

## Contributing

Contributions are welcome! If you have any ideas, enhancements, or bug fixes, please submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

Use this tool responsibly and in compliance with applicable laws. The author is not responsible for any misuse or damage caused by this tool.
