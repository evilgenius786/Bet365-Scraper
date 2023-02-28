import json
import os
import time
import traceback
from datetime import datetime
from zipfile import ZipFile

import pytz
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

t = 1
timeout = 10

debug = False

headless = True
images = False
maximize = True

incognito = False
live_urls = ["https://www.bet365.it/#/IP/B1", "https://www.bet365.it/#/IP/B13", "https://www.bet365.it/#/IP/B16",
             "https://www.bet365.it/#/IP4/B17", "https://www.bet365.it/#/IP/B18", "https://www.bet365.it/#/IP/B78",
             "https://www.bet365.it/#/IP/B8", "https://www.bet365.it/#/IP/B83", "https://www.bet365.it/#/IP/B91",
             "https://www.bet365.it/#/IP/B92", "https://www.bet365.it/#/IP/B95"]


# live_urls=["https://www.bet365.it/#/IP/B16", "https://www.bet365.it/#/IP/B8", "https://www.bet365.it/#/IP/B83", "https://www.bet365.it/#/IP/B95"]

def fetchLive(driver):
    for url in live_urls:
        print(f"Fetching live matches from {url}")
        driver.get(url)
        time.sleep(1)
        while True:
            try:
                driver.execute_script("arguments[0].scrollIntoView();",driver.find_element(By.XPATH,'//img[@class="fm-FooterModule_Logo "]'))
                break
            except:
                print("Scrolling down...")
            last_div = driver.find_elements(By.XPATH, '//div[@class="ovm-Competition ovm-Competition-open "]')[-1]
            driver.execute_script("arguments[0].scrollIntoView();", last_div)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = []
        sport_name = soup.find('div', {'class': 'ovm-ClassificationHeader_Text'}).text
        competitions = soup.find_all('div', {'class': 'ovm-Competition ovm-Competition-open'})
        print(f"Found {len(competitions)} competitions in {sport_name}")
        for competition in competitions:
            # driver.execute_script("arguments[0].scrollIntoView();", getElement(driver, '//div[@class="onf-Title "]'))
            # time.sleep(1)
            # soup = BeautifulSoup(driver.page_source, "html.parser")
            header = competition.find('div', {'class': 'ovm-CompetitionHeader_Name'}).text
            matches = competition.find_all('div', {'class': 'ovm-Fixture ovm-Fixture-horizontal'})
            if len(matches) == 0:
                matches = competition.find_all('div', {'class': 'ovm-FixtureDetailsTwoWay'})
            print("Found", len(matches), f"matches in {header} competition")
            for match in matches:
                teams = match.find_all('div', {'class': 'ovm-FixtureDetailsTwoWay_Team'})
                if len(teams) == 0:
                    teams = match.find_all('div', {'class': 'ovm-FixtureDetailsWithIndicators_Team'})
                if len(teams) == 0:
                    teams = match.find_all('div', {'class': 'ovm-FixtureDetailsTwoWay_TeamName'})
                row = {
                    "header": header,
                    "Tipo": "Live",
                    "Sport ": sport_name,
                    "Casa": teams[0].text,
                    "Ospite": teams[1].text,
                }
                rows.append(row)
        # print(json.dumps(rows, indent=4))
        with open(f"./LIVE/{sport_name}.json", 'w') as f:
            json.dump(rows, f, indent=4)


def fetchScheduled(driver):
    print("[+] Fetching scheduled matches")
    driver.get("https://www.bet365.it/#/IP/SCHEDULE")
    time.sleep(1)
    while True:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", getElement(driver, '//img[@class="fm-FooterModule_Logo "]'))
            break
        except:
            print("Scrolling down...")
        last_div = driver.find_elements(By.XPATH, '//div[@class="ovm-Competition ovm-Competition-open "]')[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_div)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = []
    # with open("schedule.txt") as f:
    #     schedule = f.read()
    driver.get('https://www.bet365.it/inplaydiaryapi/schedule?timezone=4&lid=6&zid=0')
    time.sleep(1)
    schedule = driver.page_source
    for div in soup.find_all("div", {"class": "ips-EventRow_HasPreMatchLink"}):
        teams = div.find_all("div", {"class": "ips-EventRow_EventName"})

        row = {
            "Time": div.find("div", {"class": "ips-EventRow_Time"}).text,
            "Sport": div.find("div", {"class": "ips-EventRow_ClassificationName"}).text,
            "Casa": teams[0].text,
        }
        if " v " in row["Casa"]:
            row["Casa"], row["Ospite"] = row["Casa"].split(" v ")
        for line in schedule.split("|EV;CL="):
            if f"NA={row['Casa']}" in line:
                # https://www.bet365.it/#/AC/B92/C20791634/D19/E16298707/F19/P1/
                b = line.split('CI=')[1].split(';')[0]
                c = line.split('C1=')[1].split(';')[0]
                d = line.split('T1=')[1].split(';')[0]
                e = line.split('C2=')[1].split(';')[0]
                f = line.split('T2=')[1].split(';')[0]
                url = f"https://www.bet365.it/#/AC/B{b}/C{c}/D{d}/E{e}/F{f}"
                row["url"] = url
        rows.append(row)
    # print(json.dumps(rows, indent=4))
    print(f"Found {len(rows)} matches")
    with open(f"./scheduled.json", 'w') as f:
        json.dump(rows, f, indent=4)


def ZipAndUpload():
    with ZipFile('bet365.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk('LIVE'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, filePath)
        filePath = os.path.join("scheduled.json")
        zipObj.write(filePath, "PRE MATCH/scheduled.json")
        zipObj.write("lastupdated.txt", "lastupdated.txt")
    print("Zip file created successfully!")
    with open("bet365.zip", mode='rb') as ifile:
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
                   }
        res = requests.post('https://ilmentore.site/LATE/bet365.php',
                            headers=headers,
                            data={"bet365-zip": ifile.read()}
                            )
        print(res.content)


def main():
    logo()

    if not os.path.isdir("LIVE"):
        os.mkdir("LIVE")

    while True:
        print("starting", datetime.now())
        print("Launching chrome...")
        driver = getChromeDriver()
        print("Chrome launched")
        try:
            fetchScheduled(driver)
            fetchLive(driver)
            with open("lastupdated.txt", 'w') as lfile:
                lfile.write(str(datetime.now(pytz.timezone('Europe/Rome'))))
            # time.sleep(10)
        except:
            traceback.print_exc()
        ZipAndUpload()
        print("ending", datetime.now())
        driver.close()


def pprint(msg):
    try:
        print(f"{datetime.now()}".split(".")[0], msg)
    except:
        traceback.print_exc()


def click(driver, xpath, js=False):
    if js:
        driver.execute_script("arguments[0].click();", getElement(driver, xpath))
    else:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


def getElement(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def getElements(driver, xpath):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))


def sendkeys(driver, xpath, keys, js=False):
    if js:
        driver.execute_script(f"arguments[0].value='{keys}';", getElement(driver, xpath))
    else:
        getElement(driver, xpath).send_keys(keys)


def getChromeDriver(proxy=None):
    options = webdriver.ChromeOptions()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--headless=new")
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
    else:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")

        if os.name == 'nt':
            options.add_argument('--user-data-dir=C:/Selenium1/ChromeProfile')
        else:
            options.add_argument('--user-data-dir=./ChromeProfile')
    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")

        options.add_argument("--window-size=1920x1080")
    if maximize:
        # print("Maximizing Chrome ")
        options.add_argument("--start-maximized")
    if proxy:
        # print(f"Adding proxy: {proxy}")
        options.add_argument(f"--proxy-server={proxy}")
    if incognito:
        # print("Going incognito")
        options.add_argument("--incognito")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def getFirefoxDriver():
    options = webdriver.FirefoxOptions()
    if not images:
        # print("Turning off images to save bandwidth")
        options.set_preference("permissions.default.image", 2)
    if incognito:
        # print("Enabling incognito mode")
        options.set_preference("browser.privatebrowsing.autostart", True)
    if headless:
        # print("Hiding Firefox")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
    return webdriver.Firefox(options)


def logo():
    print(rf"""
    __________        __ ________   ________.________
    \______   \ _____/  |\_____  \ /  _____/|   ____/
     |    |  _// __ \   __\_(__  </   __  \ |____  \ 
     |    |   \  ___/|  | /       \  |__\  \/       \
     |______  /\___  >__|/______  /\_____  /______  /
            \/     \/           \/       \/       \/ 
========================================================== 
        Bet365 scraper by @EvilGenius786 (Hassan)
========================================================== 
[+] Automated
[+] Browser based
__________________________________________________________
""")


if __name__ == "__main__":
    main()
