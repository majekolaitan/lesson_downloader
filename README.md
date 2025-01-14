# Sabbath School Lesson Downloader

A Python-based script to download Sabbath School lesson videos from popular YouTube channels. This tool automates the retrieval and download of weekly lesson videos, ensuring you're always prepared with the latest content.

---

## Features

- **Automated Weekly Updates**: Detects the current week's lesson based on the date.
- **Customizable Channels**: Supports multiple YouTube channels, including 3ABN and It Is Written.
- **Flexible Video Formats**: Allows users to specify download formats.
- **Efficient Downloads**: Avoids re-downloading previously downloaded videos.
- **Automatic Cleanup**: Deletes outdated lesson files to save storage.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/majekolaitan/lesson_downloader.git
   cd sabbath-school-downloader
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Run the script

```bash
python lesson_downloader/main.py [-f FORMAT_CODE]
```

- **Optional Arguments**:
  - `-f`, `--format`: Specify the download format. Default is `139/140`.

### Example

```bash
python lesson_downloader/main.py -f 22
```

This will download the video in format `22` for the current week's lesson.

---

## Configuration

### Supported Channels

- **3ABN**
  - YouTube Channel ID: `UCw_AthKfwqB3XYpboTFZFmg`
- **It Is Written**
  - YouTube Channel ID: `UCtWyoUrGPAkZgnp2486Ir4w`

You can add more channels by updating the `CHANNEL_IDS` dictionary in `main.py`.

### Lesson Title Logic

The script uses placeholders for lesson titles. Replace `"Placeholder Title"` in the `main()` function with logic to retrieve actual titles.

---

## Dependencies

- [Python 3.8+](https://www.python.org/)
- [requests](https://pypi.org/project/requests/)
- [yt-dlp](https://pypi.org/project/yt-dlp/)
- [youtubesearchpython](https://pypi.org/project/youtubesearchpython/)
- [python-dateutil](https://pypi.org/project/python-dateutil/)

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

Special thanks to the creators and contributors of the following libraries:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [YouTube Search Python](https://github.com/alexmercerind/youtube-search-python)
