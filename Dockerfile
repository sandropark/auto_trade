FROM python:3.12.2

# poetry, flask 설치
RUN pip install poetry && pip install flask
# workdir 설정
WORKDIR /auto-trade
# 현재 dir 복사
COPY . .
# poetry로 의존성 설치
RUN poetry install --no-root

# 컨테이너 생성 시 서버 실행
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]