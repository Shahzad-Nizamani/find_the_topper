from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class BatchNotFoundError(Exception):
    pass

class SubjectNotFoundError(Exception):
    pass

def get_result_page(dept, year, semester, batch, subject):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Path to chromedriver on Linux
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
      driver.get("https://exam.usindh.edu.pk/v2/course.php") 
      
      prog = f"BS ({dept})"

      if dept in ["ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCES"]:
         dept = "CENTRE FOR ENVIRONMENTAL SCIENCES"
         prog = "BS (ENVIRONMENTAL SCIENCES)"

      department = Select(driver.find_element(By.ID, "dept_id"))
      options = [option.text.strip() for option in department.options]
      if dept not in options:
         raise ValueError (f"{dept} was not found, please enter with correct")
      wait = WebDriverWait(driver, 10)
      wait.until(EC.presence_of_element_located(
      (By.XPATH, f"//select[@id='dept_id']/option[text()='{dept}']")
      ))
      department.select_by_visible_text(dept)

      if dept == "MEDIA & COMMUNICATION STUDIES":
         dept = "MASS COMMUNICATION"
         prog = f"BS ({dept})"


      if '&' in dept:
         dept = dept.replace('&', "AND")
         prog = f"BS ({dept})"

      
      if dept == "BUSINESS ADMINSTRATION":
         prog = "B.B.A (HONS)"

      program = Select(driver.find_element(By.ID, "program_id"))
      wait = WebDriverWait(driver, 3)
      wait.until(EC.presence_of_element_located(
      (By.XPATH, f"//select[@id='program_id']/option[text()='{prog}']")
      ))
      program.select_by_visible_text(prog)

      y = Select(driver.find_element(By.ID, "exam_year"))
      y.select_by_visible_text(year)

      sem = Select(driver.find_element(By.ID, "semesterCombo"))
      sem.select_by_visible_text(semester)

      time.sleep(1)
      dropdown = Select(driver.find_element(By.ID, "batch"))

      found = False
      for option in dropdown.options:
            if option.text.strip() == batch:
               dropdown.select_by_visible_text(option.text)
               found = True
               break
      if not found:
            driver.quit()
            raise BatchNotFoundError(f"Batch '{batch}' not found in dropdown.")

      time.sleep(1)

      course = Select(driver.find_element(By.ID, "courseNo"))

      found = False
      for option in course.options:
         if option.text.strip() == subject:
          course.select_by_visible_text(option.text)
          found = True
          break
      if not found:
         driver.quit()
         raise SubjectNotFoundError(f"Subject '{subject}' not found in dropdown.")
      
      display_button = driver.find_element(By.ID, "display")
      display_button.click()
      wait = WebDriverWait(driver, 10)
      wait.until(EC.presence_of_element_located((By.ID, "course")))
      time.sleep(1)
      html = driver.page_source
      return html
    finally:
       driver.quit()

def find_topper(dept, year, semester, batch, subject):
   try:
      html = get_result_page(dept, year, semester, batch, subject)
   except BatchNotFoundError:
      return "Invalid batch. Please check the batch selection."
   except SubjectNotFoundError:
      return "Invalid subject. Please check the subject selection."
   except Exception as e:
      return f"An unexpected error occurred: {e}"

   
   soup = BeautifulSoup(html, "html.parser")
   data = {}
   
   table = soup.select_one("table.table.table-bordered.table-striped")
   body = table.find("tbody")
   rows = body.find_all("tr")

   for row in rows:
      headers = row.find_all("th")
      if len(headers) < 6:
       continue
      
      roll_no = headers[1].text + '-'
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