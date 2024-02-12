from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sys
from datetime import datetime  
import requests
import re
from urllib.parse import quote


def sendToTelegram(productLink, title, image, price, strikeOffPrice):
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '1809369384:AAFU7ZebkbMRhtQOUZRn4dw-fafjdU8sh9c'
    # Replace 'YOUR_CHAT_ID' with your group chat ID
    chat_id = '@deals_dhamaka_india'
    # Encode the URI
    uri = f"chat_id={chat_id}&text=\n\n🌟{title}"
    # url = f"https://www.amazon.com/dp/{productId}/?tag={storeId}"
    productLink = f"{productLink}?tag=gadgetswareho-21"
    ur = f"chat_id={quote(chat_id)}&photo={quote(image)}&caption=\n\n🌟 {quote(title)}\n\n✅ ₹{quote(price)}\n\n❌ ₹{quote(strikeOffPrice)}\n\n🛒 [Buy Link]({productLink})&parse_mode=Markdown"
    # Construct the URL
    # url = f"https://api.telegram.org/bot{bot_token}/sendMessage?{encoded_uri}"
    curl_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto?{ur}"
    # Make the request
    response = requests.get(curl_url)



def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print(current_time, ':',  message, flush=True)

app = Flask(__name__)



firefox_options = webdriver.FirefoxOptions()
# firefox_options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
# # Disable images
# firefox_options.set_preference('permissions.default.image', 2)

# Disable Flash
firefox_options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

# Disable hardware acceleration
firefox_options.set_preference('layers.acceleration.disabled', 'true')

# Disable browser animations
firefox_options.set_preference('toolkit.cosmeticAnimations.enabled', 'false')

# Disable smooth scrolling
firefox_options.set_preference('general.smoothScroll', 'false')
firefox_options.set_preference('layout.css.scroll-behavior.enabled', 'false')

# Disable prefetching
firefox_options.set_preference('network.prefetch-next', 'false')

# Disable safe browsing
firefox_options.set_preference('browser.safebrowsing.enabled', 'false')
firefox_options.set_preference('browser.safebrowsing.malware.enabled', 'false')

# Reduce history entries
firefox_options.set_preference('places.history.enabled', 'false')
firefox_options.set_preference('browser.sessionhistory.max_entries', 10)

# Disable geolocation
firefox_options.set_preference('geo.enabled', 'false')

# Disable auto-update
firefox_options.set_preference('app.update.auto', 'false')
firefox_options.set_preference('app.update.enabled', 'false')

# Disable Firefox telemetry
firefox_options.set_preference('toolkit.telemetry.reportingpolicy.firstRun', 'false')
firefox_options.set_preference('datareporting.healthreport.uploadEnabled', 'false')

# Disable Firefox welcome page
firefox_options.set_preference('browser.startup.homepage_override.mstone', 'ignore')

firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--disable-dev-shm-usage')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('--disable-web-security')
firefox_options.add_argument("--disable-features=SameSiteByDefaultCookies")
firefox_options.add_argument("--disable-features=SameSiteDefaultChecksForLocalhost")

def extract_product_id(url):
    # Regular expression pattern to match ASIN (Amazon Standard Identification Number)
    pattern = r'/([A-Z0-9]{10})(?:[/?]|$)'
    
    # Find the match in the URL
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  # Return the matched ASIN
    else:
        return None  # Return None if no match found


def scrap(url) :
    driver = webdriver.Firefox(options=firefox_options)
    log("AFTER SETTING DRIVER =>")
    try:
        driver.get(url)
        log("AFTER LOADING WEBSITE =>" + url)
        productTitleElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@id='productTitle']")))
        productTitle = productTitleElement.text
        
        productDescriptionElement = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@id='featurebullets_feature_div']//li//span")))

        # description = []
        # for element in productDescriptionElement:
        #     description.append(element.text)
        #     print(element.text)

        priceElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"]')))

        strikeOffPriceElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="corePriceDisplay_desktop_feature_div"]//*[@class="a-price a-text-price"]')))
    
        price = priceElement.text + '.00'
        print(price)
        strikeOffPrice = re.sub('\\W+', '', strikeOffPriceElement.text) + '.00'
        print(strikeOffPrice)

        imageElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='main-image-container']//img[@id='landingImage']")))

        image = imageElement.get_attribute("src")
        print(image)

        productId = extract_product_id(url)
        sendToTelegram(url, productTitle, image, price, strikeOffPrice)


    except Exception as e:
        return print("ERROR ===>", str(e))  
    finally:
        log("QUIT THE DRIVER")
        driver.quit()

# GET method to fetch all books
@app.route('/', methods=['GET'])
def get():
    try:
        url = request.args.get('url')
        scrap(url)
        return jsonify({"status": 200})
    except Exception as e:
        return jsonify({"status": 400, "error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)

