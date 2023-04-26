'''
@author: DNP Enterprises Inc.

'''
from datetime import datetime
from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
from Cars.CreateDealerSheet2 import CreateDealerSheet
from Cars.Scroll_Browser import Scroll_Browser
from selenium.webdriver.common.action_chains import ActionChains
from Cars.browser_start import browser_start
from Cars.close_out import close_out

if __name__ == '__main__':
    file_in = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Chrysler', 'in')
    file_out = data_in.sht.cell(6,7).value
    dealer = data_in.sht.cell(6,1).value
    url = data_in.sht.cell(6,2).value
    dealer_id = (data_in.sht.cell(6,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name

    headless = False
    #headless = True
    driver = browser_start(url, headless)
    #WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.d-none"))) # wait for # of vehicles to be displayed
    print (driver.title)
    num_cars = driver.find_element(By.CSS_SELECTOR, 'span.d-none').text
    num_cars = re.sub("[^0-9]", "", num_cars) # remove "Vehicles" and keep numeric part
    print ("Number of cars found on site: " , num_cars)

    try:
        driver.find_element(By.CSS_SELECTOR, '.ui-dialog-titlebar-close').click()
    except:
        pass
        
    scroll_pause_time = 2 # scroll all the way down until all pages are loaded
    Scroll_Browser(driver, scroll_pause_time)
    count = 0
    zero = 0
    car_info = []
    pages_remaining = True
    while pages_remaining:
        #Scroll_Browser(driver, scroll_pause_time)
        car_details = driver.find_elements(By.CSS_SELECTOR, '.vehicle-card-details-container')
        #car_prices = driver.find_elements(By.CSS_SELECTOR, '.value:not(.text-nowrap)')
        car_prices = driver.find_elements(By.CSS_SELECTOR, 'span.price-value')
        details_links = driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card-details-container [href]')
        stock = driver.find_elements(By.CSS_SELECTOR, 'li.stockNumber') # stock labels
                
        for index, car in enumerate(car_details):
            car_name = re.sub('[\n]', " ", car.text)
            car_name = car_name.split('|')[0] # remove extra descriptions
            car_name = car_name.split()[:4] # keep the year, make, and model, remove the rest
                 
            year = car_name[0].split() # convert the year to a list
            make = car_name[1].split() # convert make to a list
            model = car_name[2:] # model is already a list
            model = ' '.join(model).replace('Mazda','').split() #remove Mazda or MAZDA from model
            model = ' '.join(model).replace('MAZDA','').split()
            model = [' '.join(model)] # merge the model into one list element
            car_desc = year + make + model
            price = car_prices[index].text
            price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
            price = price.split() # convert to a list
            
            stock_num = stock[index].text
            stock_num = (re.sub("[Stock #: ]", "", stock[index].text)).split() # remove "Stock #: " from the stock number and convert to a list
            link = (details_links[index].get_attribute('href')).split()
            
            print (index,":", car_desc, price, stock_num, link)
            car_info.append(dealer_id + car_desc + price + stock_num + link) 
            
        count = count + index +1
        print ("Running count: ", count)
          
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next [href]')
            page_num = driver.find_element(By.CSS_SELECTOR, 'li.active').text
            print ("Page #: ", page_num, " : ", next_page.get_attribute('href'))
            ActionChains(driver).move_to_element(next_page).click(next_page).perform() # click on Next link
            #next_page.click() # click on Next link
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.d-none"))) # wait for # of vehicles to be displayed
            sleep (2)
        except:
            print ("Total cars processed: ", count, " Total unpriced cars: ", zero)
            pages_remaining = False
    #close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)        
    car_info = sorted(car_info)
    for index, i in enumerate(car_info):
        print (index, ":", i)
        
    print ("Saving data in a spreadsheet....", file_out)
    CreateDealerSheet(data_out, car_info, date_time)
    print (dealer, "Total cars: " , count)
    data_out.save_file(file_out)
       
    driver.quit() # Close the browser and end the session
