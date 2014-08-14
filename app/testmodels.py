from sqlalchemy import *
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


metadata = MetaData()
Base = declarative_base()
Base.metadata = metadata

db = create_engine('postgresql://nfldb:nfldb@localhost/nfldb', convert_unicode=True, echo=False)
metadata.reflect(bind=db)

users = metadata.tables['users']
fleagues = metadata.tables['f_league']

sm = orm.sessionmaker(bind=db, autoflush=True, autocommit=True, expire_on_commit=True)
session = orm.scoped_session(sm)

class User(Base):
	__tablename__='users'
	leagues=relationship("leagues", backref='user',lazy="dynamic")
	
class F_League(Base):
	__tablename__='f_league'
	
if __name__=='main':
	result=User.query.filter_by(user_name="ivan").first()
	print result
