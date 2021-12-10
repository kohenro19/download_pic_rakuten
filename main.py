import os
import time
import urllib.request
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

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

# def open_csv():
#     pass

# def save_pics()
def main():
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # urls, file_name = open_csv()
    
    driver.get("https://item.rakuten.co.jp/sarasa-designstore/bag/")
    time.sleep(10)
    cnt = 1
    elements = driver.find_elements_by_css_selector('.rakutenLimitedId_ImageMain1-3')
    for element in elements:
        pic_url = element.get_attribute('href')
        # urllib.request.urlretrieve(pic_url, 'test.png')

        file_name = "bag" + "_" + str(cnt) + ".png"
        data = urllib.request.urlopen(pic_url).read()
        with open(file_name, mode="wb") as f:
            f.write(data)

        cnt = cnt + 1

        # 画像用のURLを取得
        
        # 画像を保存
        # save_pics()

if __name__ == "__main__":
    main()