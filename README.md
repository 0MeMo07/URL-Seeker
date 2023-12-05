# URL-Seeker
URL Seeker is advanced docking tool that allows you to search for URLs associated with the target domain using various dors and search engine pages. Once found, SQL injection scanning will be added very soon.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Options](#options)
- [Output](#output)
- [Dependencies](#dependencies)
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
Follow the on-screen prompts to configure the scan parameters and initiate the scan.

## Options

- **Target Domain:** Specify the target domain (e.g., .com, .org, .net).
- **Number of Dorks:** Randomly select the number of dorks to use (enter 0 for all available dorks).
- **Number of Threads:** Enter the number of threads (recommended range: 50-500).
- **Pages per Dork:** Enter the number of search engine pages to crawl per dork (between 25 and 100 at 25 increments).

## Output

After the scan, you can choose from the following output options:

1. Save current sorted URLs to a file.
2. Save current unsorted URLs to a file.
3. Print all unsorted URLs.
4. Print all sorted URLs.

## Dependencies

- asyncio
- requests
- bs4
- tqdm
- aiohttp
- pystyle

## Contributing

Contributions are welcome! If you have any ideas, enhancements, or bug fixes, please submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

Use this tool responsibly and in compliance with applicable laws. The author is not responsible for any misuse or damage caused by this tool.
