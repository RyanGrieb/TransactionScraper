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
    name = "cardmember_service"

    jsonObj = driver.getCredJSON(name, True)
    jsonObj = jsonObj[name]
    username = jsonObj["username"]
    password = jsonObj["password"]

    # Define browser arguments
    options = Options()
    #options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    browser.get('https://www.myaccountaccess.com/onlineCard/login.do')

    username_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'userId')))
    username_element.send_keys(username)

    next_btn_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'nextButton')))
    next_btn_element.click()

    print(browser.current_url)
    # TODO: Implement try exception if this page doens't show up

    # time.sleep(2)

    question_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'challengeQuestion')))

    answer = driver.getSecurityQuestionAnswer(jsonObj, question_element.text)
    # print(answer)

    answer_input_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'answer')))
    answer_input_element.send_keys(answer)

    login_btn_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'loginButton')))
    login_btn_element.click()

    password_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'loginPassword0')))
    password_element.send_keys(password)

    login_btn_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'loginButton')))
    login_btn_element.click()

    # Get card balance
    cc_balance_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'summaryValue')))
    cc_balance_span_element = cc_balance_element.find_element(
        By.TAG_NAME, 'span')

    cc_balance = float(cc_balance_span_element.text.replace(
        '$', '').replace(',', ''))

    # Get card credit
    cc_credit_div_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'account-available-credit-subtext')))

    cc_credit_element = cc_credit_div_element.find_element(
        By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span')

    cc_credit = float(cc_credit_element.text.replace(
        '$', '').replace(',', ''))

    table_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'transactionDetailTable_completed')))

    tbody_element = table_element.find_element(By.TAG_NAME, 'tbody')
    tr_elements = tbody_element.find_elements(By.TAG_NAME, 'tr')

    for tr_element in tr_elements:

        if not tr_element.is_displayed():
            continue

        desc_element = tr_element.find_element(By.CLASS_NAME, 'descCol')
        date_element = tr_element.find_element(
            By.CLASS_NAME, 'tranDateCol_resp')
        amount_element = tr_element.find_element(
            By.CLASS_NAME, 'amountCol_resp').find_element(By.TAG_NAME, 'span')

        amount = float(amount_element.text.replace('$', '').replace(',', ''))

        # Note: For my credit card, we need to flip positive numbers to negative to match my bank...
        amount = -amount

        transaction = Transaction(
            date_element.text, desc_element.text, amount, 'Credit Card')
        transactions.append(transaction)
        print(transaction)

    driver.updateTransactions(name, transactions)
    browser.quit()

if __name__ == "__main__":
    main()
