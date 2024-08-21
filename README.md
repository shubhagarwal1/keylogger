# Keylogger Script

This script collects system information, takes a screenshot, and captures a photo from the webcam. It then sends these files as attachments in an email.

## Features

- **System Information**: Gathers details about the computer's system, including IP addresses, processor information, and OS details.
- **Screenshot**: Captures a screenshot of the current screen.
- **Webcam Photo**: Takes a photo using the computer's webcam.
- **Email**: Sends the collected files as attachments in an email.

## Requirements

- Python 3.x
- `Pillow` (for taking screenshots)
- `OpenCV` (for capturing webcam photos)
- `requests` (for fetching public IP address)
- `smtplib` (for sending emails)

## Installation

1. Clone this repository or download the script file.
2. Install the required Python packages:

   ```bash
   pip install pillow opencv-python requests
