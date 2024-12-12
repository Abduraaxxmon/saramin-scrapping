from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from search import search
from search_req import job_list
from scrapping import Extract
from Collecting import collect_into_dataframe

# Set up Chrome option
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

# Set up WebDriver
cService = Service(executable_path=r"C:\Program Files (x86)\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(options=options)



driver.get("https://www.saramin.co.kr/zf_user/search?cat_mcls=2&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&keydownAccess=&panel_type=&search_optional_item=y&search_done=y&panel_count=y&preview=y")
time.sleep(7)

wait = WebDriverWait(driver, 10)

for job in job_list:

    search(title=job, wait= wait)
    time.sleep(2)

    data = Extract(driver=driver,wait=wait,ec=EC)

    data.load_data()

    collect_into_dataframe(
    name_companies=data.get_name_companies(),
    job_titles=data.get_job_titles(),
    location_jobs=data.get_location_jobs(),
    post_dates=data.get_post_dates(),
    skills=data.get_skills(),
    country="South Korea",
    job=job,
    )


driver.quit()

