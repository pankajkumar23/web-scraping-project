from flask import Blueprint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
import time
from fake_useragent import UserAgent
from models.mobile_data_model import MobileData
from database.db import db

selenium_scrap_router = Blueprint("user",__name__)

@selenium_scrap_router.route("/web-scraping-selenium",methods =["GET"])
def scraping_data():
    try :
       
        ua = UserAgent()
        options =uc.ChromeOptions()
        options.add_argument(f"user-agent={ua.chrome}")
        driver = uc.Chrome(options=options)
        driver.get("https://www.flipkart.com/")
        elem= driver.find_element(By.NAME,"q")
        elem.send_keys("mobile")
        elem.send_keys(Keys.ENTER)
        ele= driver.find_element(By.CLASS_NAME,"_1G0WLw")
        link_ele= ele.find_element(By.CLASS_NAME,"WSL9JP")
        link = link_ele.find_element(By.TAG_NAME,"a")
        href = link.get_attribute("href")
        # page = ele.find_element(By.TAG_NAME,"span")
        # text = page.text
        # final_page = int(text.split()[-1])
        for i in range(1,42):
            try:
                if "page=" in href:
                    href = href.split("page=")[0] + f"page={i}"
                else:
                    href+=f"page={i}"
                driver.get(href)
                try:
                    elems = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "_75nlfW")))
                    
                except:
                    print(f"No products found on page {i}")
                    continue
                for ele in elems:
                    mobile_container=ele.find_element(By.CLASS_NAME, "yKfJKb")
                    title = mobile_container.find_element(By.CLASS_NAME,"KzDlHZ")
                    list_ele = mobile_container.find_element(By.CLASS_NAME,"_6NESgJ")
                    description = list_ele.find_element(By.TAG_NAME,"li")
                    element1 = mobile_container.find_element(By.CLASS_NAME,"BfVC2z")
                    element2 = element1.find_element(By.CLASS_NAME,"cN1yYO")
                    element3 = element2.find_element(By.CLASS_NAME,"hl05eU")
                    mobile_price = element3.find_element(By.CLASS_NAME,"Nx9bqj")
                    text = str(mobile_price.text)
                    f_mobile_price = text.replace("₹","")
                    f_mobile_price = f_mobile_price.replace(",","")
                    f_mobile_price = int(f_mobile_price)
                    mobile_data = MobileData(mobile_name=title.text.strip(),price=f_mobile_price,description=description.text.strip())
                    db.session.add(mobile_data)
                    db.session.commit()
                    print(f"{1}----->mobile_price :{f_mobile_price}\n,{1}----->title :{title.text}\n,{1}----->descriptions :{description.text}\n,")

                    # 
                    # for title in titles:
                    #     for description in descriptions:
                    #        
                    #     print(f"{i}========>title {title.text.strip()}\n,{i}========>description {description.text.strip()}")
                time.sleep(2)
            except Exception as e :
                print(f"error {i}:{e}")
        driver.quit()
        return {"message":"data scraped sucessfully!!"}
    except Exception as e:
        print(f" Error at scraping_data {e}")
        return {"message":str(e)},401

    