
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import xlsxwriter
# from webdriver_manager.chrome import ChromeDriverManager

 
# 네이버 쇼핑 검색
# driver = webdriver.Chrome(ChromeDriverManager().install()) 

def productSearch(productname):
    options = Options()
    options.add_argument('headless'); # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드
    
    workbook = xlsxwriter.Workbook("C:/Users/real1/OneDrive/Desktop/Tempus_flask/xlsx/"+productname+'.xlsx')
    worksheet = workbook.add_worksheet()
    excel_row = 1

    worksheet.set_column('A:A', 40) # A 열의 너비를 40으로 설정
    worksheet.set_row(0,18) # A열의 높이를 18로 설정
    worksheet.set_column('B:B', 12) # B 열의 너비를 12로 설정
    worksheet.set_column('C:C', 60) # C 열의 너비를 60으로 설정

    worksheet.write(0, 0, '제품 모델명')
    worksheet.write(0, 1, '가격')
    worksheet.write(0, 2, '링크')




    # webdirver 설정(Chrome, Firefox 등)
    # chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=options) # 브라우저 창 안보이기
    # driver = webdriver.Chrome() # 브라우저 창 보이기
    
    # 크롬 브라우저 내부 대기 (암묵적 대기)
    driver.implicitly_wait(5)
    
    # 브라우저 사이즈
    driver.set_window_size(1920,1280)

    driver.get('https://shopping.naver.com/home/p/index.naver')# 네이버 쇼핑 메인창
    xpath2 = "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div/div[1]/form/fieldset/div[1]/input[1]"
    search = driver.find_element_by_name("query")
    search.clear()
    search.send_keys(productname)
    time.sleep(1)
    search.send_keys("\n")
    time.sleep(2)
    
    # 현재 페이지
    curPage = 1
    
    # 크롤링할 전체 페이지수
    totalPage = 1
    
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
            review_link = v.select_one('div.basicList_title__3P9Q7 > a').get('href')
            print(name,', ', price, ', ', review_link)
            worksheet.write(excel_row, 0, name)
            worksheet.write(excel_row, 1, price)
            worksheet.write(excel_row, 2, review_link)



            driver.get(review_link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_list = soup.select('p.reviewItems_text__XIsTc')
           
            for r in review_list:

                r.text.strip()
                r = str(r)
                r.replace('<br/>','')
                r = re.sub('<.+?>','',r,0).strip()
                print(r)
                worksheet.write(excel_row,3,r)
                print()
            excel_row += 1
            driver.back()
        
        
        time.sleep(5)
        print()
        # 페이지 수 증가
        curPage += 1
    
        if curPage > totalPage:
            print('Crawling succeed!')
            break
    
        # 페이지 이동 클릭
        cur_css = 'a.pagination_next__1ITTf'
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,cur_css))).click()
    
        #2,3페이지까지 확인할경우 과한 리소스 소모+추천 제품에서 멀어져 정확도 감소-> 1페이지만 검색함

        # BeautifulSoup 인스턴스 삭제
        del soup
    
        # 3초간 대기
        time.sleep(3)
    
    # 브라우저 종료
    workbook.close()
    driver.close()    
    

productSearch("노트북")