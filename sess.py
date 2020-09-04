#This code is to create a sessin that will be used to connect to the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


mysql_host = os.environ.get('MYSQL_HOST')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
db_name = os.environ.get('DB_NAME')


engine = create_engine('mysql://' + mysql_user + ':' + mysql_password + '@' + mysql_host + '/' + db_name)
Session = sessionmaker(bind=engine)
session = Session()


