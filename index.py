import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# .env 파일 로드
load_dotenv()

wku_user_id = os.getenv("USER_ID")
wku_user_pwd = os.getenv("USER_PWD")
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
    "userid": wku_user_id,      
    "passwd": wku_user_pwd,
    "nextURL": "http://intra.wku.ac.kr/SWupis/V005/loginReturn.jsp"
}

# 로그인 요청 (auth.wku.ac.kr)
login_url = "https://auth.wku.ac.kr/Cert/User/Login/login.jsp"
login_response = session.post(login_url, data=login_data, headers=headers)

if login_response.status_code == 200:
    print("!! 로그인 성공 !!")
    print("발급된 쿠키 확인")

    print(login_response.cookies)
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
    # print(soup.prettify())
    
    # 1. 학생 기본 정보 파싱
    student_info = {}
    info_table = soup.find_all('table')[0]
    info_rows = info_table.find_all('tr')
    
    # 학생 정보 추출
    for row in info_rows:
        th_tags = row.find_all('th')
        td_tags = row.find_all('td')
        
        # 각 행에서 th와 td를 묶어서 key, value로 딕셔너리 저장
        for th, td in zip(th_tags, td_tags):
            key = th.get_text(strip=True)
            value = td.get_text(strip=True)
            student_info[key] = value
    
    print("============ 학생 기본 정보 ============\n")
    for key, value in student_info.items():
        print(f"{key} : {value}")
    print("\n=====================================")
    
    # 이수 과목
    subject_info = {}
    subject_table = soup.find_all('table')[1]
    subject_values_row = subject_table.find_all("tr")[2].find_all("td")
    subject_info_labels = ['교필', '교선', '계필', '계기', '학필', '전기', '전필', '전선', '기전', '선전',
                           '응전', '학석', '융전', '복수전공', '부전공', '교직', '일선', '편입']
    
    for i, label in enumerate(subject_info_labels):
        subject_info[label] = subject_values_row[i].text.strip()
    
    print("============ 이수 과목 정보 ============\n")
    for key, value in subject_info.items():
        print(f"{key} : {value}")
    print("\n=====================================")
    
    # 합계
    summary_info = {}
    summary_row = subject_table.find_all("tr")[3].find_all("td")
    summary_info["교양 합계"] = summary_row[0].text.strip()
    summary_info["전공 합계"] = summary_row[1].text.strip()
    summary_info["기타 합계"] = summary_row[2].text.strip()
    summary_info["총계"] = subject_values_row[-1].text.strip()
    
    print("============ 합계 정보 ============\n")
    for key, value in summary_info.items():
        print(f"{key} : {value}")
    print("\n=====================================")
    
else:
    print("!! 성적 페이지 접근 실패 !!")