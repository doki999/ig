from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
#import re

#p = re.compile('^(https?://)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_/.?=]*')

# 네이버 이미지 검색결과 URL을 baseUrl 변수에 저장한 후,
# plusUrl에 사용자 검색을 입력받고, baseUrl과 plusUrl를 더하여 url 변수에 저장한다.
#baseUrl = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query='
baseUrl = 'https://www.javbus.com'
plusUrl = input('품번을 코드를 입력하세요. ') +'-'
plusUrl_s = input('품번 시작을 입력하세요. ')
plusUrl_e = input('품번 종료를 입력하세요. ')

n_start = int(plusUrl_s)
for i in range(int(plusUrl_s), int(plusUrl_e)+1):
    url = baseUrl + '/' + quote_plus(plusUrl+str(n_start).zfill(3))
    print(url) 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    #headers = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=headers)

    cookie_handler = urllib.request.HTTPCookieProcessor()
    https_handler = urllib.request.HTTPSHandler()
    opener = urllib.request.build_opener(cookie_handler, https_handler)
    response = opener.open(url)    

    try:
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')

            img2 = soup.find(class_='bigImage') 
            img2_Url = (baseUrl + img2.attrs['href'])
            req2 = Request(img2_Url,headers=headers)
            with urlopen(req2) as img_f:
                with open('./img/' + plusUrl+str(n_start).zfill(3) + '.jpg', 'wb') as img_h:
                    req2 = img_f.read()
                    img_h.write(req2)
            #n_start+=1
            print(img2_Url)        
    
            n = 1
            img = soup.find_all(class_='sample-box') 
            for i in img:
                #print(i.string)
                imgUrl = i.attrs['href']
                #print(img_Url)
                if imgUrl.find('http') < 0 :
                    imgUrl = baseUrl  + imgUrl
                req1 = Request(imgUrl,headers=headers)
                with urlopen(req1) as f:
                    with open('./img/' + plusUrl+str(n_start).zfill(3) + '_(' + str(n) + ')' + '.jpg', 'wb') as h:
                        img = f.read()
                        h.write(img)  
                    n += 1
                    #print(imgUrl)
            
            n_start+=1
    except :
           # err = e.read()
           # code = e.getcode()
            n_start+=1
            pass
            
print('다운로드 완료')
