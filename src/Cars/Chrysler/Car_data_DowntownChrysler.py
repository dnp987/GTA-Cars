'''
Same as Scarborough Mazda
@author: DNP Enterprises Inc.
'''
from datetime import datetime
from time import sleep
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Quotes.Excel_utils2 import Excel_utils2
#from Cars.mazda_fix import mazda_fix
from Cars.browser_start import browser_start
from Cars.close_out import close_out

if __name__ == '__main__':
    file_in = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
    data_in = Excel_utils2(file_in, 'Chrysler', 'in')
    file_out = data_in.sht.cell(3,7).value
    dealer = data_in.sht.cell(3,1).value
    url = data_in.sht.cell(3,2).value
    dealer_id = (data_in.sht.cell(3,3).value).split() # convert to a list for use later
    date_time = datetime.now().strftime('%Y %B %d %I %M %p') # get the date and time
    data_out = Excel_utils2(' ', date_time, 'out') # set the spreadsheet tab to the dealer name
    
    headless = False
    #headless = True # this site seemingly won't work with headless mode
    driver = browser_start(url, headless)
        
    wait = WebDriverWait(driver, 10) # set the default web element wait time
    #WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.logo_wrapper'))) # site logo
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.title_wrapper'))) # site logo
    
    print (driver.title)
    num_cars = int(driver.find_element(By.CSS_SELECTOR, 'span.srp_carbon_results__count--digits').text)
    print ("Number of cars found on site: " , num_cars)
    pages_remaining = True
        
    zero = 0
    count = 0
    car_info = []
    while pages_remaining:
        car_desc = driver.find_elements(By.CSS_SELECTOR, 'h2.vehicle_title') # car description, make, model
        car_prices = driver.find_elements(By.CSS_SELECTOR, 'dd.vehicle_price') # car prices
        details_links = driver.find_elements(By.CSS_SELECTOR, 'a.vehicle_item__vehicle_link')
        
        for index, (cars, prices, links) in enumerate(zip(car_desc, car_prices, details_links)):
            car = cars.text.replace('Pre-Owned ', '') # remove Pre-Owned from the description
            year = car[0:4].split()
            make_model = car[5:].split()
            make = make_model[0].split()
            model = make_model[1:]
            model = [' '.join(make_model[1:])] # merge the model into one list element
            car_desc = year + make + model
            
            price = prices.text
            price = re.sub("[^0-9]", "", price) #remove text and keep the numeric part
            if len(price) == 0: # if the price is "Call for price" or something non-numeric, set the price to 0
                price = '0'
                zero += 1
                
            price = price.split() # convert to a list
            stock_num = ('N/A').split() # stock number is found on each car details page
            link = (links.get_attribute('href')).split()
            count += 1
            print (index, " : ", dealer_id + car_desc + price + stock_num + link)
            car_info.append(dealer_id + car_desc + price + stock_num + link)                                                     
        try:
            next_page = driver.find_element(By.CSS_SELECTOR, "li.next")
            next_page.click() # click on Next link
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.title_wrapper'))) # site logo
            #sleep (2)
            print ('Next page loaded: ',  driver.current_url)
        except:
            pages_remaining = False
            print ('*** Last page ***')
    
    close_out(driver, dealer, count, zero, num_cars, data_out, file_out, date_time, car_info)
