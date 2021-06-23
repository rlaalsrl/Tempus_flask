import time
import requests
from bs4 import BeautifulSoup

def getPcode(page):
    pCodeList = []
    for i in range(1,page+1):
        print(i,"페이지 입니다")
        headers = {
               "Referer" : "http://prod.danawa.com/",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
                }

        params = {"page" : page, "listCategoryCode" : 206, "categoryCode" : 206, "physicsCate1":72, 
                  "physicsCate2":73,"physicsCate3":0, "physicsCate4":0, "viewMethod": "LIST", "sortMethod":"BoardCount",
                  "listCount":30, "group": 10, "depth": 2, "brandName":"","makerName":"","searchOptionName":"",
                  "sDiscountProductRate":0, "sInitialPriceDisplay":"N", 
                  "sPowerLinkKeyword":"노트북", "oCurrentCategoryCode":"a:2:{i:1;i:144;i:2;i:206;}", 
                  "innerSearchKeyword":"",
                  "listPackageType":1, "categoryMappingCode":176, "priceUnit":0, "priceUnitValue":0, "priceUnitClass":"",
                  "cmRecommendSort":"N", "cmRecommendSortDefault":"N", "bundleImagePreview":"N", "nPackageLimit":5, 
                  "nPriceUnit":0, "isDpgZoneUICategory": "N", "sProductListApi":"search","priceRangeMinPrice":"","priceRangeMaxPrice":"",
                 "btnAllOptUse":"false"}

        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", headers = headers, data=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll("a", attrs = {"name":"productName"})
        
        for i in range(len(a)):
            pCodeList.append(a[i]['href'][35:-12])
        
    return pCodeList

def danawaCraw(pcode, page):
    reviewlist = []
    for idx in range(1,page+1):
        headers = {"Referer" : "http://prod.danawa.com/info/?pcode=2703774&cate=102206", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        params = {"t" : 0.3180507575057596, "prodCode" : pcode, "page" : idx, "limit":10, "score":0,"usefullScore":"Y", "_":1550639162598}

        res = requests.get("http://prod.danawa.com/info/dpg/ajax/companyProductReview.ajax.php?t=0.3180507575057596&prodCode=2703774&page=1&limit=10&score=0&sortType=&usefullScore=Y&_=1550639162598", headers = headers, params = params)
        soup = BeautifulSoup(res.text, "html.parser")
        divs = soup.find_all("div", attrs = {"style":"display:none;"})
        #print(idx,'페이지에서', len(divs),'개의 리뷰 크롤링완료')
        for i in range(len(divs)):
            reviewlist.append(" ".join(divs[i].text.split()))
        #print('리스트에 리뷰 넣기 완료')
    return reviewlist



review = []

for p in getPcode(3): 
    review.append(danawaCraw(p,5))

print(review)