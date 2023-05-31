'''
Created on Aug 21, 2020

@author: DNP Enterprises Inc.
Loads the carsdb.dealers database from spreadsheets
'''
import openpyxl
import pandas as pd

if __name__ == '__main__':
    car_data_file = 'C:/Users/dpenn/Desktop/Cars/CarData.xlsx'
    wkbk = openpyxl.load_workbook(car_data_file)
    dealers = pd.DataFrame(columns = ['Name', 'ID', 'Address', 'Location', 'Phone']) #create dataframe ready for loading
    total_record_count = 0
    for sheet in wkbk.sheetnames: #get each sheet
        print ("Loading: ", sheet)
        wksh = wkbk[sheet]
        record_count = 0
        for index, row in enumerate(wksh.rows): # for each sheet, scan the rows for data
            if index == 0:
                continue # skip first row which is for column headings
            dealer_name = row[0].value
            dealer_id = row[2].value
            dealer_address = row[3].value
            dealer_location = row[4].value
            dealer_phone = row[5].value
            print ("Name: ", dealer_name, "ID: ", dealer_id, "Address: ",  dealer_address, "Location: ", dealer_location, "Phone: ", dealer_phone)
            val = pd.DataFrame([{'Name': dealer_name, 'ID': dealer_id, 'Address':dealer_address, 'Location':dealer_location, 'Phone':dealer_phone }])
            dealers = pd.concat([dealers, val])
            record_count +=1
        print (record_count, "records inserted for ,", sheet)
        total_record_count = total_record_count + record_count
print ("total records added :",   total_record_count)
#dealers.to_excel('C:/Users/dpenn/Desktop/Cars/dealers.xlsx', index = False)
dealers.to_csv('C:/Users/dpenn/Desktop/Cars/dealers.csv', index = False)
            