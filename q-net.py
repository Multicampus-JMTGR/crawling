import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 정규표현식 사용하기 위한 라이브러리
import re

# 큐넷 URL
url = 'http://www.q-net.or.kr/crf005.do?id=crf00501&gSite=Q&gId='
# 응답 받기
response = requests.get(url)
# 응답 코드 확인
html = response.text
#print(html)
# 뷰티풀숩 사용하여 parser하기
soup = BeautifulSoup(html, 'html.parser')
# 메인 자격증 이름 & 메인 자격증 각각 가지고 있는 param 값을 가져오기 위한 selector tag
all_certificate = soup.select('#content > div.content > div:nth-child(4) > .tab_lc_group > ul > li > a')
# 모든 정보를 담을 list
main_list = []
for main_name in all_certificate:
    certificate_dict = {}
    # <a href="#" onclick="getList('1','0','146')" => param값인 맨 마지막 숫자 146을 가져오기 위한 정규표현식 적용
    regex = re.search(r'(\d+){3}', str(main_name))
    #print(regex.group())
    # 메인 자격증 이름 dict 저장
    certificate_dict['certificate_main_name'] = main_name.text
    # 메인 자격증 param값 dict 저장
    certificate_dict['param'] = regex.group()
    # (param값을 조합해 가져온) 서브 자격증 정보가 있는 URL을 dict에 저장
    param_join_url = 'http://www.q-net.or.kr/crf005.do?id=crf00501s01&gSite=Q&gId=&div=1&obligFldCd={}'.format(
        regex.group())
    certificate_dict['param_join_url'] = param_join_url
    # 서브 자격증 정보가 있는 URL로 다시 요청을 보내 정보를 가져옴
    response = requests.get(param_join_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # 서브자격증 이름 및 각 페이지 URL을 가져오기 위한 selector tag
    sub_certificate = soup.select('li > a')
    sub_list = []
    for sub in sub_certificate:
        sub_list.append(sub.text)
    # 메인자격증 정보가 있는 곳에 서브자격증 이름을 list로 저장하여 dict에 저장
    certificate_dict['sub_name'] = sub_list
    # 각 자격증의 정보가 들어있는 dict들을 list에 저장
    main_list.append(certificate_dict)
print(main_list)

'''
param 값이란: 
메인 자격증 클릭 시 서브자격증을 조회하는 부분을 js(getList 함수로 정의됨)로 뿌려줌 
-> 파라미터로 dev, index, parm값을 전달해주는데 parm값을 통해 구분 가능. 
-> 서브페이지 정보 나열 페이지(이름, url로 예측) : http://www.q-net.or.kr/crf005.do?id=crf00501s01&gSite=Q&gId=&div=1&obligFldCd=146 
-> 여기서 obligFldCd=146 값이 parm값이기 떄문에 parm값을 구해 URL을 조합해준 뒤 서브 자격증 정보 있는 사이트로 이동 가능

아직 해야할 크롤링 : 서브자격증 각각 페이지로 들어가는 URL을 찾아야함 - js로 돼있어서 아직 못찾겠음..
'''
