from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

chrome_driver_path = "/Users/Matt.Stritzel/repos/WebScrapers/chromedriver"
os.environ["webdriver.chrome.driver"] = chrome_driver_path
web = 'https://sports.tipico.de/en/all/football/spain/la-liga'  # you can choose any other league (update 1)
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(web)

teams = []
x12 = [] #3-way
odds_events = []
#select only upcoming matches box
box = driver.find_element(By.CLASS_NAME, 'Program-styles-program') #update 3
#Looking for 'sports titles'
sport_title = box.find_elements(By.CLASS_NAME, 'SportTitle-styles-sport')

for sport in sport_title:
    # selecting only football
    if sport.text == 'Football':
        parent = sport.find_element(By.XPATH,'./..') #immediate parent node
        grandparent = parent.find_element(By.XPATH, './..') #grandparent node = the whole 'football' section
        #Looking for single row events
        single_row_events = grandparent.find_elements(By.CLASS_NAME, 'EventRow-styles-event-row')
        #Getting data
        for match in single_row_events:
            #'odd_events'
            odds_event = match.find_elements(By.CLASS_NAME,'EventOddGroup-styles-odd-groups')
            odds_events.append(odds_event)
            # Team names
            for team in match.find_elements(By.CLASS_NAME,'EventTeams-styles-titles'):
                teams.append(team.text)
        #Getting data: the odds
        for odds_event in odds_events:
            for n, box in enumerate(odds_event):
                rows = box.find_elements(By.XPATH, './/*')
                if n == 0:
                    x12.append(rows[0].text)

driver.quit()
dict_gambling = {'Teams': teams, '1x2': x12}
df_gambling = pd.DataFrame.from_dict(dict_gambling)
print(df_gambling)