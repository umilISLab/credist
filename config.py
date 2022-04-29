from os import path, getenv, pardir
# from dotenv import load_dotenv

# load_dotenv()

db_name = getenv("STORY", "postgres")
db_pwd = getenv("PWD", "password")

smtp_server = getenv("SMTP", "smtp.unimi.it")
smtp_sender = getenv("SENDER", "vast@islab.di.unimi.it")

debug = True
# debug = False

db_path = "db.sqlite"
db_url = f"sqlite:///{db_path}?check_same_thread=False"
# db_url = f"postgresql+psycopg2://postgres:{db_pwd}@postgres:5432/{db_name}"

host = "0.0.0.0"
port = 8080

version = "0.0.1"
