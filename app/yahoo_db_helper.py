from app import db
from models import *
from datetime import datetime


class Db_Helper():

    def __init__(self):
        self.user_id = None
        self.yahoo_user_guid = None
        self.f_league_dict = None
        self.f_player_dict = None
        self.rss_dict = None

    def reset(self):
        self.__init__()

    def return_league_id(self, user_id):
        f_league = F_League.query.filter_by(user_id = user_id).first()
        if f_league is None:
            raise Exception('league_id query returned nothing')
        return f_league.yahoo_league_id

    def return_num_teams(self, league_id):
        f_league = F_League.query.filter_by(yahoo_league_id = league_id).first()
        if f_league is None:
            raise Exception('num_teams query returned nothing')
        return f_league.num_teams


    def insert_yahoo_user_guid(self, user_id, yahoo_guid):
        assert user_id is not None
        assert yahoo_guid is not None

        yahoo_user_guid=Yahoo_User_Guid(
                user_id=user_id,
                yahoo_guid=yahoo_guid
                )
        exists_in_db= yahoo_user_guid.query.filter_by(yahoo_guid=yahoo_guid).first()
        if not exists_in_db:
            db.session.add(yahoo_user_guid)
            db.session.commit()


    def insert_f_league_v2(self, f_league_dict):
        f_league = F_League(
                user_id = f_league_dict['user_id'],
                yahoo_league_id = f_league_dict['yahoo_league_id'],
                start_date = f_league_dict['start_date'],
                end_date = f_league_dict['end_date'],
                num_teams = f_league_dict['num_teams'],
                league_url = f_league_dict['league_url'],
                league_name = f_league_dict['league_name'],
                game_key = f_league_dict['game_key'],
                season_year = f_league_dict['season_year']
                )

        exists_in_db = f_league.query.filter_by(
                user_id = f_league_dict['user_id'],
                yahoo_league_id = f_league_dict['yahoo_league_id'],
                season_year = f_league_dict['season_year']).first()
        
        if not exists_in_db:
            print "new fantasy_league: %s %s" % (f_league_dict['season_year'], f_league_dict['league_name'])
            db.session.add(f_league)
            db.session.commit()

    def insert_f_league(self, f_league_dict):
        assert f_league_dict is not None
        f_league= F_League(
                user_id=f_league_dict['user_id'],
                yahoo_league_id=f_league_dict['yahoo_league_id'],
                start_date= f_league_dict['start_date'],
                end_date=f_league_dict['end_date'],
                num_teams=f_league_dict['num_teams'],
                league_url=f_league_dict['league_url'],
                league_name=f_league_dict['league_name']
                )
        exists_in_db=f_league.query.filter_by(user_id=f_league_dict['user_id'], yahoo_league_id=f_league_dict['yahoo_league_id']).first()
        if not exists_in_db:
            db.session.add(f_league)
            db.session.commit()

    def insert_f_league_teams(self,f_team_dict):
        assert f_team_dict is not None
        #Save ALL teams in a league to db. IF yahoo_manager_guid == user_guid --> add to f_team_owner and get last inserted team which will be your team
        f_team=F_Team(
                 league_id=f_team_dict['league_id'],
                 team_name=f_team_dict['yahoo_team_name'],
                 yahoo_team_id=f_team_dict['yahoo_team_id'],
                 yahoo_team_url=f_team_dict['yahoo_team_url'],
                 yahoo_manager_name=f_team_dict['yahoo_manager_name'],
                 yahoo_manager_id=f_team_dict['yahoo_manager_id'],
                 yahoo_team_logo=f_team_dict['yahoo_team_logo']
                 )
        f_team_exists= F_Team.query.filter_by(league_id=f_team_dict['league_id'], yahoo_team_id=f_team_dict['yahoo_team_id']).first()
        if not f_team_exists:
            db.session.add(f_team)
            db.session.commit()

    def insert_f_team_owner(self, user_id):
        last_team=F_Team.query.order_by(F_Team.f_team_id.desc()).first()
        last_team_id=last_team.f_team_id
        f_team_owner=F_Team_Owner(
                user_id=user_id,
                f_team_id=last_team_id
                )
        #temporary fix, only have one team per user? 
        f_team_owner_exists=F_Team_Owner.query.filter_by(user_id=user_id).first() # , f_team_id=last_team_id).first()
        if not f_team_owner_exists:
            db.session.add(f_team_owner)
            db.session.commit()

    def brians_import_players_data_v2(self, data_dict):
        """used to insert data returned from _parse_players_data_v2
        previous usage:

            yahoo_db_helper = Db_Helper()
            f_team_id = yahoo_db_helper.return_f_team_id(yahoo_league_id, yahoo_team_id)
            yahoo_db_helper.insert_f_player(f_player_dict)
            player_dict=dict(
                    f_team_id=f_team_id,
                    f_player_first_name=f_player_first_name,
                    f_player_last_name=f_player_last_name,
                    f_player_first_name_ascii=f_player_first_name_ascii,
                    f_player_last_ascii=f_player_last_ascii,
                    f_player_team_abbr=f_player_team_abbr.upper(),
                    f_player_uniform_number=f_player_uniform_number,
                    f_player_position=f_player_position
                )
            yahoo_db_helper.insert_f_player(f_player_dict)
        """
        
        yahoo_league_id = data_dict['meta']['league_id']
        yahoo_team_id = data_dict['meta']['team_id']
        f_team_id = self.return_f_team_id(yahoo_league_id, yahoo_team_id)
        f_team=F_Team()
        f_team.bench_all_roster(f_team_id=f_team_id)
        #f_players_on_team=F_Player.query.filter_by(f_team_id=f_team_id).all()
        for k, v in data_dict.iteritems():
            if k != u'meta':
                f_player_dict = {}
                f_player_dict['f_team_id'] = f_team_id
                f_player_dict['f_player_first_name'] = v['first_name']
                f_player_dict['f_player_last_name'] = v['last_name']
                f_player_dict['f_player_first_name_ascii'] = v['first_name_ascii']
                f_player_dict['f_player_last_name_ascii'] =v['last_name_ascii']
                f_player_dict['f_player_team_abbr'] = v[u'editorial_team_abbr'].upper()
                f_player_dict['f_player_uniform_number'] = v['uniform_number']
                f_player_dict['f_player_position'] = v['display_position']
                        
                f_players_on_team=F_Player.query.filter_by(f_team_id=f_team_id).all()
                f_player_dict['f_players_on_team']=f_players_on_team            
                if not f_players_on_team:
                    #print "\n"
                    #print 'NEW: ADDING: %s %s' % (f_player_dict['f_player_first_name'], f_player_dict['f_player_last_name'])
                    self.insert_f_player(f_player_dict)
                
                else:
                    #print "\n"
                    #print 'UPDATE: PLAYER EXISTS:%s %s'  % (f_player_dict['f_player_first_name'], f_player_dict['f_player_last_name'])
                    self.update_f_player(f_player_dict)                
                
         #pass

    #Call this function to update f_player roster if Last Log Out in Users Table in NFL DB is NOT NULL
    def update_f_player(self, f_player_dict):
        #FOR f_player_id in f_offense_player (IF IT EXISTS), get  player_id(nfl) 
        #See if dict first_name, last_name, team, number return nfl_player_id the same as one in the list. IF IT DOES,  set on_roster bit to one. 
        #IF IT DOESNT, new player set on_roster bit to one again. Old player will be left as on_roster False
        
        # ------------------------------------------------------------------------------------------------------------------------------------
        #Have enough info to pull out nfl_player_id for f_player_dict NFL PLAYER. 
        #Question is how to match up f_player with that nfl_player_id?
        #if f_player_dict['display_position']== 'DEF' --> see if f_def_player.nfl_player_id and f_player_id exist
        # -----------> JOIN THE TWO TABLES ON F_PLayer_ID , filter by f_team_id , try to filter by nfl_player_id
        
        if f_player_dict['f_player_position'].lower()!='def': 
            #offense player
            nfl_player_id_match=self.return_nfl_player_id(first_name=f_player_dict['f_player_first_name'],
                    last_name=f_player_dict['f_player_last_name'], uniform_number=f_player_dict['f_player_uniform_number'],
                    team=f_player_dict['f_player_team_abbr'])
            f_offense_player_exists= db.session.query(F_Player.f_player_id, F_Offense_Player).\
                    filter(F_Player.f_player_id==F_Offense_Player.f_player_id).\
                    filter(F_Player.f_team_id== f_player_dict['f_team_id']).\
                    filter(F_Offense_Player.player_id==nfl_player_id_match).first()
            if f_offense_player_exists:
               #if he exists update that he is on roster, o.w save new player 
               f_player=F_Player()
               f_player.put_f_player_on_roster(f_player_id=f_offense_player_exists.f_player_id)
            else:
                self.insert_f_player(f_player_dict)
        
        else:
            #defense player
            f_def_player_exists=db.session.query(F_Player.f_player_id, F_Def_Player).filter(F_Player.f_player_id== F_Def_Player.f_player_id).\
                    filter(F_Player.f_team_id==f_player_dict['f_team_id']).\
                    filter(F_Def_Player.team_id==f_player_dict['f_player_team_abbr']).first()
            if f_def_player_exists:
                f_player2=F_Player()
                f_player2.put_f_player_on_roster(f_player_id=f_def_player_exists.f_player_id)
            else:
                self.insert_f_player(f_player_dict)
        

        '''
        for f_player in f_player_dict['f_players_on_team']:
            nfl_player_id_match= self.return_nfl_player_id(first_name=f_player_dict['f_player_first_name'],
                    last_name=f_player_dict['f_player_last_name'], uniform_number=f_player_dict['f_player_uniform_number'],
                    team=f_player_dict['f_player_team_abbr'])
            print 'F_Player_ID: ' + str(f_player.f_player_id)
            print 'NFL_Player_ID_Match:' + str(nfl_player_id_match)          
            
            #Check if player is offense or defense
            if f_player.offense==True:
                f_offense_player=F_Offense_Player.query.filter_by(player_id=nfl_player_id_match, f_player_id=f_player.f_player_id).first()
                if f_offense_player:
                    f_player.on_roster=True
                    db.session.commit()
                else: 
                    self.insert_f_player(f_player_dict)
            else: 
                f_def_player=F_Def_Player.query.filter_by(team_id=f_player_dict['f_player_team_abbr'], f_player_id=f_player.f_player_id).first()
                if f_def_player:
                    f_player.on_roster=True
                    db.session.commit()
                else:
                    self.insert_f_player(f_player_dict)
        '''   

    #Call this only once if log out date is NULL in db. NEVER AGAIN!
    def insert_f_player(self, f_player_dict):
        assert f_player_dict is not None
        """
             Insert f_Player with only f_team_id and roster bit set to null. 
             Get the newly created f_player_id
             Determine if player is defense or offense
             Enter in corresponding table
        """
        #Check if player exists already--->don't add
        if f_player_dict['f_player_position'].upper() != 'DEF': 
            f_player=F_Player(
                    f_team_id=f_player_dict['f_team_id'],
                    on_roster=True,
                    offense=True
                    )
            print 'COMMITING F_Player: OFFENSE f_team_id: %s name: %s pos: %s' % (
                    f_player_dict['f_team_id'],
                    f_player_dict['f_player_first_name'],
                    f_player_dict['f_player_position'])

            db.session.add(f_player)
            db.session.commit()
        else:
            f_player=F_Player(
                    f_team_id=f_player_dict['f_team_id'],
                    on_roster=True,
                    offense=False)
            print 'COMMITTING F_Player: DEFENSE f_team_id: %s name: %s pos: %s' % (
                    f_player_dict['f_team_id'],
                    f_player_dict['f_player_first_name'],
                    f_player_dict['f_player_position'])
            db.session.add(f_player)
            db.session.commit()
        
        last_f_player_id=self.return_last_f_player_id()
        if f_player_dict['f_player_position'].upper() != 'DEF':
            #offense player
            #self.update_f_player_offense_bit(f_player_id=last_f_player_id, offense_bit=True) # set bit to true
            nfl_player_id=self.return_nfl_player_id(first_name=f_player_dict['f_player_first_name'],
                    last_name=f_player_dict['f_player_last_name'], uniform_number=f_player_dict['f_player_uniform_number'],
                    team=f_player_dict['f_player_team_abbr'])           
            #print "executing IF f_player_dict['f_player_position'].upper()!='DEF': "
            print "-" * 20
            print "INSERTING INTO OFFENSE_PLAYER"
            print "nfl_player_id: %s" % nfl_player_id
            print "last_player_id: %s" % last_f_player_id
            print "-" * 20
            self.insert_f_offense_player(nfl_player_id=nfl_player_id, f_player_id=last_f_player_id)
        else:
            #defense player
            #self.update_f_player_offense_bit(f_player_id=last_f_player_id, offense_bit=False) # set offense bit to false for quicker look up
            #print "executing ELSE f_player_dict['f_player_position'].upper()!='DEF': "
            print "-" * 20
            print "INSERTING INTO DEFENSE_PLAYER"
            print "inserting %s" % (f_player_dict['f_player_team_abbr'])
            print "-" * 20
            self.insert_f_def_player(f_player_dict['f_player_team_abbr'], last_f_player_id)
    
    #Update f_player offense bit after inserting a player
    def update_f_player_offense_bit(self, f_player_id, offense_bit):
        f_player=F_Player.query.filter_by(f_player_id=f_player_id).first()
        print f_player
        f_player.offense=offense_bit
        db.session.commit()
       


    def insert_f_def_player(self,team_id, f_player_id):
        f_def_player=F_Def_Player(
                team_id=team_id,
                f_player_id=f_player_id
                )
        db.session.add(f_def_player)
        db.session.commit()


    def insert_f_offense_player(self, nfl_player_id, f_player_id):
        f_offense_player=F_Offense_Player(
                player_id=nfl_player_id,
                f_player_id=f_player_id
                )
        db.session.add(f_offense_player)
        db.session.commit()

        
    def return_nfl_player_id(self, first_name, last_name, uniform_number, team):
        nfl_player=NFL_Player.query.filter_by(first_name=first_name, last_name=last_name,
                uniform_number=uniform_number, team=team.upper()).first()
        if not nfl_player:
            raise Exception('Could not match NFL Player for '+ first_name+' '+last_name + ', '+ team+ ' , ' + uniform_number)
        else:
            return nfl_player.player_id
    
    #Return current week of NFL season
    def return_current_week(self):
        week=Week_Lookup.query.all()
        #for w in week:
        #    if w.start_date <= datetime.now().date() and w.end_date >= datetime.now().date():
        #        return w.week_num
        #    else:
        #        raise Exception('Current week is not a part of regular season')
        tmp = list()
        for w in week:
            if w.start_date <= datetime.now().date() <= w.end_date:
                tmp.append(w.week_num)
            #else:
            #    raise Exception('Current week is not a part of regular season')
        assert len(tmp) is 1
        return tmp[0]



    # only one league per user for now. Let's still write it to work for many leagues
    #Return league_id, num_teams and start_date
    def return_league_info(self):
        # KEY = league_id, VALS= num_teams and start_date
        dict_league={}
        if session["user_id"]:
            league=F_League.query.filter_by(user_id=session["user_id"]).all()
            for l in league:
                    dict_league[l.league_id]={"num_teams":l.num_teams, "start_date":l.start_date}
            
        else:
            raise Exception('Must be logged in to return league info')

    
    #RETURN F TEAM ID BY YAHOO LEAGUE ID AND YAHOO TEAM ID     
    def return_f_team_id(self,yahoo_league_id, yahoo_team_id ):
        assert yahoo_league_id is not None
        assert yahoo_team_id is not None
        f_league = F_League.query.filter_by(yahoo_league_id=yahoo_league_id).first()
        f_league_id = f_league.league_id
        f_team= F_Team.query.filter_by(league_id=f_league_id, yahoo_team_id=yahoo_team_id).first()
        f_team_id=f_team.f_team_id
        if f_team_id:
            return f_team_id
        else:
            raise Exception('F_Team_ID doesnt exist')
    
    def return_last_f_player_id(self):
        #for some reason this breaks and doesn't work. Have to figure out why it returns NoneType. Doing it the hacky way. 
        """
        last_f_player_id=F_Player.query.order_by(F_Player.f_player_id.desc()).first()
        if not last_f_player_id:
            raise Exception ('bad last f_player id')
        else:
            return last_f_player_id
        """
        last_f_player_id=F_Player.query.all()
        return last_f_player_id[-1].f_player_id

    def insert_f_team_points_per_week(self,f_team_points_dict):
        f_team_id=self.return_f_team_id(yahoo_league_id=f_team_points_dict['yahoo_league_id'],
                yahoo_team_id=f_team_points_dict['yahoo_team_id'])
        f_team_points_per_week_exists= F_Team_Points_Per_Week.query.filter_by(f_team_id=f_team_id, week_num=f_team_points_dict['week_num']).first()
        if not f_team_points_per_week_exists:
            f_team_points_per_week=F_Team_Points_Per_Week(
                f_team_id=f_team_id,
                points=f_team_points_dict['points'],
                projected_points=f_team_points_dict['projected_points'],
                week_num=f_team_points_dict['week_num']
                )
            
            print "COMMITTING NEW f_team_points_per_week"
            print "f_team_id: %s week_num: %s proj_pts: %s pts: %s" % (
                    f_team_id,
                    f_team_points_dict['week_num'],
                    f_team_points_dict['projected_points'],
                    f_team_points_dict['points'] )
            print "~" * 20
            db.session.add(f_team_points_per_week)
            db.session.commit()
        else:
            f_team_points_per_week_exists.points=f_team_points_dict['points']
            print"COMMITTING UPDATE f_team_points_per_week"
            print "f_team_id: %s" % f_team_points_per_week_exists.f_team_id
            print "week_num: %s" % f_team_points_per_week_exists.week_num
            print "points: %s" % f_team_points_per_week_exists.points
            print "~" * 20
            db.session.commit()


    def insert_f_league_matchups(self,all_teams_matchups_dict):
        player1_f_team_id=self.return_f_team_id(yahoo_league_id=all_teams_matchups_dict['yahoo_league_id'],
                yahoo_team_id=all_teams_matchups_dict['player1_f_team_id'])
        
        player2_f_team_id=self.return_f_team_id(yahoo_league_id=all_teams_matchups_dict['yahoo_league_id'],
                yahoo_team_id=all_teams_matchups_dict['player2_f_team_id'])
        
        duplicate_matchup=F_Matchup.query.filter_by(week_num=all_teams_matchups_dict['week_num'],
                opponent1_f_team_id=player2_f_team_id, opponent2_f_team_id=player1_f_team_id).first()

        exists_in_db=F_Matchup.query.filter_by(week_num=all_teams_matchups_dict['week_num'],
                opponent1_f_team_id=player1_f_team_id, opponent2_f_team_id=player2_f_team_id).first()
        
        #not a duplicate matchup 
        if not duplicate_matchup and not exists_in_db:
            f_matchup=F_Matchup(opponent1_f_team_id=player1_f_team_id,
                    opponent2_f_team_id=player2_f_team_id,
                    week_num=all_teams_matchups_dict['week_num']
                    )
            db.session.add(f_matchup)
            db.session.commit()

    def import_player_stats(self, player_points_dict):
        points_dict={}
        #print player_points_dict.keys()
        for k,v in player_points_dict.iteritems():
            if k!='meta':
                points_dict=dict(player_first_name=v['name']['first'], player_last_name=v['name']['last'],
                    player_team_abbr=v['editorial_team_abbr'], player_selected_position=v['selected_pos'],
                    player_uniform_number=v['uniform_number'], player_points=v['player_points'],
                    week_num=player_points_dict['meta']['current_week'], team_key=player_points_dict['meta']['team_key'])
                
                print "teamkey:%s week:%s first:%s last:%s sel_pos:%s team_abbr:%s" % (player_points_dict['meta']['team_key'],
                        player_points_dict['meta']['current_week'],
                        v['name']['first'], v['name']['last'], v['selected_pos'], v['editorial_team_abbr'] )
                
                self.insert_f_player_weekly_points(points_dict=points_dict)
    
    def insert_f_player_weekly_points(self, points_dict):
        #list[0] --> yahoo_league_id, list[1]-->yahoo_team_id
        team_key=points_dict['team_key']
        list_yahoo_league_team_ids=self.get_yahoo_league_id_and_team_id(team_key=team_key)
        yahoo_league_id=list_yahoo_league_team_ids[0]
        yahoo_team_id=list_yahoo_league_team_ids[1]
        f_team_id=self.return_f_team_id(yahoo_league_id=yahoo_league_id, yahoo_team_id=yahoo_team_id)
        if points_dict['player_uniform_number']==False:
            #def player
            #print "%s %s %s" % (points_dict['player_first_name'], points_dict['player_last_name'], points_dict['player_team_abbr'])
            f_player_id=self.get_def_f_player_id(f_team_id=f_team_id, team_id=points_dict['player_team_abbr'].upper())
        else:
            nfl_player_id=self.return_nfl_player_id(first_name=points_dict['player_first_name'], last_name=points_dict['player_last_name'],
                uniform_number=points_dict['player_uniform_number'], team=points_dict['player_team_abbr'])
            f_player_id=self.get_offense_f_player_id(nfl_player_id=nfl_player_id, f_team_id=f_team_id)
        #check if combo of f_player_id and week_num already exists, if it does -->>>> update, else insert in f_player_points_per_week
        f_player_points_per_week_exists= F_Player_Points_Per_Week.query.filter_by(f_player_id=f_player_id, week_num=points_dict['week_num']).first()
        if f_player_points_per_week_exists:
            #update 
            f_player_points_per_week_exists.points=points_dict['player_points']
            db.session.commit()
        else:
            #insert in db
            f_player_points_per_week=F_Player_Points_Per_Week(
                    f_player_id=f_player_id,
                    week_num=points_dict['week_num'],
                    points=points_dict['player_points']
                    )
            db.session.add(f_player_points_per_week)
            db.session.commit()
        

    def get_offense_f_player_id(self, nfl_player_id, f_team_id):
        print "getting offense f_player_id for: "
        get_f_player_id = db.session.query(
                F_Player.f_player_id, F_Player.f_team_id, F_Offense_Player.player_id).filter(
                F_Player.f_player_id==F_Offense_Player.f_player_id).filter(
                F_Player.f_team_id==f_team_id).filter(
                F_Offense_Player.player_id==nfl_player_id).first()
        
        return get_f_player_id.f_player_id

    def get_def_f_player_id(self, team_id, f_team_id):
        try:
            get_f_player_id=db.session.query(F_Player.f_player_id, F_Player.f_team_id, F_Def_Player.team_id).\
                filter(F_Player.f_player_id==F_Def_Player.f_player_id).filter(F_Player.f_team_id==f_team_id).filter(F_Def_Player.team_id==team_id).first()
            return get_f_player_id.f_player_id
        except Exception:
            raise Exception('F_Def_Player does not exist with team_id: %s f_team_id: %s' % (team_id, f_team_id) )

    def get_yahoo_league_id_and_team_id(self, team_key):
        list=team_key.split('.')
        list_yahoo_league_team_ids=[list[2], list[4]]
        return list_yahoo_league_team_ids 
            
    def load_roto_players_dict(self, rss_dict):
        self.reset
        self.rss_dict = rss_dict
        self._insert_roto_players(self.rss_dict)

    def load_yahoo_rss_dict(self, rss_dict):
        self.reset
        self.rss_dict = rss_dict
        self._insert_yahoo_rss_feed(self.rss_dict)

    def load_roto_rss_dict(self, rss_dict):
        self.reset
        self.rss_dict = rss_dict
        self._insert_roto_rss_feed(self.rss_dict)
    
    def brians_import_league_info(self, f_league_dict):
        """ =) """
        self.insert_f_league(f_league_dict)
        pass

    def brians_import_user_info(self, user_id, user_guid):
        """
        here's the old call:
        yahoo_db.insert_yahoo_user_guid(user_id=session['user_id'], yahoo_guid=user_guid)
        user_id = session['user_id']
        """
        self.insert_yahoo_user_guid(user_id=user_id, yahoo_guid=user_guid)
        pass

    def brians_import_user_info_v2(self, user_id, list_of_user_dicts):
        """inserts data in to f_league. takes list of league dicts and
        creates a new dictionary with required data to be fed in to
        self._insert_f_league_v2
        
        """
        for leagues in list_of_user_dicts:
            for k, v in leagues.iteritems():
                f_league_dict = {
                        'user_id': user_id,
                        'yahoo_league_id': v['league_id'],
                        'start_date' : v['start_date'],
                        'end_date': v['end_date'],
                        'num_teams': v['num_teams'],
                        'league_url': v['league_url'],
                        'league_name': v['league_name'],
                        'game_key': v['game_key'],
                        'season_year': v['season_year']
                        }
                self.insert_f_league_v2(f_league_dict)
        
        pass
    
            
    def brians_import_team_stats(self, stats_dict):
        """:-). 
        call this from views.py like this: yahoo_db_helper = Db_Helper()

        yahoo_parser = YahooHelper()
        yahoo_parser.import_json_data(data, arg='team_stats')
        data_dict = yahoo_parser.return_data()
        yahoo_db_helper.brians_import_fnc(data_dict)
        
        """
        assert stats_dict is not None
        key_list = stats_dict.keys()
        for k in key_list:
            if k!='meta':
                team_points_dict = {}
                all_teams_matchups_dict = {}
                yahoo_team_id = stats_dict[k]['team_id']
                yahoo_league_id = stats_dict['meta']['league_id']
                total_points = stats_dict[k]['total_points']
                projected_points = stats_dict[k]['projected_points']
                week_num = stats_dict['meta']['current_week']
                ## ^^ THIS MAY BE WRONG?
                team_points_dict = dict(
                        yahoo_league_id = yahoo_league_id,
                        yahoo_team_id = yahoo_team_id,
                        points = total_points,
                        projected_points = projected_points,
                        week_num = week_num
                        )
                #pass dictionary to insert_f_team_points_per_week function 
                #yahoo_db_helper.insert_f_team_points_per_week(team_points_dict)
                self.insert_f_team_points_per_week(team_points_dict)
                ########^^^^^^^^ DA MAGIC HERE

                #pass dictionary to insert_f_matchups function
                all_teams_matchups_dict = dict(player1_f_team_id=stats_dict[k]['team_id'],
                        player2_f_team_id = stats_dict[stats_dict[k]['opp_team_key']]['team_id'],
                        yahoo_league_id = yahoo_league_id, week_num=week_num)
                
                #yahoo_db_helper.insert_f_league_matchups(all_teams_matchups_dict)
                self.insert_f_league_matchups(all_teams_matchups_dict)
                #########^^^^^^^^^ DA MAGIC HERE

    def _insert_yahoo_rss_feed(self, rss_dict):
        assert rss_dict is not None
        for k,v in rss_dict.iteritems():
            title = v['title']
            url = v['url']
            content_1 = v['content_1']
            content_2 = v['content_2']
            datetime = v['datetime']
            rss_id = v['rss_id']
            media_url = v['media_url']
            media_inf = v['media_inf']
            
            previous_data = Yahoo_RSS_Data.query.filter_by(rss_id = rss_id).first()
            if not previous_data:
                rss_data = Yahoo_RSS_Data(
                        rss_id = rss_id,
                        title = title,
                        url = url,
                        content_1 = content_1,
                        content_2 = content_2,
                        timestamp = datetime,
                        media_url = media_url,
                        media_inf = media_inf
                        )
                db.session.add(rss_data)
                db.session.commit()

    def _insert_roto_players(self, rss_dict):
        
        for k, v in rss_dict.iteritems():
            title = v['title']
            content = v['content']
            player_url = v['player_url']
            full_name = v['full_name']
            first_name = v['first_name']
            last_name = v['last_name']
            team_abbr = v['team_abbr']
            rss_id = v['rss_id']
            timestamp = v['timestamp']

            previous_data = Roto_RSS_Player_Data.query.filter_by(rss_id = rss_id).first()
            if not previous_data:
                rss_data = Roto_RSS_Player_Data(
                        title = title,
                        content = content,
                        player_url = player_url,
                        full_name = full_name,
                        first_name = first_name,
                        last_name = last_name,
                        team_abbr = team_abbr,
                        rss_id = rss_id,
                        timestamp = timestamp
                        )
                db.session.add(rss_data)
                db.session.commit()

    
    def _insert_roto_rss_feed(self, rss_dict):
        
        for k, v in rss_dict.iteritems():
            title = v['title']
            url = v['url']
            content = v['content']
            timestamp = v['ts']
            rss_id = v['rss_id']
            
            previous_data = Roto_RSS_Data.query.filter_by(rss_id = rss_id).first()
            if not previous_data:
                rss_data = Roto_RSS_Data(
                        rss_id = rss_id,
                        title = title,
                        content_1 = content,
                        url = url,
                        timestamp = timestamp
                        )
                db.session.add(rss_data)
                db.session.commit()


    #get all offense_players on your roster
    #1. joing f_league with f_team on league_id with f_player with f_offense player to get only players on your roster
    #2. filter through only players on roster
    #3. get their nfl_player_id only if last_sign_out <= status_update date 
    def get_player_status_updates(self,user_id):
        get_players_status_updates_for_f_team=db.session.query(User.last_sign_out, F_League, F_Team, F_Player, F_Offense_Player.player_id, NFL_Player_Status_Update.date,NFL_Player.full_name,\
            NFL_Player.uniform_number, NFL_Player.team).filter(User.user_id==F_League.user_id).filter(F_League.league_id==F_Team.league_id).filter(F_Team.f_team_id==F_Player.f_team_id).\
            filter(F_Player.f_player_id==F_Offense_Player.f_player_id).filter(F_Offense_Player.player_id==NFL_Player_Status_Update.nfl_player_id).\
            filter(F_Offense_Player.player_id==NFL_Player.player_id).filter(F_League.user_id==user_id).filter(NFL_Player_Status_Update.date >= User.last_sign_out).all()
         
        return get_players_status_updates_for_f_team
        

    #get f_team_points_per_week 
    #1. join f_team with f_team_points_per_Week on f_team_id  
    def get_f_team_points_per_week(self, f_team_id, week_num):
        f_team_points_per_week= db.session.query(F_Team.team_name,F_Team_Points_Per_Week.points, F_Team_Points_Per_Week.week_num, F_Team_Points_Per_Week.projected_points).\
                filter(F_Team.f_team_id==F_Team_Points_Per_Week.f_team_id).filter(F_Team.f_team_id==F_Matchup.opponent1_f_team_id).filter(F_Team.f_team_id==f_team_id).\
                filter(F_Team_Points_Per_Week.week_num==week_num).all()
        return f_team_points_per_week_exists
        #access as for i in f_team_points_per_week:
        # i.team_name << your team name, i.points , i.projected_points, i.week_num

    #get weekly matchups, only returns player and opponent f_team_id's. You can run each one thru get_f_team_name_per_week to get team name
    #and that teams points
    def get_f_matchup(self, f_team_id, week_num):
        f_matchup=db.session.query(F_Team.f_team_id,F_Matchup.opponent1_f_team_id, F_Matchup.opponent2_f_team_id).filter((F_Team.f_team_id==F_Matchup.opponent1_f_team_id)|\
                ( F_Team.f_team_id==F_Matchup.opponent2_f_team_id)).filter(F_Team.f_team_id==f_team_id). filter(models.F_Matchup.week_num==week_num).all()
        return f_matchup

    def get_f_player_points_per_week(self, f_team_id, week_num):
        f_player_points_per_week= db.session.query(F_Player, F_Offense_Player.player_id, NFL_Player.first_name,NFL_Player.last_name,NFL_Player.team, F_Player_Points_Per_Week.points,\
                F_Player_Points_Per_Week.week_num).filter(F_Player.f_player_id==F_Offense_Player.f_player_id).filter(F_Offense_Player.f_player_id==F_Player_Points_Per_Week.f_player_id).\
                filter(F_Offense_Player.player_id==NFL_Player.player_id).filter(F_Player.f_team_id==f_team_id).filter(F_Player_Points_Per_Week.week_num==week_num).all()

        return f_player_points_per_week
        #access as follows: for f in f_player_points_per_week:  f.player_id, f.team, f.points, f.week_num


