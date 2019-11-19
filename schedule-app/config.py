import os

class Config(object):
    SECRET_KEY = 'YBieLEwbUBGbThmVeLZaiP8a8L3DPp'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')}"

