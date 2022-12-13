#!/usr/bin/python3
#
#====================================================================================#
# CommonModules.py
# Used as a module for common code.
#====================================================================================#

#------------------------------------------------------------------------------------#
# Modules
#------------------------------------------------------------------------------------#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import sys, os, subprocess, re, logging, json, collections, base64

#------------------------------------------------------------------------------------#
# Variables
#------------------------------------------------------------------------------------#

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)
delay = 10

#------------------------------------------------------------------------------------#
# Loading the appropriate browser
#------------------------------------------------------------------------------------#

def getBrowser(website, **kwargs):
    # Setting variables
    platform = sys.platform
    browser = ""
    browserProfile = webdriver.ChromeOptions()

    # Setting chrome options
    browserProfile.add_argument("--disable-notifications")
    browserProfile.add_argument("--disable-extensions")
    if (kwargs.get("headless") == True):
            browserProfile.add_argument('--headless')

    # Differentiate between different platforms
    if (platform.startswith("win")):
        browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        # Opening browser
        try:
            browser = webdriver.Chrome('chromedriver.exe', options=browserProfile)
        except WebDriverException:
            logger.critical("Could not open webdriver", exc_info=True)

        browser.maximize_window()
    elif (platform.startswith("linux")):
        if (kwargs.get("xvfb") == True):
            FNULL = open(os.devnull, "w")
            subprocess.Popen(["Xvfb", ":1"], stdout=FNULL, stderr=subprocess.STDOUT)
            os.environ["DISPLAY"] = ":1"
        # Opening browser
        try:
            browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver",\
                options=browserProfile)
        except WebDriverException:
            logger.critical("Could not open webdriver", exc_info=True)

    logger.info("Loading " + website)
    browser.get(website)
    return browser