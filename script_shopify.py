import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Remplir le formulaire Shopify
def fill_form(url, info):
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
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Remplir les champs
    driver.find_element(By.NAME, 'user[company_name]').send_keys(info['nom_entreprise'])
    driver.find_element(By.NAME, 'user[email]').send_keys(info['email'])
    driver.find_element(By.NAME, 'user[address]').send_keys(info['adresse'])
    driver.find_element(By.NAME, 'user[city]').send_keys(info['ville'])
    driver.find_element(By.NAME, 'user[zip]').send_keys(info['code_postal'])
    driver.find_element(By.NAME, 'user[country]').send_keys(info['pays'])
    driver.find_element(By.NAME, 'user[province]').send_keys(info['province'])
    driver.find_element(By.NAME, 'website').send_keys(info['website'])
    
    # Trouver et cliquer sur le bouton de soumission
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

    # Scroll to the submit button
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(1)  # wait for scrolling to finish

    # Use Actions class to click the button
    actions = ActionChains(driver)
    actions.move_to_element(submit_button).click().perform()

    # Attendre que la page se charge (si nécessaire)
    time.sleep(5)
    driver.quit()

@app.route('/submit', methods=['POST'])
def submit():
    info = request.json
    urls = [
        "https://www.shopify.com/fr/outils/generateur-de-politique",
        # "https://www.shopify.com/fr/outils/generateur-de-politique/conditions-generales-de-vente-et-d-utilisation",
        # "https://www.shopify.com/fr/outils/generateur-de-politique/remboursement"
    ]
    
    for url in urls:
        fill_form(url, info)
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
