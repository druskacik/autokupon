import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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
        time.sleep(2)

        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(2)

        driver.find_element(By.CSS_SELECTOR, '[data-ga-action="My Account"]').click()
        time.sleep(5)

        driver.find_element(By.ID, 'input-email').send_keys(email)
        time.sleep(1)
        driver.find_element(By.ID, 'Password').send_keys(password)
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

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
