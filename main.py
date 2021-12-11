import os
import time
import urllib.request
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


df_log = None
df_log = pd.DataFrame(columns=['URL', 'リネーム品番'])
    
def open_csv():
    df = pd.read_csv('rakuten.csv')
    return df.URL, df.リネーム品番

def write_log(url, error_message):
    global df_log
    df_log = df_log.append({'URL': url, 'リネーム品番': error_message},ignore_index=True)
    df_log.to_csv('output.csv', mode="w")
         
def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
          options = ChromeOptions()
    else:
      options = Options()

    # ヘッドレスモード（画面非表示モード）を設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path,options=options)
    else:
        return Firefox(executable_path=os.getcwd()  + "/" + driver_path,options=options)


# def save_pics()
def main():
    urls, rename_files = open_csv()
    
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # urls, file_name = open_csv()
    

    for url, rename_file in zip(urls, rename_files):
        try:
            driver.get(url)
            time.sleep(10)
            cnt = 1
            elements = driver.find_elements_by_css_selector('.rakutenLimitedId_ImageMain1-3')
            for element in elements:
                pic_url = element.get_attribute('href')
                file_name = rename_file + "_" + str(cnt) + ".png"
                data = urllib.request.urlopen(pic_url).read()
                with open(file_name, mode="wb") as f:
                    f.write(data)
                time.sleep(1)
                cnt = cnt + 1
            write_log(url, rename_file)
        except:
            write_log(url, "error")        

if __name__ == "__main__":
    main()
