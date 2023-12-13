import selenium.common.exceptions
from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from RacerData import RacerData
import math

driver = webdriver.Firefox()
resPerPage = 9


def page(pageNum, perPage=resPerPage):
    return "https://labs.competitor.com/result/subevent/33C67F48-BA3C-472C-B696-2D8CAD67B46E?filter={}&order=ASC&page="+str(pageNum)+"&perPage="+str(perPage)+"&sort=FinishRankOverall"


driver.get(page("1"))
driver.implicitly_wait(0.5)

headers = ["Name", "Position", "Swim time", "Swim to Bike", "Bike time", "Bike to run", "Run time", "Final", "Gender",
           "Division"]
racingData = []

# totalPages = math.floor(int(driver.find_elements(by=By.CLASS_NAME, value="css-q4n587")[1].text.split(" ")[2])/10)


def isCorrectEncoding(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def get_page_data():
    table = None
    while not table:
        try:
            table = driver.find_element(by=By.ID, value="resultList")
        except selenium.common.exceptions.NoSuchElementException:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            table = driver.find_element(by=By.ID, value="resultList")

    racersOnPage = []
    for row in range(1, resPerPage+1):
        rows = table.find_elements(By.XPATH, value="//body//tbody//tr["+str(row)+"]")
        for row_data in rows:
            col = row_data.find_elements(By.TAG_NAME, "td")
            racer = RacerData()
            racer.import_data(col)
            if not isCorrectEncoding(racer.name):
                racer.name = "INCORRECT ENCODING"
            racersOnPage.append(racer)

    expandables = driver.find_elements(By.CLASS_NAME, "css-1j7qk7u")
    for i in range(len(expandables)):
        e = expandables[i]
        ActionChains(driver).click(e).perform()

        # Swim -> Bike transition index is times[3], bike -> run t is times[4]
        tTimes = driver.find_element(By.ID, "transitions")
        times = tTimes.find_elements(By.CLASS_NAME, "text")

        # Get division
        genInfoWrap = driver.find_element(By.CLASS_NAME, "genInfo")
        genInfoTable = genInfoWrap.find_element(By.CLASS_NAME, "tableFooter")
        gender_division = genInfoTable.find_elements(By.CLASS_NAME, "text")[1].text

        racersOnPage[i].t1 = times[2].text
        racersOnPage[i].t2 = times[3].text
        gender = list(gender_division)[0]
        division = "".join(list(gender_division)[1:])
        racersOnPage[i].gender = gender
        racersOnPage[i].division = division

        ActionChains(driver).click(e).perform()

    racerToCsv = [r.listOf() for r in racersOnPage]
    return racerToCsv


p = 1
lastTime = "99:99:99"
while racingData[-1][-3] != "00:00:00":
    try:
        racingData.extend(get_page_data())

        driver.get(page(p+1))
        driver.implicitly_wait(1)
        p += 1
        lastTime = racingData[-1][-3]
    except:
        break

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(racingData)

driver.close()
