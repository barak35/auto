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

lecFin = False
prgCnt = 0 
isLast = False
curTime = ''
reCount =0
import sys 

def safeedu(driver,id,pw): 
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userId"))
        )
        
        login_input = driver.find_element_by_id('userId')
        login_input.send_keys(id) 
        
        pw_input = driver.find_element_by_id('pwd')
        pw_input.send_keys(pw)
        
        links = driver.find_elements_by_tag_name('a')
        for a in links: 
            btnLogin = a.get_attribute('data-action')
            if btnLogin == 'login':
                a.click() 
                gohome(driver)
                break
    except Exception as e:
        print(e)
    
def gohome(driver): 
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "myinfo"))
        ) 
        home = driver.find_element_by_class_name('myinfo')
        home.click()
        lecList(driver)
    except Exception as e:
        print(e)

def lecList(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item-class"))
        ) 
        
        lecList = driver.find_elements_by_class_name('item-class')
        for l in lecList:
            title = l.find_element_by_class_name('item-title').text
            rate = int(l.find_element_by_class_name('progressbar').get_attribute('data-percent'))  
            if(rate<100):
                print(title) 
                goButton = l.find_element_by_class_name('btn-action.deposit') 
                goButton.click()
                lectHome(driver)
                break
            
    except Exception as e:
        print(e)
    
def lectHome(driver):
    try:
        #대리수강방지 팝업
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.ID, 'pop-study-certify'))
        ) 
        popAgree = driver.find_element_by_id('pop-study-certify')
         
        chk = popAgree.find_element_by_id('chk_substituteAgree') 
        chk.click()
        
        #driver.switch_to.new_window('window')
        bs = popAgree.find_elements_by_tag_name('button')
        for a in bs:  
            btn = a.get_attribute('data-button')
            if btn == 'agree':
                a.click()  
                classroom(driver)
                break
        
    except Exception as e:
        classroom(driver) 
        
def classroom(driver):
    #print('classroom')
    WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'classroom'))
        )
     
    #진도율 갱신 
    tbody = driver.find_element_by_class_name('tbody')
    tList = tbody.find_elements_by_class_name('tr')
    count = 1
    global isLast
    
    for list in tList:
        tds = list.find_elements_by_class_name('td')  
        rateStr = str(tds[2].text)
        if rateStr == '완료':
            rate = 100 
        else:
            rate = int(re.sub(r'[^0-9]', '', rateStr))
        
        if(rate <100):
            #클래스룸타이틀
            print(tds[1].text+' => 강의실 입장..') 
            #버튼
            b = (tds[7].find_element_by_tag_name('button'))
            b.click() 
            if len(tList) <= count: 
                isLast = True
            else:
                isLast = False
                 
            #print('isLast : '+str(isLast))
            startLec(driver)
            break
            #WebDriverWait.until(EC.number_of_windows_to_be(1)) 
    
        count +=1
        
def startLec(driver): 
    #print('startLec')
    if len(driver.window_handles) >1:
        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])  
        global lecFin
        lecFin = False
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ebody"))
            )
            
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element_by_id('ebody'))  
    
            
            #print('videoView start')
            videoView(driver)
            
        except Exception as e:
            try:
                vdoMain = driver.find_element_by_id('myVideoContainer')
                print(vdoMain.text)
                vdo = vdoMain.find_element_by_class_name('play')
                vdo.click()
                videoView2(driver)
            except Exception as e2:
                print(e2)
                lecFin = True
                sys.stdout.flush()
                 
            print(e) 

def question(driver):  
    try:
        driver.switch_to.frame(driver.find_element_by_id('loadActFrame'))  
          
        mun = driver.find_element_by_id('quizContainer')
        
        #인풋 입력하고... 
        try:
            inputarea = driver.find_element_by_class_name('mun_sub_area') 
            #print(mun.text)
            pre_input = inputarea.find_elements_by_class_name('pre_input_txt')
            #print(pre_input)
            inputData = ''
            for i in pre_input:
                inputData += i.text
            
            inputData = inputData.replace("\n", "")
            if inputData == '':
                inputData = 'ㄱㄴㄷㄹㅁ'
       
        except Exception as e:
            inputData = 'ㄱㄴㄷㄹㅁ'
            sys.stdout.flush()
            
        try:   
            inp = driver.find_element_by_class_name('input_txt')   
            inp.send_keys(inputData) 
        except Exception as e:
            sys.stdout.flush()
                
         
        #startdiv 클릭
        try: 
            inputarea = driver.find_element_by_id('startBtnArea') 
            inputarea.click()
        except:
            sys.stdout.flush()  
         
        #버튼 클릭스... 
        buttons = mun.find_elements_by_tag_name('button')
        for ab in  buttons: 
            ab.click()

        defaultFrame(driver)

    except Exception as e: 
        defaultFrame(driver)
        sys.stdout.flush() 

def defaultFrame(driver):
    #driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])  
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_id('ebody')) 
    except:
        sys.stdout.flush() 
        
    
def forcePlayVideo(driver): 
    try:
        pBtn = driver.find_element_by_id('playBtn')
        pBLabel= pBtn.get_attribute('class')  
        if pBLabel == 'controlSet controlBtn': 
            pBtn.click()
            
    except: 
        sys.stdout.flush() 
        
    #3회 이상 멈춰있을경우 강제로 플레이버튼 누름   
    global curTime
    global reCount
    #print(curTime)
    if curTime == '00:00':
        reCount+=1
    else:
        reCount =0
    
    #3회 걸림
    if reCount >=3:
        try:
            pBtn = driver.find_element_by_id('playBtn') 
            reCount = 0
            pBtn.click() 
        except: 
            sys.stdout.flush() 
            
   # print(reCount)
   
def newLect(driver):
    global lecFin  
    lecFin = True
    main = driver.window_handles
    #print(main)
    for i in main:
        if i != main[0]:
            driver.switch_to.window(i)
            #print(i)
            driver.close()
            #print('닫기 완료')
            
    driver.switch_to.window(driver.window_handles[0]) 
    #print('스위칭 완료')
    time.sleep(2) 
    global isLast
    #print('isLast : '+str(isLast))
    if isLast: 
        time.sleep(1)
        print('\n강의 수강 완료 다음 강의로 넘어감...')
        topMn = driver.find_element_by_id('topMenuUl') 
        alist = topMn.find_elements_by_tag_name('a')
        #print(alist)
        for a in alist:
            btn = a.text
            if btn == '나의강의실':  
                a.click()
                lecList(driver) 
                break 
    else:
        classroom(driver)
        
def videoView2(driver):
    global lecFin 
    
    try:
        wid = str(driver.find_element_by_class_name('ui-slider-range').get_attribute('style'))
        sIdx = wid.find('width: ')
        eIdx = wid.find(';')
        tStr = wid[sIdx:eIdx]
        tStr = tStr.replace('width: ','')
        #print(tStr)
        tStrFin = tStr[0:tStr.find('.')] 
    except:
        sys.stdout.flush()
            
    loadingMsg()
    
    if int(tStrFin) >=100:
        newLect(driver) 
    
    if lecFin == False:
        threading.Timer(1, videoView2,args=[driver]).start() 
        
def loadingMsg():
    msg = '―＼｜／―＼｜／―'
    
    global prgCnt
    if prgCnt >= len(msg)-1:
        prgCnt = 0 
        # delete last line
        sys.stdout.write('\x1b[2K')
    else:
        prgCnt+=1
         
    sys.stdout.flush()
    sys.stdout.write("\r" + msg[prgCnt])
    
            
def videoView(driver):
    forcePlayVideo(driver)
    defaultFrame(driver) 
    global lecFin  
    
    loadingMsg()
    
    #print('Q스타트...')
    question(driver)
    
    #마지막 체크..
    try: 
        #print('마지막 체크')
        #print(driver.window_handles)
        pageNum = driver.find_element_by_id('pageNum')
        totNum = pageNum.find_element_by_id('totalNum').text
        currentNum = pageNum.find_element_by_id('currentNum').text
        #print('pageNum {},{},{}'.format(pageNum.text,totNum,currentNum))
         
        timeStr = driver.find_element_by_id('time').text
        #print(timeStr)
        global curTime
        totTime = timeStr.split('/')[1].strip()
        curTime = timeStr.split('/')[0].strip()
         
        if totNum == currentNum:
            if totTime == curTime:
                newLect(driver)
        
    except Exception as e:
        print(e)
        sys.stdout.flush()
        
    #넥스트 버튼 누르기
    try: 
        next = driver.find_element_by_id('nextBtn')
        next.click()
    except Exception as e:
        sys.stdout.flush() 
    
    if lecFin == False:
        threading.Timer(1, videoView,args=[driver]).start()