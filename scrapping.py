import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Data_time_clean import clean_and_format_first_date

class Extract:
    def __init__(self, driver, wait, ec):
        self.driver = driver
        self.wait = wait
        self.ec = ec

        self.name_companies = []
        self.job_titles = []
        self.location_jobs = []
        self.post_dates = []
        self.skills = []

    def load_data(self):
        page_num = 1  # Start from page 1
        while True:
            try:
                # Find job titles on the current page
                job_titles = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'item_recruit')]//div[@class='area_job']//h2[@class='job_tit']/a")
                
                # Find and print the number of job listings on the current page
                print(f"Page {page_num}: Found {len(job_titles)} job listings")
                
                job_sectors = self.driver.find_elements(By.CLASS_NAME, 'job_sector')
                for job_sector in job_sectors:
                    skill = self.__skills_sectors(job_sector)
                    self.skills.append(skill)
                    time.sleep(1)

                # Extract job URLs
                job_urls = [url.get_attribute("href") for url in job_titles]
                print(f"Total job URLs found on page {page_num}: {len(job_urls)}")

                # Store the current page URL to return to it later
                current = self.driver.current_url

                # Scrape data for each job listing
                for job_url in job_urls:
                    time.sleep(1)
                    self.driver.get(job_url)
                    time.sleep(1)
                    self.__extract_data()

                # Go back to the current page after scraping each job listing
                self.driver.get(current)
                time.sleep(2)

                # Try to click the "Next Page" button or link
                pagination_link = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[@page='{page_num + 1}']"))
                )
                print(f"Navigating to page {page_num + 1}")
                pagination_link.click()
                page_num += 1

                # Sleep between page navigations to simulate human behavior
                time.sleep(2)

            except Exception as e:
                # If an error occurs (such as no next page), break the loop
                print(f"Error: {e}. Exiting pagination loop.")
                break

    def __extract_data(self):
        time.sleep(3)

        company_Xpath = '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/div[1]/a[1]'
        name_company = self.__get_text_or_nan(By.XPATH, company_Xpath)
        self.name_companies.append(name_company)

        job_title_xpath = '//*[@id="content"]/div[3]/section[1]/div[1]/div[1]/div/h1'
        job_title = self.__get_text_or_nan(By.XPATH, job_title_xpath)
        self.job_titles.append(job_title)

        location_xpath = '''//div[@class='col']//dl[dt[text()='근무지역']]/dd'''
        location = self.__get_text_or_nan(By.XPATH, location_xpath)
        self.location_jobs.append(location)

        posted_date_xpath = '''//*[@id="content"]//dl[contains(., '시작일')]'''
        posted_date = self.__get_text_or_nan(By.XPATH, posted_date_xpath)
        cleaned_date = clean_and_format_first_date(posted_date)
        self.post_dates.append(cleaned_date)

        print(f"ID: {len(self.name_companies)}, Posted Date: {cleaned_date}, Location: {location}, Job: {self.job_titles},Company: {self.name_companies}")

    def __get_text_or_nan(self, locator_type, locator_value):
        try:
            element = self.wait.until(EC.presence_of_element_located((locator_type, locator_value)))
            return element.text.strip() if element and element.text.strip() else "N/A"
        except Exception as e:
            return "N/A"

    def __skills_sectors(self, sector):
        try:
            # Find all category elements within the sector
            categories = sector.find_elements(By.XPATH, ".//a")

            if categories:
                # Extract category names
                category_texts = [category.text for category in categories]
                # print("Job Categories:", category_texts)  # Printing the categories

                # Clean the category texts by removing 'etc' and unwanted characters

                # Join the cleaned categories into a single string, separated by a comma and space
                cleaned_string = ', '.join(category_texts).replace("etc", "").strip()  # Join cleaned categories into a string with commas
                print(cleaned_string)
                # Return the cleaned string
                return cleaned_string if cleaned_string else "N/A"
            else:
                print("No categories found in this job sector.")
                return "N/A"  # Return "N/A" if no categories are found

        except Exception as e:
            print(f"Error extracting job categories: {str(e)}")
            return "N/A"  # Return "N/A" in case of an error




    # Getter for _name_companies
    def get_name_companies(self):
        return self.name_companies

        # Getter for _job_titles

    def get_job_titles(self):
        return self.job_titles

        # Getter for _location_jobs

    def get_location_jobs(self):
        return self.location_jobs

        # Getter for _post_dates

    def get_post_dates(self):
        return self.post_dates

        # Getter for _logo_urls

    def get_logo_urls(self):
        return self.logo_urls

        # Getter for _skills

    def get_skills(self):
        return self.skills