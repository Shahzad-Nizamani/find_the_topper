from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def get_result_page(dept, year, semester, batch, subject):
    # Setup headless Chrome options for Linux
    options = Options()
    options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    options.add_argument("--no-sandbox")  # Required for Linux servers
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Path to chromedriver on Linux
    service = Service(executable_path="/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://exam.usindh.edu.pk/v2/course.php")

        # SECURITY: Validate all user input before injecting into web selectors

        prog = f"BS ({dept})"

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='dept_id']/option[text()='{dept}']")
        ))
        department = Select(driver.find_element(By.ID, "dept_id"))
        department.select_by_visible_text(dept)

        if dept == "MEDIA & COMMUNICATION STUDIES":
            dept = "MASS COMMUNICATION"
            prog = f"BS ({dept})"

        if '&' in dept:
            dept = dept.replace('&', "AND")
            prog = f"BS ({dept})"

        if dept == "BUSINESS ADMINSTRATION":
            prog = "B.B.A (HONS)"

        if dept == "PHARMACY":
            prog = "DOCTOR OF PHARMACY (PHARM. D)"

        if dept == "SINDH DEVELOPMENT STUDIES CENTRE":
            prog = "BS (RURAL DEVELOPMENT)"

        wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='program_id']/option[text()='{prog}']")
        ))
        program = Select(driver.find_element(By.ID, "program_id"))
        program.select_by_visible_text(prog)

        y = Select(driver.find_element(By.ID, "exam_year"))
        y.select_by_visible_text(year)

        sem = Select(driver.find_element(By.ID, "semesterCombo"))
        sem.select_by_visible_text(semester)

        space_batch = batch + "  "
        wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//select[@id='batch']/option[text()='{space_batch}']")
        ))
        dropdown = Select(driver.find_element(By.ID, "batch"))

        for option in dropdown.options:
            if option.text.strip() == batch:
                dropdown.select_by_visible_text(option.text)
                break

        wait.until(EC.text_to_be_present_in_element((By.ID, "courseNo"), subject))
        course = Select(driver.find_element(By.ID, "courseNo"))
        course.select_by_visible_text(subject)

        display_button = driver.find_element(By.ID, "display")
        display_button.click()

        wait.until(EC.presence_of_element_located((By.ID, "course")))
        time.sleep(1)  # wait for table to render

        html = driver.page_source
        return html

    except Exception as e:
        print(f"[ERROR] Something went wrong: {e}")
        return None

    finally:
        driver.quit()  # Ensure the browser closes no matter what


def find_topper(dept, year, semester, batch, subject):
    html = get_result_page(dept, year, semester, batch, subject)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    data = {}

    table = soup.select_one("table.table.table-bordered.table-striped")
    if not table:
        print("[ERROR] Results table not found.")
        return None

    body = table.find("tbody")
    rows = body.find_all("tr")

    for row in rows:
        headers = row.find_all("th")
        if len(headers) < 6:
            continue

        roll_no = headers[1].text.strip() + ' - '
        name = headers[2].text.strip()
        marks = headers[5].text.strip()

        data[roll_no + name] = marks

    # Extract top 3 unique scores
    unique_marks = sorted(set(data.values()), reverse=True)
    top_scores = unique_marks[:3]

    first = [k for k, v in data.items() if v == top_scores[0]]
    second = [k for k, v in data.items() if len(top_scores) > 1 and v == top_scores[1]]
    third = [k for k, v in data.items() if len(top_scores) > 2 and v == top_scores[2]]

    # Output
    print(f"\n📘 Highest marks in {subject}:")

    print("\n🥇 FIRST: ")
    for name in first:
        print(name + " = " + data[name])

    print("\n🥈 SECOND: ")
    for name in second:
        print(name + " = " + data[name])

    print("\n🥉 THIRD: ")
    for name in third:
        print(name + " = " + data[name])

    return [first, second, third], top_scores
