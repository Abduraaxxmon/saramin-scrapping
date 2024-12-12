import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def search(title, wait):
    try:
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'btn_keyword btn_open_layer keyword')]"))
        )
        button.click()
        time.sleep(3)  # Wait for the input field to be visible (if dynamic)

        # Now find the input field
        search_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='search_keyword']"))  # Update this XPath with the actual input field
        )

        # Send keys to the input field
        search_input.send_keys(title)
        search_input.send_keys(Keys.ENTER)  # or Keys.ENTER

        time.sleep(10)  # Let the search complete or process

    except Exception as e:
        print("Error:", e)