# QR Code Generator

A simple Python desktop application that creates a QR code from a website URL.

## Features

- Enter a website URL with or without `https://`
- Generate and preview a QR code
- Save the QR code as a PNG or JPEG image
- Basic URL format validation and helpful error messages

## Requirements

- Python 3.10 or newer recommended
- The required Python libraries listed in `requirements.txt`
- Tkinter (included with most standard Windows Python installations)

## How to Use

1. Open the project folder in a terminal.
2. Install the required libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

   If `python` is not recognized on Windows, try:

   ```bash
   py -m pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   python main.py
   ```

   On Windows, you can also try `py main.py`. On macOS or Linux, use `python3 main.py`.

4. When the QR Code Generator window opens, type or paste a website address into the URL field. For example:

   `https://www.wikipedia.org`

5. Click **Generate QR Code**. The QR code will appear in the preview area.
6. Click **Save QR Code**, choose a location and filename, then save the image.
7. Scan the saved QR code with a phone camera or QR scanner to open the website.

## Troubleshooting

- **Missing library error:** Run `python -m pip install -r requirements.txt` again.
- **Python command not found:** Try `py` on Windows or `python3` on macOS/Linux.
- **Tkinter error on Linux:** Install your distribution's Tkinter package (often named `python3-tk`).
- **URL error:** Enter a website address such as `https://www.example.com`. The app checks URL formatting but does not confirm that a website exists.

## Safety Note

The application does not verify whether a website is trustworthy. Only scan or open links you recognize and trust.
