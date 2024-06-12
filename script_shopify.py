from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# # Collect user data
# def collect_user_info():
#     info = {}
#     info['company_name'] = input("Nom de l’entreprise : ")
#     info['email'] = input("Adresse e-mail : ")
#     info['address'] = input("Adresse : ")
#     info['city'] = input("Ville : ")
#     info['postal_code'] = input("Code postal : ")
#     info['country'] = input("Pays/Région : ")
#     info['state'] = input("Province/Département/État : ")
#     info['website'] = input("Url de votre site web :")
#     return info

# Fill the Shopify form
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

    # fill the form
    driver.find_element(By.NAME, 'user[company_name]').send_keys(info['company_name'])
    driver.find_element(By.NAME, 'user[email]').send_keys(info['email'])
    driver.find_element(By.NAME, 'user[address]').send_keys(info['address'])
    driver.find_element(By.NAME, 'user[city]').send_keys(info['city'])
    driver.find_element(By.NAME, 'user[zip]').send_keys(info['postal_code'])
    driver.find_element(By.NAME, 'user[country]').send_keys(info['country'])
    driver.find_element(By.NAME, 'user[province]').send_keys(info['state'])
    driver.find_element(By.NAME, 'website').send_keys(info['website'])
    
    # Find the submission btn
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
    app.run(debug=True)


# Fonction principale
# def main():
#     info = collect_user_info()

#     # info = {
#     #     'nom_entreprise': 'Nom Test Entreprise',
#     #     'email': 'mathieukohl@hotmail.com',
#     #     'adresse': '123 Rue de Test',
#     #     'ville': 'Ville de Test',
#     #     'code_postal': '75000',
#     #     'pays': 'France',
#     #     'province': 'Île-de-France',
#     #     'website': 'test.fr'
#     # }

#     urls = [
#         "https://www.shopify.com/fr/outils/generateur-de-politique",
#         "https://www.shopify.com/fr/outils/generateur-de-politique/conditions-generales-de-vente-et-d-utilisation",
#         "https://www.shopify.com/fr/outils/generateur-de-politique/remboursement"
#     ]
    
#     for url in urls:
#         fill_form(url, info)

# if __name__ == "__main__":
#     main()
