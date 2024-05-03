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
    table_body_element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/main/div/div[5]/table/tbody')))

    # load the list of stablecoin elements
    stablecoins = table_body_element.find_elements(by='xpath', value='./tr')

    # save results
    for c in stablecoins:
        name = c.find_element(by='xpath', value='./td[3]/a/div/div/div').text
        url = c.find_element(by='xpath', value='./td[3]/a').get_attribute('href')
        result[name] = {"url": url, "contracts": {}}
    
    for c in result:
        loadTokenAddresses(c)

    # close browser window
    browser.quit()
    
    # Serializing json
    json_object = json.dumps(result, indent=4)

    # Writing to sample.json
    with open("stablecoins.json", "w") as outfile:
        outfile.write(json_object)

def loadTokenAddresses(coin):

    # avoid being denied from server
    sleep(2)
    
    # load the coin page
    browser.get(result[coin]['url'])
   
    try:
        # wait for the content to be available
        contract_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located(('xpath', '/html/body/div[2]/main/div/div[2]/div[6]/div[5]/div[1]/div/div[2]/div/span/button[1]/div/tag/div/div/span')))
                                                                                                    
        result[coin]['contracts']['main'] = contract_element.get_attribute('data-content')

        # load the list of contracts
        browser.find_element(by='xpath', value='/html/body/div[2]/main/div/div[2]/div[6]/div[5]/div[1]/div/div[2]/div/span/button[2]').click()

        # select all results
        contracts = browser.find_elements(by='xpath', value='/html/body/div[2]/main/div/div[2]/div[6]/div[5]/div[1]/div/div[2]/div/div/div/div/div')
        # contracts.pop()                                 

        # update result dictionnary
        for c in contracts:
            try:
                result[coin]['contracts'][c.find_element(by='xpath', value='./div/div/span').text] = c.find_element(by='xpath', value='./div/div/div/span').get_attribute('data-content')
            except Exception as e:
                print(e)
    
    except Exception as e:
        print("")

if __name__ == "__main__":
    result = {}

    # set options 
    option = webdriver.FirefoxOptions()
    # option.add_argument("--headless")
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0") # Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0
    option.add_argument("window-size=720,1080")

    # create browser
    browser = webdriver.Firefox(options=option)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    main()
