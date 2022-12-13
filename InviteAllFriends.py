#------------------------------------------------------------------------------------#
# Modules
#------------------------------------------------------------------------------------#

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,\
    UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from word2number import w2n
import time, sys, re, os, threading, logging, argparse, datetime, base64
from selenium.webdriver.common.action_chains import ActionChains
sys.path.append(os.getcwd() + "/PythonModules/")
import commonModules

#------------------------------------------------------------------------------------#
# Variables
#------------------------------------------------------------------------------------#

parser = argparse.ArgumentParser()
parser.add_argument("--test", "-t", action="store_true", default=False, help="Does not message people when starting \
    lifts")
args = parser.parse_args()
logger = None

#------------------------------------------------------------------------------------#
# Waiting for an element and then returning that element
#------------------------------------------------------------------------------------#

def WaitFor(browser, element, delay=10):
    flag = False
    while True:
        try:
            WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.XPATH, element)))
            break
        except Exception:
            if (not flag):
                flag = True
                try:
                    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH,\
                        '//*[contains(text(), "This site can") and contains(text(), "be reached")]')))
                    logger.info("There is not an internet connection, refreshing...")
                    browser.refresh()
                except Exception:
                    logger.critical("Could not find " + element, exc_info=True)
                    raise Exception()
            else:
                logger.critical("Could not find " + element, exc_info=True)
                raise Exception()
    return browser.find_element_by_xpath(element)

#------------------------------------------------------------------------------------#
# JS version of clicking an element
#------------------------------------------------------------------------------------#

def ClickElem(browser, xpath, delay=10):
        browser.execute_script("arguments[0].click();", WaitFor(browser, xpath, delay=delay))

#------------------------------------------------------------------------------------#
# First initial steps
#------------------------------------------------------------------------------------#

def Init():
    global logger
    logformatter = logging.Formatter("%(asctime)s-%(levelname)-8s-[%(filename)s:%(lineno)d] %(message)s",\
        datefmt="%Y/%m/%d-%H:%M:%S")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.getLogger(__name__)
    fileHandler = logging.FileHandler("{0}/{1}.log".format(".", "InviteAllFriends"), mode="w")
    fileHandler.setFormatter(logformatter)
    logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logformatter)
    logger.addHandler(consoleHandler)

    # Opening the browser
    logger.info("Opening browser")
    browser = commonModules.getBrowser("https://www.google.com/", headless=False)
    logger.info("Loaded Google, loading Facebook")

    Main(browser)

#------------------------------------------------------------------------------------#
# Loading the browser and kicking off script
#------------------------------------------------------------------------------------#

def Main(browser):
    # Log in details
    EMAIL = "YnJ1bnllZWJAZ21haWwuY29t"
    PASSWORD = "C4llywasmyf!rstd0g"

    # Getting log in page
    browser.get("https://www.facebook.com/")
    logger.info("Loaded Facebook")

    ClickElem(browser, '//button[@data-testid="cookie-policy-dialog-accept-button"]')

    WaitFor(browser, '//input[@name="email"]').send_keys(base64.b64decode(EMAIL).decode())
    WaitFor(browser, '//input[@name="pass"]').send_keys(PASSWORD + "\n")
    logger.info("Logging in")

    logging.info("Waiting on 2 factor authentication")
    WaitFor(browser, '//input[@placeholder="Login code"]', delay=3)
    input("Waiting for confirmation, hit enter once logged in\n")

    logging.info("Refreshing the page")
    browser.refresh()

    WaitFor(browser, '//input[@type="search"]')
    logger.info("Loading facebook page")

    browser.get("https://www.facebook.com/groups/1062589187555388")

    ClickElem(browser, '//div[@aria-label="Invite" and @role="button"]')

    logging.info("Selecting friends")

    WaitFor(browser, '//div[@aria-checked="false"]')

    elems = browser.find_elements_by_xpath('//div[@aria-checked="false"]')
    lastCount = 0
    currentCount = -1

    while (lastCount != currentCount):
        browser.execute_script("return arguments[0].scrollIntoView();", elems[len(elems) - 1])
        time.sleep(1.5)
        lastCount = len(elems)
        elems = browser.find_elements_by_xpath('//div[@aria-checked="false"]')
        currentCount = len(elems)

    for elem in elems:
        browser.execute_script("arguments[0].click();", elem)

    logging.info("Selected all available friends")
    input("Manually press invite button\n")

Init()
