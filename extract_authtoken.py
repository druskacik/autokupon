import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extract_authtoken_from_headers(headers):
    auth_token = None
    for key, value in headers.items():
        if key.lower() == 'set-cookie' and value.startswith('authToken='):
            auth_token = value.split(';')[0].split('=')[1]
    return auth_token

def extract_authtoken(email, password, proxy_url=None):
    options = Options()
    
    seleniumwire_options = {}
    if proxy_url:
        seleniumwire_options = {
            'proxy': {
                'http': proxy_url,
                'https': proxy_url,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    if os.getenv('GITHUB_ACTIONS') == 'true':
        options.add_argument("--headless")
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-dev-shm-usage")
    else:
        # options.add_argument("--headless") 
        pass
    driver = webdriver.Firefox(options=options, seleniumwire_options=seleniumwire_options)
    try:
        driver.get('https://www.lidl.cz/')
        wait = WebDriverWait(driver, 20)

        # Wait for and accept cookies
        cookie_btn = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookie_btn.click()

        # Wait for cookie banner to disappear
        wait.until(EC.invisibility_of_element_located((By.ID, 'onetrust-banner-sdk')))
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'onetrust-pc-dark-filter')))

        # Wait for and click My Account
        account_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-ga-action="My Account"]')))
        account_btn.click()

        # Wait for login page
        email_input = wait.until(EC.visibility_of_element_located((By.ID, 'input-email')))
        email_input.send_keys(email)

        password_input = wait.until(EC.visibility_of_element_located((By.ID, 'Password')))
        password_input.send_keys(password)

        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        submit_btn.click()

        # Wait some time for the auth token to appear in network requests
        time.sleep(5)
        headers = None
        auth_token = None
        for request in driver.requests:
            # if '/user-api/signin-oidc' in request.url:
            #     if request.response:
            #         headers = request.response.headers
            if request.response:
                headers = request.response.headers
                auth_token = extract_authtoken_from_headers(headers)
                if auth_token:
                    break

        # print('headers', headers)

        if headers:
            for key, value in headers.items():
                if key.lower() == 'set-cookie' and value.startswith('authToken='):
                    auth_token = value.split(';')[0].split('=')[1]

        return auth_token
    except Exception as e:
        raise e
    finally:
        driver.quit()
