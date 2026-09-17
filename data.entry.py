from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


#For scrap data from website
url = "https://appbrewery.github.io/Zillow-Clone/"

res = requests.get(url)
soup = BeautifulSoup(res.text,'html.parser')

data = soup.find_all("div",class_="StyledPropertyCardDataWrapper")
rent_price = []
space = []
link_address = []
address = []


for details in data:
    rent_price.append(details.find(name="span",class_="PropertyCardWrapper__StyledPriceLine").text.replace("/mo","").replace("+","").replace('1 bd',''))
    space.append(details.find_all(name="ul",class_="StyledPropertyCardHomeDetailsList")[0].text.strip())
    link_address.append(details.find('a').get('href'))
    address.append(details.find('address').text.strip().removeprefix("/n").replace("#",""))

sleep(10)
#Scrap , cleaning data and fill form to make a google sheet
Form_link = 'https://docs.google.com/forms/d/e/1FAIpQLSfUgKxqluHAcx_5OVg8UllZwnRqSpJScOjxwWhty62Nju3xHw/viewform?usp=header'

c_o = webdriver.ChromeOptions()
c_o.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=c_o)



sleep(5)

for x in range(0,44):
    try:
        driver.get(Form_link)
        Q1 = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.whsOnd.zHQkBf")))
        sleep(2)
        Q1[0].send_keys(address[x])
        Q1[1].send_keys(rent_price[x])
        Q1[2].send_keys(link_address[x])

        submit = driver.find_element(By.CSS_SELECTOR, 'span.NPEfkd ')
        submit.click()
        sleep(5)
    except TimeoutException:
        print("FIx that")









