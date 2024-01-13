import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

def get_legi_dict(url1, url2, pages):
    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode to avoid opening a visible browser window

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    legi_dict_lst = []
    
    for i in range(1, pages+1):
        driver.get(url1+str(i)+url2)

        # Wait for the page to load (you may need to adjust the waiting time)
        time.sleep(1)
        
        # get td class
        lst_items = driver.find_elements(By.TAG_NAME, 'tr')
        for i, lst_item in enumerate(lst_items):
            if i == 0:
                continue
            items = lst_item.find_elements(By.TAG_NAME, 'td')

            legi_dict={
                "type": items[0].text,
                "title": items[1].text,
                "link": items[1].find_element(By.TAG_NAME, 'a').get_attribute('href'),
                "ministry": items[2].text,
                "start_date": items[3].text,
                "end_date": items[4].text,
            }
            # print(legi_dict["title"])
            legi_dict_lst.append(legi_dict)

    return legi_dict_lst

# Example usage
url1 = "https://moleg.go.kr/lawinfo/makingList.mo?mid=a10104010000&currentPage="
url2 = "&pageCnt=10&keyField=lmNm&keyWord=&stYdFmt=&edYdFmt=&lsClsCd=%EB%B2%95%EB%A5%A0&cptOfiOrgCd="
result = get_legi_dict(url1, url2, 582)

with open("legi_dict.jsonl", "w", encoding='utf-8') as f:
    for i, line in enumerate(result):
        line["id"] = i
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
