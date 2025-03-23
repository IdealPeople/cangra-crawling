import requests
from bs4 import BeautifulSoup

# 세션 생성
session = requests.Session()

# User-Agent 생성
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

# 로그인용 데이터
login_data = {
    "userid": "웹정보서비스 아이디",      
    "passwd": "웹정보서비스 비밀번호",
    "nextURL": "http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp"
}

# 로그인 요청 (auth.wku.ac.kr)
login_url = "https://auth.wku.ac.kr/Cert/User/Login/login.jsp"
login_response = session.post(login_url, data=login_data, headers=headers)

if login_response.status_code == 200:
    print("!! 로그인 성공 !!")
else:
    print("!! 로그인 실패 !!")
    exit()

# wkuTokenKey 쿠키 확보
wku_token = login_response.cookies.get("wkuTokenKey")
if not wku_token:
    print("!! wkuTokenKey 발급 실패 !!")
    exit()
print(f"!! wkuTokenKey 확보: {wku_token} !!")

# intra.wku 접근
return_url = "https://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp"
return_response = session.get(return_url, headers=headers)

if return_response.status_code == 200:
    print("!! loginReturn 성공 intra 세션 확보 성공 !!")
else:
    print("!! loginReturn 실패 !!")
    exit() 

# 크롤링 진행
score_url = "https://intra.wku.ac.kr/SWupis/V005/Service/Stud/Print/studComplete.jsp?sm=3"

# wkuTokenKey를 쿠키로 intra.wku에 강제로 추가
session.cookies.set("wkuTokenKey", wku_token, domain="intra.wku.ac.kr")

score_response = session.get(score_url, headers=headers)

if score_response.status_code == 200:
    print("!! 페이지 접근 성공 !!")

    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(score_response.text, "html.parser")
    print(soup.prettify())
    
    # 학생 기본 정보 파싱
    student_info = {}
    info_table = soup.find_all('table')[0]
    info_rows = info_table.find_all('tr')
    for row in info_rows:
        th_tags = row.find_all('th')
        td_tags = row.find_all('td')
    for th, td in zip(th_tags, td_tags):
        key = th.get_text(strip=True)
        value = td.get_text(strip=True)
        student_info[key] = value

    print("============ 학생 기본 정보 ============\n")
    for key, value in student_info.items():
        print(f"{key} : {value}")
    print("\n=====================================")
    
else:
    print("!! 성적 페이지 접근 실패 !!")
