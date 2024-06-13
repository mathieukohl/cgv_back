import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def fill_form(url, info):
    logger.info(f"Starting to fill form at {url} with info {info}")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size to avoid any issues with visibility
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Set paths for Chrome and ChromeDriver
    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', '/app/.apt/usr/bin/google-chrome')
    chrome_options.binary_location = chrome_bin
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/app/.chromedriver/bin/chromedriver')

    driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=chrome_options)
    driver.get(url)

    try:
        # Fill the form fields
        logger.info("Filling form fields")
        driver.find_element(By.NAME, 'user[company_name]').send_keys(info['nom_entreprise'])
        driver.find_element(By.NAME, 'user[email]').send_keys(info['email'])
        driver.find_element(By.NAME, 'user[address]').send_keys(info['adresse'])
        driver.find_element(By.NAME, 'user[city]').send_keys(info['ville'])
        driver.find_element(By.NAME, 'user[zip]').send_keys(info['code_postal'])
        driver.find_element(By.NAME, 'user[country]').send_keys(info['pays'])
        driver.find_element(By.NAME, 'user[province]').send_keys(info['province'])
        driver.find_element(By.NAME, 'website').send_keys(info['website'])

        # Find and click the submit button
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)  # wait for scrolling to finish

        actions = ActionChains(driver)
        actions.move_to_element(submit_button).click().perform()

        logger.info("Form submitted successfully")
        time.sleep(5)  # Wait for any potential page load
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        driver.quit()

@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200  # Respond to preflight request

    info = request.json
    urls = [
        "https://www.shopify.com/fr/outils/generateur-de-politique",
    ]
    
    for url in urls:
        fill_form(url, info)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
