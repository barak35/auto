import selenium
import requests
import datetime 
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
 
import shutil
 
application_path = os.getcwd()

t = '' 

def autoUpdater():
    print('업데이트 버전 확인...')
    
    MY_API_KEY = "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"
    OWNER = 'barak35'
    REPO = 'auto'
    API_SERVER_URL = f"https://api.github.com/repos/{OWNER}/{REPO}" 

    res = requests.get(f"{API_SERVER_URL}/releases/latest", auth=(OWNER, MY_API_KEY))  # 
    if res.status_code != 200:
        print(datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 체크 실패") 
        return False
    
    dataJson = res.json()
    
    try:
        v = open("version","r")
    except:
        #파일이 없으니 새로 작성..
        v = open("version","w")
        v.write(str(dataJson['assets'][0]["id"]))
        v.close()
    
    with open("version", "r") as f:
        now_version = f.read() 
        if str(dataJson['assets'][0]["id"]) != now_version:
            print("====================")
            print("업데이트 가능 버전을 발견했습니다.")
            print(f'''{dataJson["name"]} / {dataJson["tag_name"]}''')  # 해당 릴리즈의 제목과 태그명을 확인할 수 있음
            print(f'''{dataJson["body"]}''')  # 해당 릴리즈의 내용을 확인할 수 있음
    
            download_url = dataJson['assets'][0]["url"] 
            contents = requests.get(download_url, headers={'Accept': 'application/octet-stream'}, stream=True)  # 헤더와 stream을 지정하여 파일을 다운받을 수 있도록 했다.

            os.makedirs(os.path.join(application_path, "update"), exist_ok=True)  # 업데이트할 파일이 겹치지 않도록 update 폴더 생성

            # 다운받은 데이터를 태그명으로 저장
            with open(os.path.join(application_path, 'update', f'''auto_{dataJson["tag_name"]}.exe'''), "wb") as f:
                for chunk in contents.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
            
            shutil.copytree(os.path.join(application_path, "update"), application_path, ignore=shutil.ignore_patterns("update-check.exe",), dirs_exist_ok=True)  # update/tmp에 압축해제된 데이터를 루트에 복사하며, update-check.exe는 복사하지 않음

            # 새로운 버전을 입력해 줌
            with open(os.path.join(application_path, "version"), "w") as f:
                f.write(str(dataJson["assets"][0]["id"]))

            shutil.rmtree(os.path.join(application_path, "update"))  # 업데이트 임시 폴더 삭제

            print(datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "업데이트 완료")

            os.startfile(os.path.join(application_path, f'auto_{dataJson["tag_name"]}.exe'))  # 업데이트 완료 후 메인 프로그램을 다시 실행시켜줌
            return True
    
    print('최신 버전 입니다!')
    return True
    
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
        return
    
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