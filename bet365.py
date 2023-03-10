import json
import os
import random
import time
import traceback
from datetime import datetime
from datetime import timedelta
from zipfile import ZipFile

import pyperclip
import pytz
import requests
from bs4 import BeautifulSoup
from pywinauto import mouse, keyboard
from selenium import webdriver
from selenium.webdriver import Keys, DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

wait_time = 3
# test = True

schedule_list = [
    {
        "Sport": "PALLAVOLO",
        "Links": [
            "https://www.bet365.it/#/AC/B91/C20873403/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873388/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873264/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872263/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872986/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872575/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873429/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873575/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873584/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20864077/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872354/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873428/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20870924/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20865432/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20842029/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873432/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873599/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873072/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873259/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20846471/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20840718/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873001/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873421/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873475/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872910/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20872276/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873469/D48/E1/F4/",
            "https://www.bet365.it/#/AC/B91/C20873420/D48/E1/F4/"
        ]
    },
    {
        "Sport": "TENNIS",
        "Links": [
            "https://www.bet365.it/#/AC/B13/C1/D50/E2/F163/"
        ]
    },
    {
        "Sport": "CALCIO",
        "Links": [
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J99/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J6/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J1/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J8/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J7/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J15/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J9/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J17/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J2/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J13/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J18/I1/Q1/F^12/",
            "https://www.bet365.it/#/AC/B1/C1/D1002/G40/J12/I1/Q1/F^12/"
        ]
    },
    {
        "Sport": "PALLACANESTRO",
        "Links": [
            "https://www.bet365.it/#/AC/B18/C20604387/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20849562/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20872155/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20873262/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20870840/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20868136/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20860830/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20840920/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20870875/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20871554/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20870847/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20868925/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20867997/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20870648/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20872614/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20873162/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20872845/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20873373/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20870891/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20872938/D48/E1453/F10/",
            "https://www.bet365.it/#/AC/B18/C20571937/D48/E1453/F10/"
        ]
    },

    {
        "Sport": "PALLAMANO",
        "Links": [
            "https://www.bet365.it/#/AC/B78/C20872852/D48/E1/F10/",
            "https://www.bet365.it/#/AC/B78/C20864031/D48/E1/F10/",
        ]
    },
    {
        "Sport": "HOCKEY SU GHIACCIO",
        "Links": [
            "https://www.bet365.it/#/AC/B17/C20836572/D48/E972/F10/",
            "https://www.bet365.it/#/AC/B17/C20867882/D48/E972/F10/"
        ]
    },
    {
        "Sport": "TENNISTAVOLO",
        "Links": [
            "https://www.bet365.it/#/AC/B92/C1/D50/E2/F163/",
            "https://www.bet365.it/#/AC/B92/C20694992/D48/E920000/F10/",
            "https://www.bet365.it/#/AC/B92/C20791634/D48/E920000/F10/"
        ]
    },
    {
        "Sport": "PALLANUOTO",
        "Links": [
            "https://www.bet365.it/#/AC/B110/C20809027/D48/E1100003/F10/",
            "https://www.bet365.it/#/AC/B110/C20811896/D48/E1100003/F10/",
            "https://www.bet365.it/#/AC/B110/C20843366/D48/E1100003/F10/"
        ]
    }
]

sports_list = [
    {
        "url": "https://www.bet365.it/#/IP/B16",
        "name": "Baseball",
        "driver": None,
        "match_class": "ovm-FixtureDetailsBaseball_TeamsAndScoresWrapper",
        "team_class": "ovm-FixtureDetailsBaseball_Teams"
    },
    {

        "url": "https://www.bet365.it/#/IP/B110",
        "name": "Pallanuoto",
        "driver": None,
        "match_class": "ovm-FixtureDetailsTwoWay_TeamsWrapper",
        "team_class": "ovm-FixtureDetailsTwoWay_TeamName"
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
random.shuffle(sports_list)
# schedule_list = []

t = 1
timeout = 10

debug = True

headless = False
images = False
maximize = True

incognito = False


def get(driver, url):
    driver.get(url)
    return
    mouse.click(coords=(290, 60))
    time.sleep(0.5)
    keyboard.send_keys("^a")
    time.sleep(0.5)
    pyperclip.copy(url)
    time.sleep(0.5)
    keyboard.send_keys("^v")
    time.sleep(1)
    keyboard.send_keys('{ENTER}')


def openNewTab(driver):
    # mouse.move()
    mouse.click(coords=(340, 10))
    driver.close()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])


def fetchLive(sport):
    print(sport['name'], sport['url'])
    driver = sport["driver"]
    get(driver, sport['url'])
    time.sleep(wait_time)
    if driver.current_url != sport["url"]:
        print(f"Wrong url: {driver.current_url}")
        return
    for i in range(10):
        try:
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.XPATH, '//div[@class="flm-FooterLegacyModule_Wrapper "]'))
        except:
            pass
        if i == 3:
            print("Switching to new tab...")
            # openNewTab(driver)
            get(driver, sport['url'])
        if "bl-Preloader_Spinner" in driver.page_source:
            print("Waiting for preloader...")
            time.sleep(1)
        else:
            break
    print(f"Fetching live matches from {driver.current_url}")
    for i in range(3):
        try:
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element(By.XPATH, '//div[@class="flm-FooterLegacyModule_Wrapper "]'))
            break
        except:
            traceback.print_exc()
            print("Scrolling down...")
        ld = getElements(driver, '//div[@class="ovm-Competition ovm-Competition-open "]')
        if len(ld) > 0:
            last_div = ld[-1]
            driver.execute_script("arguments[0].scrollIntoView();", last_div)
            time.sleep(1)
        else:
            driver.find_element(By.XPATH, '//*').send_keys(Keys.SPACE)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for i in range(10):
        rerun = False
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for competition in soup.find_all('div', {'class': 'ovm-Competition ovm-Competition-open'}):
            if competition.find('div', {'class': 'ovm-Link_Text'}):
                continue
            try:
                matches = competition.find_all('div', {'class': sport["match_class"]})
                if len(matches) == 0:
                    print(
                        f"Waiting for matches in {competition.find('div', {'class': 'ovm-CompetitionHeader_Name'}).text} {i}")
                    time.sleep(1)
                    rerun = True
                    break
            except:
                traceback.print_exc()
                # print("Waiting for matches...")
                # time.sleep(1)
                # rerun = False
                # break
        if not rerun:
            break
    rows = []
    sport_name = soup.find('div', {'class': 'ovm-ClassificationHeader_Text'}).text
    competitions = soup.find_all('div', {'class': 'ovm-Competition ovm-Competition-open'})
    print(f"Found {len(competitions)} competitions in {sport_name}")
    for competition in competitions:
        try:
            if competition.find('div', {'class': 'ovm-Link_Text'}):
                for comp in competition.find_all('div', {'class': 'ovm-Link_Text'}):
                    team = comp.text.split(" v ")
                    row = {
                        "header": competition.find('div', {'class': 'ovm-CompetitionHeader_Name'}).text,
                        "Tipo": "Live",
                        "Sport ": sport_name,
                        "Casa": team[0],
                    }
                    if len(team) > 1:
                        row["Ospite"] = team[1]
                    rows.append(row)
                continue
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
        except:
            traceback.print_exc()
    # print(json.dumps(rows, indent=4))
    with open(f"./LIVE/{sport_name}.json", 'w') as f:
        json.dump(rows, f, indent=4)
    print(f"Found {len(rows)} matches in {sport_name}")


def main():
    today = datetime.now().strftime("%d-%m-%Y")
    logo()
    if not os.path.isdir("LIVE"):
        os.mkdir("LIVE")
    if not os.path.isdir("SCHEDULE"):
        os.mkdir("SCHEDULE")
    with open("lastupdated-schedule.txt", 'w') as lfile:
        lfile.write("")
    with open("lastupdated-live.txt", 'w') as lfile:
        lfile.write("")
    while True:
        start = datetime.now()
        if datetime.now().strftime("%d-%m-%Y") != today:
            today = datetime.now().strftime("%d-%m-%Y")
            with open("schedule_anticipate.json", "w") as f:
                json.dump([], f, indent=4)
            with open("schedule.json", "w") as f:
                json.dump([], f, indent=4)
        driver = getChromeDriver(sport="Scheduled")
        # get('http://lumtest.com/myip.json')
        # print(driver.find_element(By.XPATH, '//*').text)
        try:
            # for sport in sports_list:
            #     sport["driver"] = driver
            # for sport in sports_list:
            #     try:
            #         fetchLive(sport)
            #     except:
            #         traceback.print_exc()
            #         print(f"Error on sport {sport}")
            # with open("lastupdated-live.txt", 'a') as lfile:
            #     lfile.write(f"{datetime.now(pytz.timezone('Europe/Rome'))}\n")
            # ZipAndUpload()
            # continue
            # input("done")
            for schedule in schedule_list:
                try:
                    n = 10
                    links_list = [schedule["Links"][i:i + n] for i in range(0, len(schedule["Links"]), n)]
                    for links in links_list:
                        random.shuffle(sports_list)
                        random.shuffle(links)

                        for url in links:
                            try:
                                GetNewSchedule(driver, url, schedule["Sport"])
                            except:
                                traceback.print_exc()
                        fetchSchedule(driver)
                        for sport in sports_list:
                            sport["driver"] = driver
                        for sport in sports_list:
                            try:
                                fetchLive(sport)
                            except:
                                traceback.print_exc()
                                print(f"Error on sport {sport}")
                        with open("lastupdated-live.txt", 'a') as lfile:
                            lfile.write(f"{datetime.now(pytz.timezone('Europe/Rome'))}\n")
                        # ZipAndUpload()
                        with open("lastupdated-schedule.txt", 'a') as lfile:
                            lfile.write(f"{schedule['Sport']} {datetime.now(pytz.timezone('Europe/Rome'))}\n")
                        ZipAndUpload()
                except:
                    traceback.print_exc()
                    print("Error while fetching live matches, retrying...")
                    time.sleep(1)
            pprint("Fetching done, zipping and uploading...")
            while True:
                try:
                    ZipAndUpload()
                    break
                except:
                    traceback.print_exc()
                    print("Error while uploading, retrying...")
                    time.sleep(1)
            pprint("Done!")
        except:
            traceback.print_exc()
        try:
            driver.close()
            driver.quit()
        except:
            pass
        print("Done in", datetime.now() - start, "seconds")


def GetNewSchedule(driver, url, sportName, num_try=3):
    print(f"Fetching {sportName} schedule {url}")
    get(driver, url)
    time.sleep(wait_time)
    for i in range(10):
        if i == 8:
            print("Switching to new tab...")
            get(driver, url)
        if "bl-Preloader_Spinner" in driver.page_source:
            print("Waiting for preloader...")
            time.sleep(1)
        else:
            break
    for i in range(3):
        try:
            driver.find_element(By.XPATH, '//div[@class="sph-BettingSuspendedScreen_Message "]')
            print("Suspended")
            return
        except:
            pass
            # traceback.print_exc()
        time.sleep(1)
    logs_raw = driver.get_log("performance")
    # print(f"Found {len(logs_raw)} logs")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        # for log in logs:
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        # print(resp_url)
        if url.split("/#")[1].replace("/", "%23") in resp_url or "upcomingmatches" in resp_url:
            time.sleep(1)
            print(f"Caught {resp_url}")
            data = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            if "NA" in data["body"]:
                ParseScheduleData(data["body"], sportName, driver)
                return
            else:
                if num_try > 0:
                    print(f"Retrying {num_try} times...")
                    GetNewSchedule(driver, url, sportName, num_try=num_try - 1)
                    return
                else:
                    print(f"No data found {sportName} {url}")
                    return


def fetchSchedule(driver):
    schedule_rows = []
    schedule_anticipate_rows = []
    if os.path.isfile("schedule_anticipate.json"):
        with open("schedule_anticipate.json", "r") as f:
            schedule_anticipate_rows = json.loads(f.read())
    if os.path.isfile("schedule.json"):
        with open("schedule.json", "r") as f:
            schedule_rows = json.loads(f.read())
    print("Fetching schedule")
    get(driver, "https://www.bet365.it/inplaydiaryapi/schedule?timezone=4&lid=6&zid=0")
    time.sleep(wait_time)
    schedule = driver.page_source
    dd = ""
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
            elif " - " in row["Casa"] and len(row["Casa"].split(" - ")) == 2:
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
            if row not in schedule_anticipate_rows:
                print(f"Adding new scheduled row {row}")
                if row["Data"] == datetime.now().strftime("%d/%m"):
                    schedule_rows.append(row)
                schedule_anticipate_rows.append(row)
    with open("schedule.json", "w") as f:
        f.write(json.dumps(schedule_rows, indent=4))
    print(f"Found {len(schedule_rows)} matches in schedule")
    with open("schedule_anticipate.json", "w") as f:
        f.write(json.dumps(schedule_anticipate_rows, indent=4))
    print(f"Found {len(schedule_anticipate_rows)} matches in schedule_anticipate")


def ParseScheduleData(data, sportName, driver):
    schedule_rows = []
    first = True
    try:
        if os.path.isfile(f"./SCHEDULE/{sportName}_schedule.json"):
            with open(f"./SCHEDULE/{sportName}_schedule.json", 'r') as f:
                schedule_rows = json.loads(f.read())
                first = False
    except:
        traceback.print_exc()
    championship = data.split("¬")[1].split(",#")[0]
    found = False
    for line in data.split("|"):
        if "MG;ID=" in line:
            try:
                if "Scommesse" not in line:
                    championship = line.split(";NA=")[1].split(";")[0]
                    continue
            except:
                pass
                # traceback.print_exc()
        if ";NA=" in line and ";N2=" in line:
            dt = datetime.strptime(line.split(";BC=")[1].split(";")[0], "%Y%m%d%H%M%S") + timedelta(hours=1)
            row = {
                "Casa": line.split(";NA=")[1].split(";")[0],
                "Ospite": line.split(";N2=")[1].split(";")[0],
                "Sport": sportName,
                "Date": dt.strftime("%d/%m/%Y"),
                "Time": dt.strftime("%H:%M"),
                "Championship": championship
            }
            if ";FS=1;" in line:
                row["Live"] = "Yes"
            else:
                row["Live"] = "No"
                row["url"] = f"https://www.bet365.it/#" + line.split(";PD=")[1].split(";")[0].replace("#", "/")
            # print(line)
            if row not in schedule_rows:
                print(f"Adding new scheduled row {row}")
                found = True
                if first:
                    schedule_rows.append(row)
                else:
                    schedule_rows.insert(0, row)
            else:
                found = True
                print(f"Row already added {row}")
    if not found:
        print(f"No new rows found {data}")
    # print(len(schedule_rows))
    with open(f"./SCHEDULE/{sportName}_schedule.json", 'w') as f:
        f.write(json.dumps(schedule_rows, indent=4))


def log_filter(log_):
    return log_["method"] == "Network.responseReceived"


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
    with ZipFile('bet365.zip', 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk('LIVE'):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, filePath)
        zipObj.write(os.path.join("schedule.json"), "PRE MATCH/schedule.json")
        zipObj.write(os.path.join("schedule_anticipate.json"), "PRE MATCH/schedule_anticipate.json")
        # zipObj.write(os.path.join("tennisBet365scheduled.json"), "PRE MATCH/tennisBet365scheduled.json")
        for schedule in schedule_list:
            file = f"./SCHEDULE/{schedule['Sport']}_schedule.json"
            if os.path.isfile(file):
                zipObj.write(os.path.join(file), file)
        zipObj.write("lastupdated-live.txt", "lastupdated-live.txt")
        if os.path.isfile("lastupdated-schedule.txt"):
            zipObj.write("lastupdated-schedule.txt", "lastupdated-schedule.txt")
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
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    if debug:
        # print("Connecting existing Chrome for debugging...")
        options.debugger_address = "127.0.0.1:9222"
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    else:
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f'--user-data-dir=C:/Selenium/{sport}')
        # options.add_extension("./proxy.zip")
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
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()),
                             options=options)


if __name__ == "__main__":
    main()
