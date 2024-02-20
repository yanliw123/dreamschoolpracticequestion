import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_chn_name(currency_code):
    if currency_code == "HKD ":
        return "港币"
        # Corner case: 在https://www.11meigui.com/tools/currency 对照表里 HKD 对应的是 港元
        # 在https://www.boc.cn/sourcedb/whpj/ 外汇牌价网站里用到的是 港币
        
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://www.11meigui.com/tools/currency")
        
        # Find currency code
        currency_code_elements = driver.find_element(By.XPATH,"//td[text()='{0}']".format(currency_code))
        #print(f"cur code is {currency_code_elements.text}")
        
        # Find correspond chinese name
        chinese_currency_name = currency_code_elements.find_element(By.XPATH,"preceding-sibling::td[3]").text
        #print(f"get chn name {chinese_currency_name}")
        
        return chinese_currency_name
    
    except Exception as e:
        print(f"Unable to find correspond chinese currency name with error {str(e)}")
        return None
    
    finally:
        driver.quit()
        
        
        
def get_forex_rate(date, chn_code):
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # Input date to 结束时间
        end = driver.find_element(By.CSS_SELECTOR, "input[name='nothing']")
        end.clear()
        end.send_keys(date)

        #print("Date fields inputted successfully.")
        
        # Find dropdown and open
        currency_select = driver.find_element(By.ID,"pjname")
        currency_select.click()

        # Find the option corresponding to the currency code
        currency_option = driver.find_element(By.XPATH, f"//select[@id='pjname']/option[text()='{chn_code}']")
        currency_option.click()

        #print("Currency code inputted successfully.")

        # Click the search button
        search_button = driver.find_element(By.CSS_SELECTOR, "[onclick='executeSearch()']")
        search_button.click()

        # Find 现汇卖出价
        currency_col = driver.find_element(By.XPATH,f"//td[contains(text(), '{chn_code}')]")
        xh = currency_col.find_element(By.XPATH,"following-sibling::td[3]").text


        # Write the result to result.txt
        with open("result.txt", "w", encoding="utf-8") as file:
            file.write(xh)

        return xh

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 practice.py <date> <currency_code>")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2] + " "
    chn_code = get_chn_name(currency_code)
    xh = get_forex_rate(date, chn_code)
    """
    if xh:
        print(f"现汇卖出价 for {date} and currency {chn_code} is: {xh}")
    """