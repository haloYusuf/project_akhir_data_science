from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = "https://www.pinhome.id/dijual/cari/dki-jakarta-6?buildingType=building_type.house&sorter=last_modified_at_descend"



if url :
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    data = []
    for i in range(0, 100):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('div', attrs = {'class':'pin-card___heavr pin-card_compact___ze5lh pin-card_pointer___1venj'})
        for container in containers:
            try:
                type = container.find('ul', attrs = {'class':'pin-card__bullet-list___d8lwu pin-card__text_color-subtle___12yde pin-card__text_body3___kd1yj pin-card__ellipsis___xqz18'})
                house_type = type.find('li').text

                type = container.find('div', attrs = {'class':'pin-card__text_body3___kd1yj'})
                price = type.find('p', attrs = {'class': 'pin-card__text_heading3___1wnac pin-card__ellipsis___xqz18'}).text
                
                type = container.find('h3', attrs = {'class':'pin-card__text_label2___41ezj pin-card__title___dflce'})
                loc = container.find('p', attrs = {'class': 'pin-card__text_body3___kd1yj pin-card__text_color-subtle___12yde pin-card__ellipsis___xqz18'}).text

                listData = container.find('ul', attrs = {'class':'pin-card__bullet-list___d8lwu pin-card__text_body3___kd1yj pin-card__ellipsis___xqz18'})
                desc = listData.findAll('li')
                desc1 = []
                for v in desc:
                    try:
                        desc1.append(v.text.strip())
                    except AttributeError:
                        continue

                
                print(desc1)
                print("ya")
                rev = {
                    'type': house_type,
                    'price': price,
                    'loc': loc,
                    'kamar_tidur': desc1[0] if len(desc1) > 0 else None,
                    'luas_tanah': desc1[1] if len(desc1) > 1 else None,
                    'luas_bangunan': desc1[2] if len(desc1) > 2 else None,
                    'sertifikasi': desc1[3] if len(desc1) > 3 else None,
                }
                data.append(
                (rev)
                )
            except AttributeError:
                continue
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "a[data-testid^='btn-pagination-next']").click()
        time.sleep(2)

    print(data)
    df = pd.DataFrame(data, columns=["type", "price", "loc", "kamar_tidur", "luas_tanah", "luas_bangunan", "sertifikasi"])
    df.to_csv("rumah.csv", index=False)