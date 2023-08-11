'''
Created on Aug 11, 2023

@author: dpenn
'''
import re

txt = "This is a testt 123 !@#"

found = re.sub("i","9",txt)
print (found)

found = re.findall("[T|t]", txt)
print (found)

found = re.sub("[A-Za-z]","0-9",txt)
print (found)

found = re.sub("T|t","A",txt)
print (found)

found = re.sub("t{2}","*",txt)
print (found)

found = re.sub("\d","*",txt)
print (found)

found = re.sub("\D","*",txt)
print (found)

found = re.sub("\W","*",txt)
print (found)

found = re.sub("\w","*",txt)
print (found)

found = re.sub("!@#\Z","*",txt)
print (found)

found = re.sub("[0-9]","*",txt)
print (found)

found = re.sub("[^a-n]","*",txt)
print (found)



