from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')
user = os.getenv('DB_USER')


engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{db}')