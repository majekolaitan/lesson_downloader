# YouTube Sabbath School Lesson Downloader

## Overview

This script automates the process of searching and downloading Sabbath School lesson videos from YouTube channels. It searches specified YouTube channels for lesson videos based on a predefined query format, allows for optional confirmation before downloading, and saves the videos to a local directory.

## Features

- **Configurable Channel Search:** Define YouTube channels and query formats in `config.py`.
- **First Result Selection:** Automatically selects the first search result if enabled.
- **Confirmation Prompt:** Optionally confirm before adding videos to the download list.
- **Sorting by Published Date:** When `first_result` is disabled, the most recent video is selected.
- **Automatic Downloading:** Retrieves and saves the selected videos to a specified folder.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/sabbath-school-downloader.git
   cd sabbath-school-downloader
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

Modify `config.py` to specify the YouTube channels and query formats.

Example:

```python
CHANNEL_IDS = {
    '3abn': {
        'id': 'UCw_AthKfwqB3XYpboTFZFmg',
        'query_format': '{lesson_title} | Sabbath School Panel by 3ABN - Lesson {lesson_number} Q{quarter} {year}',
        'first_result': True,
        'confirm_download': False
    },
    'itiswritten': {
        'id': 'UCtWyoUrGPAkZgnp2486Ir4w',
        'query_format': 'Sabbath School - {year} Q{quarter} Lesson {lesson_number}: {lesson_title}',
        'first_result': True,
        'confirm_download': True
    }
}
```

### Key Configurations

- `first_result`: If `True`, selects the first search result automatically.
- `confirm_download`: If `True`, asks for confirmation before adding a video.
- `query_format`: Defines the search query format.

## Usage

Run the script to search and download lesson videos:

```sh
python main.py
```

The script will:

1. Search YouTube channels for lesson videos.
2. Display the found video titles.
3. Confirm downloads if `confirm_download` is enabled.
4. Download and save the selected videos.

## Dependencies

- `youtubesearchpython`
- `dateutil`
- `pytube`

## License

This project is open-source and available under the MIT License.
