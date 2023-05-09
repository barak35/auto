import selenium
import requests
import datetime
import zipfile
import getpass
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import hunetStart
import safeedu
import os
 
import AutoUpdate
 
application_path = os.getcwd()

t = ''

def extract(file_name):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(application_path, 'update', 'tmp'))

def autoUpdater():
    MY_API_KEY = "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"
    OWNER = 'barak35'
    REPO = 'auto'
    API_SERVER_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"
    print(API_SERVER_URL)

    res = requests.get(f"{API_SERVER_URL}/releases/latest", auth=(OWNER, MY_API_KEY))  # 
    if res.status_code != 200:
        print(datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 체크 실패")
    print(res.json())
    
    """
    with open("version", "r") as f:
        now_version = f.read()
        if str(res["assets"][0]["id"]) != now_version:
            print("====================")
            print("업데이트 가능 버전을 발견했습니다.")
            print(f'''{res["name"]} / {res["tag_name"]}''')  # 해당 릴리즈의 제목과 태그명을 확인할 수 있음
            print(f'''{res["body"]}''')  # 해당 릴리즈의 내용을 확인할 수 있음
            
            download_url = res["assets"][0]["url"]
            contents = requests.get(download_url, headers={'Accept': 'application/octet-stream'}, stream=True)  # 헤더와 stream을 지정하여 파일을 다운받을 수 있도록 했다.

            os.makedirs(os.path.join(application_path, "update"), exist_ok=True)  # 업데이트할 파일이 겹치지 않도록 update 폴더 생성

            # 다운받은 데이터를 태그명으로 저장
            with open(os.path.join(application_path, 'update', f'''{res["tag_name"]}.zip'''), "wb") as f:
                for chunk in contents.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
    """
    return False
    
def typecheck():
    global t 
    t = input('★ 학습을 원하는 사이트를 선택하세요(1: 휴넷, 2: 산업안전보건교육) : ')
    if t == '1':
        print('\n-> 휴넷으로 로그인 합니다')
        URL= 'https://sisul.hunet.co.kr/Home'
        return URL
    elif t == '2':
        print('\n-> 산업안전보건공단으로 로그인 합니다')
        URL = 'https://www.safetyedu.net/safetyedu'
        return URL
    else:
        print('잘못된 입력입니다.. "1" 또는 "2"만 입력하세요!') 
        typecheck()
        
def main():
    #업데이트 체크.. 
    if autoUpdater() == False:
        return False
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #options.add_argument('headless')

    chromedriver_autoinstaller.install()
    print('\n\n')
    print('******************************** 자동학습 도구 *********************************\n')
    print('(참고) 자동으로 수강이 안되는 교육 과정이 많습니다 \n') 
    URL = typecheck()
    print('   ★ 아이디 / 비밀번호는 로그인을 위한 것으로 저장되지 않습니다\n')
    id = input('  - 아이디를 입력하여주세요 : ')
    pw = getpass.getpass('  - 비밀번호를 입력하여주세요(입력 후 Enter) : ')
    print('\n\n')
    print('*********************** 잠시 후 크롬 브라우저가 실행됩니다. *********************\n')

    driver=''  
    #global t 
    #t='2' 
    #URL= 'https://sisul.hunet.co.kr/Home'
    #URL = 'https://www.safetyedu.net/safetyedu'
    try:
        driver = webdriver.Chrome(options=options)
        
        # 크롬 브라우저 내부 대기 (암묵적 대기)
        driver.implicitly_wait(5)
        
        # 브라우저 사이즈
        driver.set_window_size(1920,1280) 
        driver.maximize_window()
        
    except Exception as e: 
        s = str(e)
        if(s != "'module' object is not callable"):
            print(s)
    finally: 
        if(type(driver) is not str):  
            
            driver.get(url=URL)
            if t == '1':
                hunetStart.hunet(driver,id,pw)  
                os.system("pause")
            elif t == '2': 
                safeedu.safeedu(driver,id,pw)  

if __name__ == "__main__":
    main()