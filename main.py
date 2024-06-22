from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

import os
import time
import glob
from urllib import parse

def get_browser(download_dir):
    download_dir = os.path.abspath(download_dir)
    edge_options = webdriver.EdgeOptions()
    edge_options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    edge_options.add_argument("--log-level=3")    
    driver_path = r'./msedgedriver.exe'
    service = Service(driver_path)
    browser = webdriver.Edge(service=service, options=edge_options)
    browser.minimize_window()
    return browser

def read_file(file):
    with open(file, 'r') as f:
        text = f.read()
    return text

def get_files(path):
    files = glob.glob(f'{path}/*')
    for file in files:
        if os.path.isfile:
            yield file

def encode_text(file):
    text = read_file(file)
    uri_encoded_text = parse.quote_plus(text)
    return uri_encoded_text

def main():
    with (get_browser(OUTPUT_DIR))as browser:
        for file in get_files(CODE_DIR):
            print(f"{'\033[32m'}Processing '{file}'{'\033[0m'}")
            encoded_text = encode_text(file)
            url = "https://carbon.now.sh?code=" + encoded_text
            browser.get(url)

            time.sleep(2.5)
            browser.find_element(By.XPATH, "//button[@id='export-menu']").click()
            browser.find_element(By.XPATH, "//input[@title='filename']").send_keys(file.split('.')[0].split('\\')[-1])
            browser.find_element(By.XPATH, "//button[contains(text(), '4x')]").click()
            browser.find_element(By.XPATH, f"//button[@id='export-{OUTPUT_DIR}']").click()
            time.sleep(2.5)
        
        time.sleep(2.5)
        print(f"{'\033[32m'}Finished.{'\033[0m'}")   

if __name__ == '__main__':
    CODE_DIR = 'code'
    OUTPUT_DIR = 'svg' # 'png' or 'svg'
    if os.path.isdir(CODE_DIR):
        main()
    else:
        os.mkdir(CODE_DIR)
        msg = f"{'\033[33m'}'{CODE_DIR}' is created please put files in '{os.path.abspath(CODE_DIR)}'{'\033[0m'}"
        print(msg)
