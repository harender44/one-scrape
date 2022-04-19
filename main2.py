from selenium import webdriver
import pandas as pd

#specify your chrome webdriver path here
PATH = '/home/harender/drivers/chromedriver'

#chrome webdriver is used here
driver = webdriver.Chrome(executable_path=PATH)

#the url to scraped
url = 'https://www.giiresearch.com/material_report.shtml'

#specify the dates ( instead of only months as endpoints, dates or both can be used as endpoints after a few modifications)
#here months are used as endpionts 
start_date=input("Enter starting month: ")
end_date=input('Enter ending month: ')

driver.get(url)

data=[]

tables = driver.find_elements_by_class_name('plist_item')
for i in range(len(tables)):
    published =driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ i+2 }]/tbody/tr[2]/td/div[2]/div[1]/div[2]').text
    if published.split(' ')[0].lower() == end_date.lower():                          # 'end_date' because website shows the latest data before
        for j in range(i,len(tables)):
            published =driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ i+2 }]/tbody/tr[2]/td/div[2]/div[1]/div[2]').text
            if published.split(' ')[0].lower() == start_date.lower():                # 'start_dte' because website shows the older data later
                break
            title=driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ j+2 }]/tbody/tr[1]/td/div[2]/div/a[1]').text
            published_by = driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ j+2 }]/tbody/tr[2]/td/div[1]/div[1]/div[2]').text
            product_code =driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ j+2 }]//tbody/tr[2]/td/div[1]/div[2]/div[2]').text
            content_info = driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ j+2 }]/tbody/tr[2]/td/div[2]/div[2]/div[2]').text
            price_info = driver.find_element_by_xpath(f'.//*[@id="Content_Body"]/form[1]/table[{ j+2 }]/tbody/tr[2]/td/div[3]/div/div[2]/span').text
            #print(title +'\n'+published_by+'\n'+product_code+'\n'+published+'\n'+content_info+'\n'+price_info+'\n\n\n')
            data.append({
                'title': title,
                'published_by': published_by,
                'product_code': product_code,
                'published': published,
                'content_info': content_info,
                'price_info': price_info
            })
        break


df = pd.DataFrame(data)
df.to_csv(f'data_from_{start_date}_to_{end_date}.csv', index=False)