from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def extract_authtoken(email, password):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    try:
        driver.get('https://www.lidl.cz/')
        time.sleep(2)

        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, '[data-ga-action="My Account"]').click()
        time.sleep(1)

        driver.find_element(By.ID, 'input-email').send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, 'Password').send_keys(password)
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        time.sleep(5)
        headers = None
        auth_token = None
        for request in driver.requests:
            if '/user-api/signin-oidc' in request.url:
                if request.response:
                    headers = request.response.headers

        print('headers', headers)

        if headers:
            for key, value in headers.items():
                if key.lower() == 'set-cookie' and value.startswith('authToken='):
                    auth_token = value.split(';')[0].split('=')[1]

        return auth_token
    except Exception as e:
        raise e
    finally:
        driver.quit()
