from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import shutil
import tempfile


class BatchNotFoundError(Exception):
    pass

class SubjectNotFoundError(Exception):
    pass

def get_result_page(dept, year, semester, batch, subject):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Use a unique temporary user-data-dir for each run
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    # Path to chromedriver on Linux
    chrome_driver_path = shutil.which("chromedriver")
    print("Found ChromeDriver at:", chrome_driver_path)
    service = Service(executable_path="D:\python practice\chromedriver-win64/chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    try:
      driver.get("https://exam.usindh.edu.pk/v2/course.php") 
      
      prog = f"BS ({dept})"

      if dept in ["ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCES"]:
         dept = "CENTRE FOR ENVIRONMENTAL SCIENCES"
         prog = "BS (ENVIRONMENTAL SCIENCES)"

      department = Select(driver.find_element(By.ID, "dept_id"))
      dept_options = [option.text.strip() for option in department.options]
      if dept not in dept_options:
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

      if "LAB" in subject:
         subject = subject.replace("(LAB)", "LAB").replace("(lab)", "LAB")
         subject = subject.replace("lab", "LAB").replace("Lab", "LAB")
         subject = subject.replace("LAB", "(LAB)")

      if "MINOR" in subject:
       subject = subject.replace("(MINOR)", "MINOR").replace("(minor)", "MINOR").replace("minor", "MINOR")
       subject = subject.replace("MINOR", "(MINOR)")
      
      if subject == "COMPILER CONSTRUCTION":
         subject = "COMPLIER CONSTRUCTION"

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
      for batch_option in dropdown.options:
            if batch_option.text.strip() == batch:
               dropdown.select_by_visible_text(batch_option.text)
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
       shutil.rmtree(temp_dir, ignore_errors=True)