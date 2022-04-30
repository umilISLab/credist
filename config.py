from os import path, getenv, pardir

from secret import db_pwd

db_name = "credist"
db_user = "credist"
db_host = "localhost"

mail_host = "smtp.unimi.it"
mail_sender = "vast@islab.di.unimi.it"

# debug = True
debug = False

# db_path = "db.sqlite"
# db_url = f"sqlite:///{db_path}?check_same_thread=False"
db_url = f"postgresql+psycopg2://{db_user}:{db_pwd}@{db_host}:5432/{db_name}"

host = "0.0.0.0"
port = 8080

version = "0.0.1"
