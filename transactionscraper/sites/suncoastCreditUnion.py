import os.path
import json
import transactionscraper.common.driver as driver
from transactionscraper.common.transaction import Transaction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options


def main():
    transactions = []
    name = "suncoast_creditunion"

    jsonObj = driver.getCredJSON(name, False)
    jsonObj = jsonObj[name]
    username = jsonObj["username"]
    password = jsonObj["password"]

    # Define browser arguments
    options = Options()
    # options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)

    # Load bank details...
    browser.get('https://www.suncoastcreditunion.com/')

    # Handle login process..
    memberNumberElement = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'member-number')))
    memberNumberElement.send_keys(username)

    passwordElement = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'password')))
    passwordElement.send_keys(password)

    rightLoginElement = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'masthead__right-login')))

    loginButton = rightLoginElement.find_element(
        By.CSS_SELECTOR, '.btn[data-submit-url="https://banking.suncoastcreditunion.com/Mfa/index"]')
    loginButton.click()

    # Beyond this point is not tested, errors will probably occur...
    # Navigate to Accounts section..
    navBarElement = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'sectMainNavigationBar')))
    print("Ensure navBarElement - |{}|".format(navBarElement))

    accountsElement = navBarElement.find_element(
        By.CLASS_NAME, 'tile-accounts')
    print("Ensure accountsElement - |{}|".format(accountsElement))
    accountsElement.click()  # Unsure if were able to click divs in this instance

    # Click on >>Details for Smart checking
    # FIXME: Add support for other accounts in this instance
    # FIXME: I doubt this works
    detailsElement = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(By.CSS_SELECTOR, '.a[data-bind="attr: { href: historyUrl() }"]'))
    print("Ensure detailsElement - |{}|".format(detailsElement))
    detailsElement.click()

    # Parse transactions..
    # NOTE: I don't have sufficient html information to parse currently.

    # ????


    driver.updateTransactions(name, transactions)
    browser.quit()


if __name__ == "__main__":
    main()
