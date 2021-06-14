import os
import time
import geckodriver_autoinstaller

# from selenium import webdriver
from seleniumwire import webdriver

from .archive import InternetArchive

# Check if the current version of geckodriver exists
geckodriver_autoinstaller.install()


def download(urls, output_folder, email, password):
    driver = webdriver.Firefox()
    driver.maximize_window()

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    try:
        archive = InternetArchive(driver)
        archive.log_in(email, password)
        time.sleep(3)
        archive.download_books(urls, output_folder)
    except Exception as e:
        print(e)
        driver.close()
