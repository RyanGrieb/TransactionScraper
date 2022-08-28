import os.path
import json
import driver
from transaction import Transaction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

def main():
    transactions = []
    name = "broadway_bank"

    jsonObj = driver.getCredJSON(name, True)
    jsonObj = jsonObj[name]
    username = jsonObj["username"]
    password = jsonObj["password"]

    # Define browser arguments
    options = Options()
    #options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)

    # Load bank details...
    browser.get('https://digital.broadway.bank/SignIn.aspx')
    username_element = browser.find_element(
        By.ID, 'M_layout_content_PCDZ_MMCA7G7_ctl00_webInputForm_txtLoginName')

    password_element = browser.find_element(
        By.ID, 'M_layout_content_PCDZ_MMCA7G7_ctl00_webInputForm_txtPassword')

    login_element = browser.find_element(
        By.ID, 'M_layout_content_PCDZ_MMCA7G7_ctl00_webInputForm_cmdContinue')

    username_element.send_keys(username)
    password_element.send_keys(password)

    login_element.click()


# Check URL if website is asking us to save this device...
# https://digital.broadway.bank/RememberDevice.aspx
    if browser.current_url == 'https://digital.broadway.bank/RememberDevice.aspx':
        # print('Remember this browser...')
        save_element = browser.find_element(
            By.ID, 'M_layout_content_PCDZ_M4HNZU6_ctl00_webInputForm_btnSave')
        save_element.click()

    browser.get('https://digital.broadway.bank/AccountActivity.aspx?a=1')

    # Get available & current bank balance
    header_buttons_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='account-activity-header buttons']")))

    balance_div_elements = header_buttons_element.find_element(
        By.TAG_NAME, 'div').find_elements(By.XPATH, './/*')

    # Initialize bank balance variables
    balance_type = None
    for balance_div_element in balance_div_elements:
        sub_balance_div_elements = balance_div_element.find_elements(
            By.XPATH, './/*')
        for sub_balance_div_element in sub_balance_div_elements:

            if sub_balance_div_element.get_attribute('class') == 'account-nickname':
                balance_type = sub_balance_div_element.text

            if sub_balance_div_element.get_attribute('class') == 'account-balance':
                if balance_type == 'Available Balance':
                    bank_available_balance = float(sub_balance_div_element.text.replace(
                        '$', '').replace(',', ''))
                if balance_type == 'Current Balance':
                    bank_current_balance = float(sub_balance_div_element.text.replace(
                        '$', '').replace(',', ''))

    # Parse bank transactions
    grid_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "customGrid")))

    tbody_element = grid_element.find_element(By.TAG_NAME, 'tbody')
    tr_elements = tbody_element.find_elements(By.TAG_NAME, 'tr')

    for tr_element in tr_elements:
        desc_element = tr_element.find_element(By.CLASS_NAME, 'description')
        date_element = tr_element.find_element(
            By.CLASS_NAME, 'date').find_element(By.TAG_NAME, 'span')
        amount_element = tr_element.find_element(
            By.CLASS_NAME, 'amount').find_element(By.TAG_NAME, 'span')

        amount = amount_element.text.replace('$', '').replace(',', '')
        transaction = Transaction(
            date_element.text, desc_element.text, float(amount), 'Bank')
        transactions.append(transaction)
        print(transaction)
    
    driver.updateTransactions(name, transactions)
    browser.quit()


if __name__ == "__main__":
    main()
