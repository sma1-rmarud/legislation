import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

def get_legi_content(json_path, save_path):

    options = ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode to avoid opening a visible browser window

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    with open(save_path, "a", encoding='utf-8') as u:
        with open(json_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 563:
                    continue
                elif i < 1899:
                    continue
                elif i < 2092:
                    continue
                print(i)
                result_dict = {}
                data = json.loads(line)
                url = data['link']
                driver.get(url)

                # Wait for the page to load (you may need to adjust the waiting time)
                time.sleep(1)
                
                tb_contents = driver.find_elements(By.CLASS_NAME, 'tb_contents')
                if len(tb_contents) != 1:
                    print(f"len(tb_content) is not 1 ({len(tb_contents)}), id: {data['id']}")
                    break
                else:
                    tb_content = tb_contents[0]
                    main_text = ""
                    main_contents = tb_content.find_elements(By.TAG_NAME, 'p')
                    for content in main_contents:
                        main_text += content.text
                        main_text += "\n"
                    result_dict['main_text'] = main_text
                    
                    embed_file_tb = tb_content.find_element(By.TAG_NAME, 'ul')

                    embed_files = embed_file_tb.find_elements(By.TAG_NAME, 'li')
                    for embed_file in embed_files:
                        file_name = embed_file.find_element(By.TAG_NAME, 'strong').text
                        embed_file_links = embed_file.find_elements(By.TAG_NAME, 'a')

                        for embed_file_link in embed_file_links:
                            link = embed_file_link.get_attribute('href')
                            name = embed_file_link.text
                            if "hwp" in name:
                                result_dict[file_name+'hwp'] = link
                            elif "pdf" in name:
                                result_dict[file_name+'pdf'] = link
                            else:
                                result_dict[file_name] = link
                    
                    result_dict['id'] = data['id']
                    u.write(json.dumps(result_dict, ensure_ascii=False) + "\n")
                            
if __name__ == "__main__":
    myjsonl = "C:/Users/ohs/Documents/legislation/legi_dict.jsonl"
    save_path = "C:/Users/ohs/Documents/legislation/legi_content.jsonl"
    get_legi_content(myjsonl, save_path)