import selenium
import time
from selenium import webdriver
from selenium.webdriver import ActionChains 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait 
import re
import threading
import sys 
import keyboard 

lecFin = False
prgCnt = 0 

t1 = ''
           
def hunet(driver,id,pw):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ID"))
    )
        
    login_input = driver.find_element_by_id('ID')
    login_input.send_keys(id) 
    
    pw_input = driver.find_element_by_id('PW')
    pw_input.send_keys(pw) 
    
    btn_login = driver.find_element_by_class_name('btn-login')
    btn_login.click()  
    #time.sleep(1)
    print('휴넷 로그인 중.. : '+id)
    mainPage(driver) 

def mainPage(driver):  
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )  
    time.sleep(1)
    print('메인 입장 후 divmain 찾기')
    try:
        div_main = driver.find_element_by_class_name('main-status')
        btn_more = div_main.find_element_by_class_name('btn-more')  
        btn_more.click()
        print('강의실 입장 중.. ')
    except Exception as e: 
        #팝업이 있는 경우 닫기 하는 로직 추가..
        popList = driver.find_elements_by_class_name('cookie_check') 
        for pl in popList:  
            closebtn = pl.find_element_by_class_name('close')
            closebtn.click()
        mainPage(driver)
        
    #time.sleep(1)
     
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dvIngList"))
    ) 
    
    dvList = driver.find_element_by_id('dvIngList')
    count = 0
    
    articles = dvList.find_elements_by_class_name('article')
    print('진행 중인 교육 과정 수 : '+str(len(articles))+'개')
    
    for ar in articles:
        try:
            class_name = ar.find_element_by_class_name('class-name')
            rateStr = str(ar.find_element_by_class_name('graph-bar-type1-wrap').text) 
            rate = re.sub(r'[^0-9]', '', rateStr)
            
            #if class_name.text == '[생생고민톡] 김기리, 윤태진과 함께하는 직장 내 장애인 인식개선 교육':
            if int(rate) < 100:
                btn_start = ar.find_element_by_class_name('ico-ar')
                btn_start.click()
                print('학습 시작 => '+class_name.text+'(키보드 "Ctrl" + "q" 버튼을 누르면 다음 강좌로 넘어갑니다)')
                time.sleep(1)
                startLec(driver) 
        except Exception as e:
            print(e)
            print('학습 중 에러 발생... 다시 시도해주세요')
        finally:
            count+=1 
            
def startLec(driver): 
    if len(driver.window_handles) >1:
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1]) 
        
        try: 
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-primary"))
            )
            
            btn_start = driver.find_element_by_class_name('btn-primary')
            btn_start.click()
        except Exception as e:
            print(e) 
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "goStudy"))
                )
                
                btn_start = driver.find_element_by_class_name('goStudy')
                btn_start.click()
            except Exception as e:
                print(e)
                try:
                    main = driver.window_handles
                    for i in main:
                        if i != main[0]:
                            driver.switch_to.window(i)
                            driver.close()
                            
                    driver.switch_to.window(driver.window_handles[0])
                    
                except:
                    print('자동 수강이 불가능한 강좌 입니다')
            
        #time.sleep(1)
         
        if len(driver.window_handles) >2:
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
            
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert  
                # 확인하기
                alert.accept()
                
            except Exception as e:
                print(e)
            
            #아이프레임으로 들어옴 
            driver.switch_to.frame(driver.find_element_by_id('main')) 
            
            global lecFin
            lecFin = False 
            
            ##백그라운드 키보드 입력  
            daemon = threading.Thread(target=KeyPressSample,args=[driver],daemon=True, name='keystroke')
            daemon.start()
            
            progress_bar()
            
            waitNext(driver)
              
        else:
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print('강의실 입장 실패... 다시 시도하세요')
                
            except Exception as e:
                print(e) 
               
def KeyPressSample(driver,endkey='ctrl+q'): 
    while True:  # making a inifinte loop
        try:
            if keyboard.is_pressed(endkey):
                print('\n강의 수강 완료 다음 강의로 넘어감...')
                main = driver.window_handles
                for i in main:
                    if i != main[0]:
                        driver.switch_to.window(i)
                        driver.close()
                        
                driver.switch_to.window(driver.window_handles[0]) 
                break
        except KeyboardInterrupt:
            print('\nDone Reading input. Keyboard Interupt.')
            break
        except Exception as e:
            print(e)
            break
    
#def progress_bar(current, total, bar_length=50):
def progress_bar(): 
    msg = '********************************* 학습 진행 중 *******************************'
    
    global prgCnt
    if prgCnt > len(msg):
        prgCnt = 0 
        # delete last line
        sys.stdout.write('\x1b[2K')
    else:
        prgCnt+=1
         
    sys.stdout.flush()
    sys.stdout.write("\r" + msg[0:prgCnt])
    
    global lecFin
    if lecFin == False:
        threading.Timer(1, progress_bar).start()  
    
def speedUp(driver):
    #print('speedUp')
    time.sleep(0.2)
    try:
        a = ActionChains(driver) 
        vd = driver.find_element_by_id('video_display')
        
        for i in range(10):
            a.move_to_element(vd).perform()
            spdUp = driver.find_element_by_id('video_dock_spdUp')  
            spdUp.click() 
            time.sleep(0.2)
    except Exception as e:
        print('배속 재생 설정 불가..')

def alertMsgFinalChk(alertMsg): 
    if alertMsg == '본 차시의 학습을 다 하셨습니다' or alertMsg.find('마지막') >=0:
        return True
    else: 
        return False

def waitNext(driver):
    #print('waitNext')
    speedUp(driver)
    try: 
        #print('알람을 위한 대기 걸기')
        WebDriverWait(driver, 4000).until(EC.alert_is_present())
        
        #print('알람을 위한 대기 완료')
        alertNext = driver.switch_to.alert 
        #print('알럿 스위치')
        # 확인하기
        #print(alertNext.text)
        #print('다음 회차 학습 시작')
        alertMsg = str(alertNext.text)
        alertMsg = alertMsg.strip() 
        
        alertNext.accept() 
        #print('알럿 컴펌')
        #print('알럿 메시지 {}'.format(alertMsg))
        #print('알럿 index {}'.format(alertMsg.find('마지막')))
        
        global lecFin
        lecFin = True
        
        if alertMsgFinalChk(alertMsg) :
            print('\n강의 수강 완료 다음 강의로 넘어감...')
            main = driver.window_handles
            for i in main:
                if i != main[0]:
                    driver.switch_to.window(i)
                    driver.close()
                    
            driver.switch_to.window(driver.window_handles[0]) 
        else:
            #print('다음차시... ')
            #print(alertMsg)
            waitNext(driver)
    except Exception as e: 
        print(e)
        print('\n다음 회차 없음 다음 강좌 시작..')
        #global lecFin
        #lecFin = True
        
        main = driver.window_handles
        for i in main:
            if i != main[0]:
                driver.switch_to.window(i)
                driver.close()
                
        driver.switch_to.window(driver.window_handles[0])
        