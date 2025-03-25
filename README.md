# Cangra 크롤링 파트

## 🛠 프로젝트 실행 방법

```bash
# 프로젝트 클론
git clone https://github.com/IdealPeople/cangra-crawling.git

cd project

# 가상환경(env) 생성
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# 프로젝트 실행
# index.py를 열어 웹정보서비스 아이디와 비밀번호 입력 필수
python3 index.py

# 작업 후 반드시 가상환경을 비활성화 할 것
deactivate
```

## 🛠️ 필수 환경 설정

해당 프로젝트는 주요 정보를 환경변수로 관리하고 있습니다.  
프로젝트를 클론한 후 아래의 단계를 따라 `.env`파일을 생성한 뒤 설정해주세요!

### 1. .env 파일 생성

프로젝트 루트 디렉터리에 `.env` 파일을 생성하세요.

### 2. .env 파일 설정

`USER_ID`와 `USER_PWD` 값을 아래와 같이 입력해주세요

```bash
USER_ID=웹정보서비스 아이디
USER_PWD=웹정보서비스 비밀번호

# 예시
USER_ID=abcdef
USER_PWD=thisispwd12
```

### 3. .env 파일을 git에 포함되지 않게 관리

`.env` 파일은 민감한 정보를 포함합니다. 따라서 `.gitignore`파일에 `.env`가 포함되어 있는지 반드시 확인하세요!

## 인증/인가구조

1. 로그인 POST (auth.wku.ac.kr) - `wkuTokenKey`, `JSESSIONID` 발급 → session 저장

2. loginReturn GET (intra.wku.ac.kr) - intra용 `JSESSIONID` 새로 발급 → session 저장

3. `wkuTokenKey`을 intra.wku에 강제 추가

4. 원하는 페이지 접근 GET - 모든 쿠키 (auth + intra) 자동 전송 - 최종 데이터 접근 성공
