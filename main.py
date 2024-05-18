import re
import yaml
from fastapi import FastAPI, HTTPException, status
import pymysql
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# 配置CORS设置


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


def read_config_file(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


config = read_config_file('config/config.yaml')
database = config['database']

app = FastAPI()
# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', database='login', charset='utf8mb4')
conn = pymysql.connect(host=database['host'], port=database['port'], user=database['username'], password=database['password'], database=database['database_name'], charset='utf8mb4')
table = database['table_name']
cur = conn.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def confirm(username: str, password: str) -> bool:
    sql = f'SELECT passwd FROM {table} WHERE username="{username}"'
    cur.execute(sql)
    result: tuple = cur.fetchall()

    if len(result) == 0:
        return False
    if result[0][0] == password:
        return True
    else:
        return False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.options("/login")
async def login_options():
    return {"Allow": "POST"}, status.HTTP_200_OK


@app.post("/login")
async def login(request: LoginRequest):
    username = request.username
    password = request.password
    if confirm(username, password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.post('/register')
async def register(request: RegisterRequest):
    username = request.username
    password = request.password
    sql = f'SELECT COUNT(*) FROM {table} WHERE username="{username}"'
    # sql = f'SELECT COUNT(*) FROM userinfo WHERE username"{username}"'
    cur.execute(sql)
    result = cur.fetchone()
    if re.match(r'^1[3456789]\d{9}$', username) and result[0] == 0:
        sql = f'insert into {table}(username,passwd) values("{username}","{password}")'
        # sql = f'insert into userinfo(username,passwd) values("{username}","{password}")'
        cur.execute(sql)
        conn.commit()
        return {"message": "Register successful"}
    else:
        raise HTTPException(status_code=401, detail="username has already been registered or username is not right")