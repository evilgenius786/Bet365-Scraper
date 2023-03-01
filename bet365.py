import json
import os
import threading
import time
import traceback
from datetime import datetime
from datetime import timedelta
from zipfile import ZipFile

import pytz
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys, DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

wait_time = 10
# test = True
sports_list = [
    {
        "url": "https://www.bet365.it/#/IP/B16",
        "name": "Baseball",
        "driver": None,
        "match_class": "ovm-FixtureDetailsBaseball_TeamsAndScoresWrapper",
        "team_class": "ovm-FixtureDetailsBaseball_Teams"
    },
    {

        "url": "https://www.bet365.it/#/IP/B1",
        "name": "Calcio",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsAndInfoWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_TeamName"
    },
    {
        "url": "https://www.bet365.it/#/IP/B13",
        "name": "Tennis",
        "driver": None,
        "match_class": "ovm-FixtureDetailsWithIndicators_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsWithIndicators_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B18",
        "name": "Pallacanestro",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B92",
        "name": "Tennistavolo",
        "driver": None,
        "match_class": "ovm-FixtureDetailsWithIndicators_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsWithIndicators_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B91",
        "name": "Pallavolo",
        "driver": None,
        "match_class": "ovm-FixtureDetailsWithIndicators_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsWithIndicators_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B78",
        "name": "Pallamano",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B17",
        "name": "Hockey su ghiaccio",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B83",
        "name": "Calcio a 5",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B8",
        "name": "Rugby",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },
    {
        "url": "https://www.bet365.it/#/IP/B95",
        "name": "Beach Volley",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_Team"
    },

]
t = 1
timeout = 10

debug = True

headless = False
images = False
maximize = True

incognito = False


def fetchSchedule(driver):
    print("Fetching schedule")
    driver.get("https://www.bet365.it/inplaydiaryapi/schedule?timezone=4&lid=6&zid=0")
    schedule = driver.page_source
    dd = ""
    schedule_rows = []
    schedule_anticipate_rows = []
    for line in schedule.split("|"):
        # print(line)
        if line.startswith("CL;IT="):
            dd = line.split("DD=")[1].split(";")[0]
        elif line.startswith("EV;CL="):
            row = {
                "Data": dd,
                "Time": line.split("SM=")[1].split(";")[0],
                "Sport": line.split("CL=")[1].split(";")[0],
                "Casa": line.split("NA=")[1].replace("&amp;", "&").split(";")[0]
            }
            if row['Sport'] == "Tennis":
                continue
            if " v " in row["Casa"]:
                row["Casa"], row["Ospite"] = row["Casa"].split(" v ")
            elif " - " in row["Casa"]:
                row["Casa"], row["Ospite"] = row["Casa"].split(" - ")
            elif " @ " in row["Casa"]:
                row["Casa"], row["Ospite"] = row["Casa"].split(" @ ")
            b = line.split('CI=')[1].split(';')[0]
            c = line.split('C1=')[1].split(';')[0]
            d = line.split('T1=')[1].split(';')[0]
            e = line.split('C2=')[1].split(';')[0]
            f = line.split('T2=')[1].split(';')[0]
            url = f"https://www.bet365.it/#/AC/B{b}/C{c}/D{d}/E{e}/F{f}"
            row["url"] = url
            if row["Data"] == datetime.now().strftime("%d/%m"):
                schedule_rows.append(row)
            schedule_anticipate_rows.append(row)
    with open("schedule.json", "w") as f:
        f.write(json.dumps(schedule_rows, indent=4))
    print(f"Found {len(schedule_rows)} matches in schedule")
    with open("schedule_anticipate.json", "w") as f:
        f.write(json.dumps(schedule_anticipate_rows, indent=4))
    print(f"Found {len(schedule_anticipate_rows)} matches in schedule_anticipate")


def fetchLive(sport):
    print(sport['name'], sport['url'])
    driver = sport["driver"]
    driver.get(sport["url"])
    time.sleep(1)
    if driver.current_url != sport["url"]:
        print(f"Wrong url: {driver.current_url}")
        return
    for i in range(30):
        if "bl-Preloader_Spinner" in driver.page_source:
            print("Waiting for preloader...")
            time.sleep(1)
        else:
            break
    print(f"Fetching live matches from {driver.current_url}")
    while True:
        try:
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.XPATH, '//img[@class="fm-FooterModule_Logo "]'))
            break
        except:
            print("Scrolling down...")
        ld = getElements(driver, '//div[@class="ovm-Competition ovm-Competition-open "]')
        if len(ld) > 0:
            last_div = ld[-1]
            driver.execute_script("arguments[0].scrollIntoView();", last_div)
            time.sleep(1)
        else:
            driver.find_element(By.XPATH, '//*').send_keys(Keys.SPACE)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in range(10):
        rerun = False
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for competition in soup.find_all('div', {'class': 'ovm-Competition ovm-Competition-open'}):
            matches = competition.find_all('div', {'class': sport["match_class"]})
            if len(matches) == 0:
                print(
                    f"Waiting for matches in {competition.find('div', {'class': 'ovm-CompetitionHeader_Name'}).text} {i}")
                time.sleep(1)
                rerun = True
                break
        if not rerun:
            break
    rows = []
    sport_name = soup.find('div', {'class': 'ovm-ClassificationHeader_Text'}).text
    competitions = soup.find_all('div', {'class': 'ovm-Competition ovm-Competition-open'})
    print(f"Found {len(competitions)} competitions in {sport_name}")
    for competition in competitions:
        header = competition.find('div', {'class': 'ovm-CompetitionHeader_Name'}).text
        matches = competition.find_all('div', {'class': sport["match_class"]})
        print(f"Found {len(matches)} matches in {header} competition")
        for match in matches:
            teams = match.find_all('div', {'class': sport["team_class"]})
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
    print(f"Found {len(rows)} matches in {sport_name}")


def main():
    global sports_list
    logo()
    if not os.path.isdir("LIVE"):
        os.mkdir("LIVE")
    scheduled_driver = getChromeDriver(sport="Scheduled")
    for sport in sports_list:
        if sport["driver"] is None:
            if debug:
                sport["driver"] = scheduled_driver
            else:
                sport["driver"] = getChromeDriver(sport=sport["name"])
    while True:
        start = datetime.now()
        try:
            threads = [threading.Thread(target=fetchLive, args=(sport,)) for sport in sports_list]
            # threads = []
            threads.append(threading.Thread(target=fetchSchedule, args=(scheduled_driver,)))
            threads.append(threading.Thread(target=getTennisSchedule, args=(scheduled_driver,)))
            for t in threads:
                t.start()
                t.join()
            pprint("Fetching done, zipping and uploading...")
            while True:
                try:
                    ZipAndUpload()
                    break
                except:
                    print("Error while uploading, retrying...")
                    time.sleep(1)
            pprint("Done!")
        except:
            traceback.print_exc()
        print("Done in", datetime.now() - start, "seconds")


def log_filter(log_):
    return log_["method"] == "Network.responseReceived"


def TennisSchedule(data):
    rows = []
    championship = ""
    for line in data.split("|"):
        if "MG;ID=" in line:
            championship = line.split(";NA=")[1].split(";")[0]
        if ";NA=" in line and ";N2=" in line:
            dt = datetime.strptime(line.split(";BC=")[1].split(";")[0], "%Y%m%d%H%M%S") + timedelta(hours=1)
            row = {
                "Casa": line.split(";NA=")[1].split(";")[0],
                "Ospite": line.split(";N2=")[1].split(";")[0],
                "Sport": "Tennis",
                "Date": dt.strftime("%d/%m/%Y"),
                "Time": dt.strftime("%H:%M"),
                "Championship": championship
            }
            if ";FS=1;" in line:
                row["Live"] = "Yes"
                row["url"] = f"https://www.bet365.it/#/IP/EV" + line.split(";PT=L13")[1].split(";")[0].replace("-",
                                                                                                               "").replace(
                    "20000625_6_0", "C13")
            else:
                row["Live"] = "No"
                row["url"] = f"https://www.bet365.it/#" + line.split(";PD=")[1].split(";")[0].replace("#", "/")
            # print(line)
            rows.append(row)
    print(len(rows))
    with open("tennisBet365scheduled.json", 'w') as f:
        f.write(json.dumps(rows, indent=4))


def getTennisSchedule(driver):
    print("Fetching tennis schedule...")
    driver.get('https://www.bet365.it/#/AC/B13/C1/D50/E2/F163/')
    time.sleep(3)
    logs_raw = driver.get_log("performance")
    # print(f"Found {len(logs_raw)} logs")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        # for log in logs:
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        if "https://www.bet365.it/SportsBook.API/web?lid=6&zid=0&pd=%23AC%23B13%23C1%23D50%23E2%23F163%23&cid=97&cgid=4&ctid=97" == resp_url:
            print(f"Caught {resp_url}")
            data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            TennisSchedule(data["body"])
            break


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


def ZipAndUpload():
    with open("lastupdated.txt", 'w') as lfile:
        lfile.write(str(datetime.now(pytz.timezone('Europe/Rome'))))
    with ZipFile('bet365.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk('LIVE'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, filePath)
        zipObj.write(os.path.join("schedule.json"), "PRE MATCH/schedule.json")
        zipObj.write(os.path.join("schedule_anticipate.json"), "PRE MATCH/schedule_anticipate.json")
        zipObj.write(os.path.join("tennisBet365scheduled.json"), "PRE MATCH/tennisBet365scheduled.json")
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


def getChromeDriver(proxy=None, sport=""):
    options = webdriver.ChromeOptions()
    capabilities = DesiredCapabilities.CHROME
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    else:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f'--user-data-dir=C:/Selenium/{sport}')

    if not images:
        # print("Turning off images to save bandwidth")
        options.add_argument("--blink-settings=imagesEnabled=false")
    if headless:
        # print("Going headless")
        options.add_argument("--headless")
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
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=options,
                            desired_capabilities=capabilities)


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


if __name__ == "__main__":
    main()
