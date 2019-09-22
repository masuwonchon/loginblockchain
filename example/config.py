"""
This is example web site using python flask based on LHB(login hash block) module.
@version: 1.0.0
@authour: suwonchon(suwonchon@gmail.com)
@contact http://github.com/masuwonchon/loginblockchain
@license: MIT
"""

import os

SECRET_KEY = 'top-secret'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
