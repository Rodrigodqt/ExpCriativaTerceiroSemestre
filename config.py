import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ibk-xfragil-chave-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:root123@db:3306/xfragil'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
