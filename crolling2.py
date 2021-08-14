
    # url = "https://www.naver.com/"
    # res = requests.get(url)
    # res.raise_for_status()
    # soup = BeautifulSoup(res.text,"lxml")
    # print(soup.text)
    # print(soup.title)
    # browser = webdriver.Chrome("D:/python/priconne/chromedriver.exe")
    # browser.get(url)
    # #파이썬은 코드가 끝난 후 모든 리소스를 정리하기에 뒤에 추가 코드가 없으면 꺼짐
    # print("test")

# pip install selenium
# pip install chromedriver-autoinstaller 
# pip install bs4
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
 
# 다나와 사이트 검색
 
options = Options()
options.add_argument('headless'); # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드
 
# webdirver 설정(Chrome, Firefox 등)
# chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=options) # 브라우저 창 안보이기
# driver = webdriver.Chrome() # 브라우저 창 보이기
 
# 크롬 브라우저 내부 대기 (암묵적 대기)
driver.implicitly_wait(5)
 
# 브라우저 사이즈
driver.set_window_size(1920,1280)
 
# 페이지 이동(열고 싶은 URL)
driver.get('https://search.shopping.naver.com/search/category?catId=50000151')
 
# 페이지 내용
# print('Page Contents : {}'.format(driver.page_source))
 
# # 제조사별 검색 (XPATH 경로 찾는 방법은 이미지 참조)
# mft_xpath = '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'
# WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,mft_xpath))).click()
 
# # 원하는 모델 카테고리 클릭 (XPATH 경로 찾는 방법은 이미지 참조)
# model_xpath = '//*[@id="selectMaker_simple_priceCompare_A"]/li[16]/label'
# WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,model_xpath))).click()
 
# 2차 페이지 내용
# print('After Page Contents : {}'.format(driver.page_source))
 
# 검색 결과가 렌더링 될 때까지 잠시 대기
time.sleep(2)
 
# 현재 페이지
curPage = 1
 
# 크롤링할 전체 페이지수
totalPage = 6
 
while curPage <= totalPage:
    #bs4 초기화
    soup = BeautifulSoup(driver.page_source, 'html.parser')
 
    # 상품 리스트 선택
    goods_list = soup.select('li.basicList_item__2XT81')
 
    # 페이지 번호 출력
    print('----- Current Page : {}'.format(curPage), '------')
 
    for v in goods_list:
        # 상품명, 가격, 이미지
        
        name = v.select_one('div.basicList_title__3P9Q7 > a').text.strip()
        price = v.select_one('span.price_num__2WUXn').text.strip()
        print(name,', ', price)
        
        review_link = v.select_one('div.basicList_title__3P9Q7 > a').get('href')
        # print(review_link)
        # # print(v.select_one('p.price_sect > a').get('href'))
        driver.get(review_link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # test = soup.select('p.tit')
        # print(test)
        review_list = soup.select('p.reviewItems_text__XIsTc')
        # if review_list.find("<br>") != -1:
        #     review_list = review_list.replace("<br>","\n")
        # print(review_list)
        for r in review_list:
            # if r.find('<br/>') != -1:
            #     r.replace('<br/>','\n')
            r.text.strip()
            r = str(r)
            r.replace('<br/>','')
            r = re.sub('<.+?>','',r,0).strip()
            print(r)
            print()
        # review = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[2]/div[4]/div[4]/div/div[3]/div[2]/div[2]/div[2]/ul/li[2]/div[2]/div[1]/div[2]')
        # print(review)
        #     # text = v.select_one('danawa-prodBlog-companyReview-content-wrap-0 > div.rvw_atc > div.atc_cont > div.atc').text.strip()
        #     # print(text)
        driver.back()
    time.sleep(5)

#다나와 내 외부 리뷰는 크롤링이 차단되어 있는것으로 보임
    print()
 
    # 페이지 수 증가
    curPage += 1
 
    if curPage > totalPage:
        print('Crawling succeed!')
        break
 
    # 페이지 이동 클릭
    cur_css = 'a.pagination_next__1ITTf'
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()
 
    # BeautifulSoup 인스턴스 삭제
    del soup
 
    # 3초간 대기
    time.sleep(3)
 
# 브라우저 종료
driver.close()    
 

