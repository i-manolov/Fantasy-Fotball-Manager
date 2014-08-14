# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'dev key'
CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'postgresql://nfldb:nfldb@localhost/nfldb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')

POSTGRES_DIR = 'postgresql://nfldb:nfldb@localhost/nfldb'

