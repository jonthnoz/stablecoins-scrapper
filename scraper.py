import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains, keys

def main():
    # go to CoinGecko stablecoins list page
    browser.get('https://www.coingecko.com/en/categories/stablecoins')

    # wait for the content to be available
    table_body_element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/main/div[8]/div[1]/div[2]/div/table/tbody')))

    # load the list of stablecoin elements
    stablecoins = table_body_element.find_elements(by='xpath', value='./tr')

    # save results
    for c in stablecoins:
        name = c.find_element(by='xpath', value='./td[contains(@class, "py-0")]/div/div[2]/a/span[2]').text
        url = c.find_element(by='xpath', value='./td[contains(@class, "py-0")]/div/div[2]/a').get_attribute('href')
        result[name] = {"url": url, "contracts": {}}
    
    for c in result:
        loadTokenAddresses(c)
    
    for c in result:
        result[c].pop('url')

    # close browser window
    browser.quit()
    
    # Serializing json
    json_object = json.dumps(result, indent=4)

    # Writing to sample.json
    with open("stablecoins.json", "w") as outfile:
        outfile.write(json_object)

def loadTokenAddresses(coin):
    sleep(2)
    
    # load the coin page
    browser.get(result[coin]['url'])
   
    try:
        # wait for the content to be available
        contract_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located(('xpath', '/html/body/div[3]/main/div[@data-controller="coins-information"]/div[3]/div[1]/div/div/div[1]/div/i')))
        result[coin]['contracts']['main'] = contract_element.get_attribute('data-address')

        # load the list of contracts
        browser.find_element(by='xpath', value='/html/body/div[3]/main/div[@data-controller="coins-information"]/div[3]/div[1]/div/div/div[2]').click()

        # select all results
        contracts = browser.find_elements(by='xpath', value='/html/body/div[3]/main/div[@data-controller="coins-information"]/div[3]/div[1]/div/div/div[2]/div/div')
        contracts.pop()

        # update result dictionnary
        for c in contracts:
            try:
                result[coin]['contracts'][c.find_element(by='xpath', value='./div/div[2]/span').text] = c.find_element(by='xpath', value='./i').get_attribute('data-address')
            except Exception as e:
                print(e)
    
    except Exception as e:
        print("")

if __name__ == "__main__":
    result = {}

    # set options 
    option = webdriver.FirefoxOptions()
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0") # Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0

    # create browser
    browser = webdriver.Firefox(options=option)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.set_window_size(720, 1080)

    main()



"""
images :
tbody -> each tr -> div:coin-icon img:source

data :
dans tbody pour chaque tr -> td: py-0 coin-name (class)
1ere div
2e div
a
2e span = ticker

click sur chaque tr -> td: py-0 coin-name (class)
dans div: data-target="coins-information.mobileOptionalInfo"
pour chaque div: data-title "Click to copy", récupérer le data-address = contract

"""


