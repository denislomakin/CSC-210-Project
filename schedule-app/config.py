import os

class Config(object):
    SECRET_KEY = 'YBieLEwbUBGbThmVeLZaiP8a8L3DPp'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')}"
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_PUBLIC_KEY = '6Lem_cMUAAAAAKJkYy8dzRKOrZAGMXg1oztfP1id'
    RECAPTCHA_PRIVATE_KEY = '6Lem_cMUAAAAADtjIVxrSOeFnAI8uSTyhEz1t7Eg'
    RECAPTCHA_OPTIONS = {'theme': 'black'}

