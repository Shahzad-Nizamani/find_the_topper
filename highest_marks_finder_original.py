from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup


def find_topper(dept, year, semester, batch, subject):

   html = get_result_page(dept, year, semester, batch, subject)

   soup = BeautifulSoup(html, "html.parser")
   data = {}
   
   table = soup.select_one("table.table.table-bordered.table-striped")
   body = table.find("tbody")
   rows = body.find_all("tr")

   for row in rows:
      headers = row.find_all("th")
      if len(headers) < 6:
       continue
      
      roll_no = headers[1].text + ' - '
      name = headers[2].text
      data[roll_no+name] = headers[5].text

   marks = set(data.values())
   marks = list(marks)
   marks.sort()
   vals = [marks[len(marks)-1], marks[len(marks)-2], marks[len(marks)-3]]

   first = [k for k, v in data.items() if v == vals[0]]
   second = [k for k, v in data.items() if v == vals[1]]
   third = [k for k, v in data.items() if v == vals[2]]

   print(f"Highest marks in {subject}: ")

   print("FIRST: ")
   for name in first:
      print(name + " = " + data[name])

      print("SECOND: ")
   for name in second:
      print(name + " = " + data[name])
   
   print("THIRD: ")
   for name in third:
      print(name + " = " + data[name])

   return [first, second, third], [vals[0], vals[1], vals[2]] 
   