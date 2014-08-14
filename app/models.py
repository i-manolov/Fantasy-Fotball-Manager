#from app import POSTGRES_DIR
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, mapper
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime, date



engine = create_engine('postgresql://nfldb:nfldb@localhost/nfldb', convert_unicode=True, echo=False)
#engine = create_engine(POSTGRES_DIR, convert_unicode=True, echo=False)
metadata=MetaData()
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    metadata.create_all(bind=engine)

#*************************************************FANTASY COMPONENTS*************************************************
class User(object):
        query=db_session.query_property()
       # leagues=relationship("F_League",backref="fowner",lazy="dynamic") 
	def __init__(self, user_name=None, first_name=None, last_name=None, email=None, password=None, last_sign_out=None):
	   # self.user_id= user_id
	    self.user_name = user_name
	    self.first_name = first_name
	    self.last_name = last_name
	    self.email = email
	    self.password = password
	    self.last_sign_out = last_sign_out

        
           

	#def set_password(self, password):
         #   self.pwdhash = generate_password_hash(password)

        def check_password(self, password):
            return self.password == password

        def is_authenticated(self):
            return True
        
        def is_active(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            return unicode(self.user_id)
        
	def save_last_sign_out(self, user_id):
            user=User.query.filter_by(user_id=user_id).first()
            if user:
                user.last_sign_out=datetime.now()
                print user.last_sign_out
                db_session.commit()

        def __repr__(self):
            return '<User %r>' % (self.user_name)
        
users = Table('users',metadata,
        Column('user_id', Integer, primary_key=True),
        Column('user_name', String, unique=True, nullable=False),
        Column('first_name', String, nullable=False),
        Column('last_name', String, nullable=False),
        Column('email', String,unique=True, nullable=False),
        Column('password', String),
        Column('last_sign_out', DateTime)
        )
mapper(User, users)

class F_League(object):
    query=db_session.query_property()  

    def __init__(self, user_id=None, yahoo_league_id=None, start_date=None, 
            end_date=None, num_teams=None, league_url=None, league_name=None,
            game_key=None, season_year=None):
       # self.league_id=league_id
        self.user_id = user_id
        self.yahoo_league_id = yahoo_league_id
        self.start_date = start_date
        self.end_date = end_date
        self.num_teams = num_teams
        self.league_url = league_url
        self.league_name = league_name
        self.game_key = game_key
        self.season_year = season_year

    def get_weeks(self):
        week = Week_Lookup.query.all()
        # hardcoded current year, for now, lol
        if self.season_year == 2013:
            week_list = list()
            for w in week:
                if (w.start_date <= date.today()) and (w.start_date >= self.start_date):
                    week_list.append(w.week_num)
            print "week list: %s" % week_list
            return week_list
        else:
            # return all weeks
            return list(range(1,17))

    
    def full_league_id(self):
        return "%s.l.%s" % (self.game_key, self.yahoo_league_id)

    def __repr__(self):                                                    
        return '<F_League  %r>' % (self.league_name) 

fleagues = Table("f_league",metadata,
        Column( 'league_id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.user_id')),
        Column('yahoo_league_id', Integer, nullable=False, unique=True),
        Column('start_date', DateTime, nullable=False),
        Column('end_date', DateTime, nullable=False),
        Column('num_teams', Integer, nullable=False),
        Column('league_url', String, nullable=False),
        Column('league_name', String, nullable=False),
        Column('game_key', Integer),
        Column('season_year', Integer)
        )
mapper(F_League, fleagues)

class F_Team(object):
    query = db_session.query_property()

    def __init__(self, league_id=None,team_name=None,yahoo_team_id=None, yahoo_team_url=None, yahoo_team_logo=None, yahoo_manager_name=None, yahoo_manager_id=None) : 
        #self.team_id=team_id
        self.league_id = league_id
        self.team_name = team_name
        self.yahoo_team_id = yahoo_team_id
        self.yahoo_team_url = yahoo_team_url
        self.yahoo_manager_name = yahoo_manager_name
        self.yahoo_manager_id = yahoo_manager_id
        self.yahoo_team_logo = yahoo_team_logo

    def bench_all_roster(self, f_team_id):
        f_players_on_team=F_Player.query.filter_by(f_team_id=f_team_id) 
        for f_player in f_players_on_team:
            f_player.on_roster=False
            db_session.commit()

    def __repr__(self):
        return '< F_Team %r>' % (self.team_name)

fteams = Table('f_team', metadata,
        Column('f_team_id', Integer, primary_key=True),
        Column('league_id', Integer, ForeignKey('f_league.league_id'), nullable=False),
        Column('team_name', String, nullable=False),
        Column('yahoo_team_id', Integer, nullable=False),
        Column('yahoo_team_url', String, nullable=False),
        Column('yahoo_team_logo', String),
        Column('yahoo_manager_name', String, nullable=False),
        Column('yahoo_manager_id', String, nullable=False),
        UniqueConstraint('league_id' ,'yahoo_team_id', name='uniqueteam')
        )
mapper(F_Team, fteams)

class F_Player(object):
    query = db_session.query_property() 

    def __init__(self, f_team_id=None, on_roster=None, offense=None):
        #self.fplayer_id=fplayer_id
        #self.player_id = player_id
        self.f_team_id = f_team_id
        self.on_roster = on_roster
        self.offense= offense

    def put_f_player_on_roster(self, f_player_id):
        f_player=F_Player.query.filter_by(f_player_id=f_player_id).first()
        f_player.on_roster=True
        db_session.commit()

    def __repr__(self):
        print '< F_Player %r>' % (self.f_player_id)

fplayers = Table('f_player', metadata,
        Column('f_player_id',Integer, primary_key=True),
        Column('f_team_id', Integer, ForeignKey('f_team.f_team_id')),
        Column ('on_roster', Boolean),
        Column('offense', Boolean)
        )
mapper(F_Player, fplayers)

class F_Played_For_Week(object):
    query = db_session.query_property()
    
    def __init__(self, f_player_id=None, week_num=None, selected_position=None, display_position=None):
        #self.fplayed_id=fplayed_id
        self.f_player_id = f_player_id
        self.week_num = week_num
        self.selected_position=selected_position
        self.display_position=display_position

    def __repr__(self):
        print '< F_Played_For_Week %r>' % (self.fplayed_id)

f_played_for_weeks = Table('f_played_for_week', metadata,
        Column('f_played_id', Integer, primary_key=True),
        Column('f_player_id', Integer, ForeignKey('f_player.f_player_id')),
        Column('week_num', Integer, ForeignKey('week_lookup.week_id')),
        Column('display_position', String, nullable=False),
        Column('selected_position', String, nullable=False)
        #UniqueConstraint('f_player_id' ,'week_num', name='uniqueplayedforweek')
        )
mapper(F_Played_For_Week, f_played_for_weeks)   

# Class to keep track of yahoo_guid and user_id. Only registered users will be added to this table. 
#This way we can match up who owns the team in the get_league_teams query 
class Yahoo_User_Guid(object):
    query=db_session.query_property()

    def __init__(self, user_id=None, yahoo_guid=None):
        self.user_id = user_id
        self.yahoo_guid = yahoo_guid

    def __repr__(self):
        print '<UserId: %r> <Yahoo Guid: %r >' %(self.user_id, self.yahoo_guid)

yahoo_user_guids= Table('yahoo_user_guid', metadata,
        Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False, primary_key=True),
        Column('yahoo_guid', String, nullable=False, unique=True, primary_key=True),
        )
mapper(Yahoo_User_Guid, yahoo_user_guids)

#Class to match up Fantasy Team Owner
class F_Team_Owner(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, f_team_id=None):
        self.user_id = user_id
        self.f_team_id = f_team_id

    def __repr__(self):
        print '< FTeam Owner --> UserID: %r, F_Team_ID: %r>' %(self.user_id, self.f_team_id)

f_team_owners= Table('f_team_owner', metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), nullable=False, primary_key=True),
    Column('f_team_id', Integer, ForeignKey('f_team.f_team_id'), nullable=False, primary_key=True),
    UniqueConstraint('user_id', 'f_team_id', name='uniqueteamowner')
    )

mapper(F_Team_Owner, f_team_owners)

class F_Team_Points_Per_Week(object):
    query=db_session.query_property()

    def __init__(self,f_team_id=None, points=None, 
            projected_points=None,week_num=None):
        self.f_team_id = f_team_id
        self.points = points
        self.projected_points = projected_points
        self.week_num = week_num

    def __repr__ (self):
        print '<Team points for the week --> F_Team_ID: %r, Points: %r, Projected Points %r>' % (self.f_team_id,
                self.points, self.projected_points)

f_team_points_per_weeks=Table('f_team_points_per_week', metadata,
        Column('f_team_points_per_week_id', Integer, primary_key=True),
        Column('f_team_id', Integer, ForeignKey('f_team.f_team_id'), nullable=False),
        Column('points', Float, nullable=False),
        Column('projected_points', Float, nullable=False),
        Column('week_num', Integer, ForeignKey('week_lookup.week_num'), nullable=False),
        UniqueConstraint('f_team_id', 'week_num', name='f_team_points_per_week_unique')
        )
mapper(F_Team_Points_Per_Week, f_team_points_per_weeks)


class Week_Lookup(object):
    query=db_session.query_property()

    def __init__(self, week_description=None,week_num=None, start_date=None,end_date=None):
        self.week_description = week_description
        self.week_num = week_num
        self.start_date = start_date
        seld.end_date = end_date
    
    def __repr__(self):
        print '<Week Description: %r>' % (self.week_description)

week_lookups=Table('week_lookup', metadata,
        Column('week_num', Integer, primary_key=True),
        Column('week_description', String, nullable=False),
        Column('start_date', DateTime, nullable=False),
        Column('end_date', DateTime, nullable=False)
        )
mapper(Week_Lookup, week_lookups)

class F_Player_Points_Per_Week(object):
    query=db_session.query_property()

    def __init__(self, f_player_id=None, points=None, week_num=None):
        self.f_player_id = f_player_id
        self.points = points
        self.week_num = week_num

f_player_points_per_weeks=Table('f_player_points_per_week', metadata,
        Column('f_player_points_per_week_id', Integer, primary_key=True),
        Column('f_player_id', Integer, ForeignKey('f_player.f_player_id'), nullable=False),
        Column('points', Float, nullable=False),
        Column('week_num', Integer, ForeignKey('week_lookup.week_num'), nullable=False)
        )
mapper(F_Player_Points_Per_Week, f_player_points_per_weeks)

class F_Matchup(object):
    query = db_session.query_property()

    def __init__(self, opponent1_f_team_id=None, opponent2_f_team_id=None,  week_num=None):
        self.opponent1_f_team_id = opponent1_f_team_id
        self.opponent2_f_team_id = opponent2_f_team_id
        self.week_num = week_num

f_matchups=Table('f_matchups', metadata, 
        Column('f_matchup_id', Integer, primary_key=True),
        Column('opponent1_f_team_id', Integer, ForeignKey('f_team.f_team_id'), nullable=False),
        Column('opponent2_f_team_id', Integer, ForeignKey('f_team.f_team_id'), nullable=False),
        Column('week_num', Integer, ForeignKey('week_lookup.week_num')),
        UniqueConstraint('opponent1_f_team_id', 'opponent2_f_team_id','week_num', name='f_matchups_unique')
        )
mapper(F_Matchup, f_matchups)  

class F_Def_Player(object):
    query=db_session.query_property()

    def __init__(self, f_player_id=None, team_id=None):
        self.f_player_id=f_player_id
        self.team_id=team_id

f_def_players=Table('f_def_player', metadata,
        Column('f_def_player_id', Integer, primary_key=True),
        Column('team_id', String, ForeignKey('team.team_id'), nullable=False),
        Column('f_player_id', Integer, ForeignKey('f_player.f_player_id'), nullable=False)
        )
mapper(F_Def_Player, f_def_players)

class F_Offense_Player(object):
    query = db_session.query_property()

    def __init__(self,player_id=None, f_player_id=None):
        self.player_id = player_id
        self.f_player_id = f_player_id

f_offense_players=Table('f_offense_player', metadata,
        Column('f_offense_player_id', Integer, primary_key=True),
        Column('player_id', String, ForeignKey('player.player_id'), nullable=False),
        Column('f_player_id', Integer, ForeignKey('f_player.f_player_id'), nullable=False)
        )
mapper(F_Offense_Player, f_offense_players)
    

#********************************************NFL COMPONENTS*********************************************
class NFL_Player(object):
    query = db_session.query_property()

    def __init__(self, first_name=None, last_name=None, full_name=None,
                team=None, position=None, uniform_number=None, height=None,
                weight=None, status=None):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.team = team
        self.position = position
        self.uniform_number = uniform_number
        self.height = height
        self.weight = weight
        self.status = status

    def __repr__(self):
        print '< NFL Player --> Full Name: %r, Team: %r, Uniform#: %r >' %(self.full_name, self.team, self.uniform_number)

nfl_players=Table('player', metadata,
        Column('player_id', String, primary_key=True),
        Column('full_name', String),
        Column('first_name', String, nullable=False),
        Column('last_name', String, nullable=False),
        Column('team', String, nullable=False),
        Column('position', String,ForeignKey('team.team_id'), nullable=False),
        Column('uniform_number', Integer, nullable=False),
        Column('height', String),
        Column('weight', String),
        Column('status',String)
        )
mapper(NFL_Player, nfl_players)

class NFL_Team(object):
    query=db_session.query_property()

    def __init__(self, team_id=None, city=None, name=None):
        self.team_id = team_id
        self.city = city
        self.name = name

    def __repr__(self):
        print '< Team --> Name: %r, City: %r >' % (self.name, self.city)

nfl_teams=Table('team', metadata,
        Column('team_id', String, primary_key=True),
        Column('city', String, nullable=False),
        Column('name', String, nullable=False)
        )
mapper(NFL_Team, nfl_teams)

class NFL_Player_Status_Update(object):
    query=db_session.query_property()
    
    def __init__(self, old_status=None, new_status=None, nfl_player_id=None, date=None):
        self.old_status=old_status
        self.new_status=new_status
        self.nfl_player_id=nfl_player_id
        self.date=date
    
    def __repr__(self):
        print ('<NFL PLayer Status Update: --> nfl_player_id: %r , old status: %r , new_status: %r , date updated: %r>'
                % (self.nfl_player_id, self.old_status, self.new_status, self.date))

nfl_player_status_updates= Table('nfl_player_update_status', metadata,
        Column('status_update_id', Integer, primary_key=True),
        Column('old_status', Text, nullable=False),
        Column('new_status', Text, nullable=False),
        Column('date', DateTime, nullable=False),
        Column('nfl_player_id', Text, ForeignKey('player.player_id'), nullable=False)
        )
mapper(NFL_Player_Status_Update, nfl_player_status_updates)


#*******************RSS FEEDS***************************** 
class Yahoo_RSS_Data(object):
    query = db_session.query_property()
    
    def __init__(self, rss_id=None, title=None, url=None, content_1=None, content_2=None,
            timestamp=None, media_url=None, media_inf=None):
        self.rss_id = rss_id
        self.title = title
        self.url = url
        self.content_1 = content_1
        self.content_2 = content_2
        self.timestamp = timestamp
        self.media_url = media_url
        self.media_inf = media_inf

yahoo_rss_feed = Table('yahoo_rss_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('rss_id', String, nullable=False),
        Column('title', String, nullable=False),
        Column('url', String, nullable=False),
        Column('content_1', String),
        Column('content_2', String),
        Column('media_url', String),
        Column('media_inf', String),
        Column('timestamp', DateTime)
)
mapper(Yahoo_RSS_Data, yahoo_rss_feed)

class Roto_RSS_Data(object):
    query = db_session.query_property()

    def __init__(self, rss_id=None, title=None, url=None, content_1=None, timestamp=None):
        self.rss_id = rss_id
        self.title = title
        self.url = url
        self.content_1 = content_1
        self.timestamp = timestamp

roto_rss_feed = Table('roto_rss_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('rss_id', String, nullable=False),
        Column('title', String, nullable=False),
        Column('content_1', String),
        Column('url', String),
        Column('timestamp', DateTime)
)
mapper(Roto_RSS_Data, roto_rss_feed)

class Roto_RSS_Player_Data(object):
    query = db_session.query_property()

    def __init__(self, rss_id=None, title=None, player_url=None, content=None,
            full_name=None, first_name=None, last_name=None, team_abbr=None,
            timestamp=None):
        
        self.rss_id = rss_id
        self.title = title
        self.player_url = player_url
        self.content = content
        self.timestamp = timestamp
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name

roto_rss_players = Table('roto_rss_player_data', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String, nullable=False),
        Column('content', String, nullable=False),
        Column('full_name', String, nullable=False),
        Column('first_name', String, nullable=False),
        Column('last_name', String, nullable=False),
        Column('team_abbr', String, nullable=False),
        Column('rss_id', String, nullable=False),
        Column('player_url', String, nullable=False),
        Column('timestamp', DateTime)
        )
mapper(Roto_RSS_Player_Data, roto_rss_players)
        


#***************TESTING *****************
if __name__=="__main__":
	result=User.query.filter_by(user_name="brian").first()
        print result
        league = db_session.query(F_League).join(User).filter_by(user_id=1).first()
        print league
        test= User.query.filter_by(user_name='ivan').first()
        print test.user_id

        #get last insert record user_id
        test1=User.query.all()
        print str(test1[-1].user_id)

        test2=User.query.order_by(User.user_id.desc()).first()
        print test
        
        test2=User.query.order_by(User.user_id.desc()).first()
        print test2.user_id
        
        #get league_id by searching yahoo_league_id
        f_league=F_League.query.filter_by(yahoo_league_id='1173612').first()
        print f_league.league_id
        
        nfl_player=NFL_Player.query.filter_by(first_name='Montee', last_name='Ball', uniform_number=28, team='DEN').first()
        print nfl_player.player_id

        last_f_player_id=F_Player.query.all()
        print last_f_player_id[-1].f_player_id

        #u1=User()
        #f1= F_League()
        #print u1.leagues
        #many1= db_session.query(User.leagues).join(User).filter_by(user_id=1).first()
        #print many1
