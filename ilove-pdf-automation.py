import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

# File path and settings
file_path = r"C:\Users\Jaya\Documents\Bikram Chatterjee\Python\ilove-pdf-automation\P5 report cards - Ishan-All Term.pdf"

download_dir = r"C:\Users\Jaya\Downloads"

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_dir}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Step 1: Navigate to the website
    driver.get("https://www.ilovepdf.com/ocr-pdf")
    driver.maximize_window()

    # Step 2: Upload the file
    try:
        print("Locating the upload button...")
        upload_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "pickfiles"))
        )
        driver.execute_script(
            "document.querySelector('#uploader input[type=\"file\"]').style.display = 'block';"
        )
        file_input = driver.find_element(By.CSS_SELECTOR, "#uploader input[type='file']")
        file_input.send_keys(file_path)
        print("File uploaded successfully.")
    except Exception as e:
        print(f"Error during file upload: {e}")
        print(driver.page_source)  # For debugging
        driver.quit()
        exit()

    # Step 3: Click 'Apply OCR'
    try:
        print("Clicking 'Apply OCR'...")
        apply_ocr_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "processTask"))
        )
        apply_ocr_button.click()
        print("Clicked 'Apply OCR'.")
    except Exception as e:
        print(f"Error during 'Apply OCR' click: {e}")
        driver.quit()
        exit()

    # Step 4: Wait for the download button and click it
    try:
        print("Waiting for the download button...")
        download_button = WebDriverWait(driver, 180).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".downloader__btn"))
        )
        download_button.click()
        print("Download initiated.")
    except Exception as e:
        print(f"Error during download: {e}")
        driver.quit()
        exit()

    # Wait for the download to complete
    print("Waiting for file to download...")
    downloaded_file = None
    for _ in range(30):  # Check for file for up to 30 seconds
        time.sleep(1)
        files = os.listdir(download_dir)
        for file in files:
            if file.endswith(".pdf") and "ocr" in file.lower():  # Adjust as per naming convention
                downloaded_file = file
                break
        if downloaded_file:
            break

    if downloaded_file:
        print(f"Downloaded file detected: {downloaded_file}")

        # Step 5: Rename the file with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"Processed_File_{timestamp}.pdf"
        os.rename(
            os.path.join(download_dir, downloaded_file),
            os.path.join(download_dir, new_filename),
        )
        print(f"File renamed to: {new_filename}")
    else:
        print("Downloaded file not found within the timeout period.")

finally:
    # Close the browser
    driver.quit()
