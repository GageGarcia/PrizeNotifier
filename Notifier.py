from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from twilio.rest import Client
from selenium.webdriver.chrome.options import Options

CUTOFF = 60
SLEEP_SECS = 300

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Set up Twilio client
account_sid = ""
auth_token = ""
twilio_client = Client(account_sid, auth_token)
my_phone_number = '6509960037'  # replace with your phone number

username = ""
password = ""

last_val = 0.0
# Create webdriver

while True:

  try:
    #login
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://dgfantasy.com/login-2/")

    driver.find_element(By.ID, "user_login").send_keys(username)
    driver.find_element(By.ID, "user_pass").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input[type=\"submit\"]").click()

    #get to pp website
    driver.get("https://dgfantasy.com/all-sports-prizepicks-optimizer/")

    time.sleep(7)

    #find top score, text it
    testFirst = driver.find_elements(
      By.CLASS_NAME, "ninja_clmn_nm_pct_avg_odds_adj_balanced")
    try:
      if (float)(testFirst[1].text) > CUTOFF and (float)(
          testFirst[1].text) != last_val:
        message = twilio_client.messages.create(body="PRIZEPICKS ALERT: " +
                                                testFirst[1].text,
                                                from_="+18886106208",
                                                to="+16509960037")
       
        time.sleep(SLEEP_SECS)
        last_val = (float)(testFirst[1].text)
    except:
      print("BUG")

  finally:
    # Clean up resources

    driver.quit()
    time.sleep(5)
