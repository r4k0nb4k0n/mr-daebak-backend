# mr-daebak-backend

## How to install

```
python3 -m venv .venv
. .venv/bin/activate
(venv) python -m pip install -r requirements.txt
```

## How to run

```
. .venv/bin/activate
(venv) python3 -m uvicorn main:app --reload
```

## Description

- `mr-daebak-backend/`
  - `./app/` - 파이썬 모듈 `app`
    - `./__init__.py` - 모듈화를 위한 더미 파일
    - `./database/` - 파이썬 서브모듈 `database`. `db.json` 파일을 이용하여 데이터베이스를 모사한다.
      - `./__init__.py` - 모듈화를 위한 더미 파일
      - `./database.py` - `database` 클래스. `db.json` 파일 안의 JSON을 파이썬 dict로 불러오고 변경사항이 생겨서 저장할 필요가 생길 때마다 파일에도 반영한다.
    - `./models/` - 파이썬 서브모듈 `models`. 데이터들을 어떤 형식으로 저장하고 주고 받을 것인지 정의한다.
      - `./__init__.py` - 모듈화를 위한 더미 파일
      - `./domain/` - 파이썬 서브모듈 `domain`. 데이터베이스에 데이터들을 어떤 형식으로 저장할 것인지 정의한다.
        - `./__init__.py` - 모듈화를 위한 더미 파일
        - `item.py`
        - `dinner_menu.py`
        - `dinner_style.py`
        - `order_detail.py`
        - `order.py`
        - `user.py`
      - `./schema/` - 파이썬 서브모듈 `schema`. REST API에서 데이터들을 어떤 형식으로 주고 받을 것인지 정의한다.
        - `./__init__.py` - 모듈화를 위한 더미 파일
        - `./item.py`
        - `./dinner_menu.py`
        - `./dinner_style.py`
        - `./order.py`
        - `./user.py`
        - `./jwt.py`
    - `./services/` - 파이썬 서브모듈 `services`. 사용자 인증에 필요한 JSON Web Token, 패스워드 해싱 등의 기능을 제공한다.
      - `./__init__.py` - 모듈화를 위한 더미 파일
      - `./jwt.py` - JSON Web Token
      - `./security.py` - 패스워드 해싱
    - `./routers/` - 파이썬 서브모듈 `routers`. 프론트엔드에서 가져다 쓰기 편하게 REST API를 정의한다.
      - `./__init__.py` - 모듈화를 위한 더미 파일
      - `./item.py` - item에 대한 GET/POST/PATCH/DELETE 핸들러 정의
      - `./dinner_menu.py` - dinner_menu에 대한 GET/POST/PATCH/DELETE 핸들러 정의
      - `./dinner_style.py` - dinner_style에 대한 GET/POST/PATCH/DELETE 핸들러 정의
      - `./order.py` - order에 대한 GET/POST/PATCH/DELETE 핸들러 정의
      - `./user.py` - user에 대한 GET/POST/PATCH/DELETE 핸들러 정의 / user login에 대한 POST 핸들러 정의
  - `./db.json` - 데이터베이스를 모사하는 JSON 파일
  - `./main.py` - 파이썬 모듈 `app`을 기반으로 웹 서버를 실행하는 스크립트 파일
  - `./requirements.txt` - 필요한 파이썬 모듈들이 적힌 파일
