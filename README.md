# 졸업의 민족

~~우리가 어떤 민족입니까~~

## 🛠 프로젝트 실행 방법

```bash
# 프로젝트 클론
git clone https://github.com/IdealPeople/graduation-minjok.git

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

# 인증/인가구조

1. 로그인 POST (auth.wku.ac.kr) - `wkuTokenKey`, `JSESSIONID` 발급 → session 저장

2. loginReturn GET (intra.wku.ac.kr) - intra용 `JSESSIONID` 새로 발급 → session 저장

3. `wkuTokenKey`을 intra.wku에 강제 추가

4. 원하는 페이지 접근 GET - 모든 쿠키 (auth + intra) 자동 전송 - 최종 데이터 접근 성공
