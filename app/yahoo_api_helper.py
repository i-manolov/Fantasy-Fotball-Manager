import re
import json
#try:
#from app import db
#except ImportError:
    #from flask import Flask
    #from flask.ext.sqlalchemy import SQLAlchemy
    #app = Flask(__name__)
    #db = SQLAlchemy(app)
try:
    from models import *
    from flask import session
    from yahoo_db_helper import *
except ImportError:
    # this should only happen during unit testing
    print "SOMETHING WENT WRONG DURING IMPORT"

class YahooHelper(object):
    """this helper class parses yahoo API JSON data and returns
    massaged data to be inserted into postgresql.
    
    user info -> league_info -> team_info -> player_info.
    this class should be re-instantiated for EVERY API call.
    I'm dumb. added self.__init__() call during each import_json_data.
    """
    def __init__(self):
        """
        self.data holds the yahoo PROCESSED  JSON object which has not been parsed.
        self.get holds the parameter passed in from view that tells this
        object what type of API call has been made.
        
        self.yahoo_leagues_data, self.yahoo_players_data, self.yahoo_teams_data 
        holds the parsed JSON data waiting to be inserted in to the database.
        
        self.yahoo_league_id will hold all yahoo league id's in a list. if the
        user has more than one league, it will simply be appended to the list.
        
        self.yahoo_team_id will hold yahoo_league_id + team_id. same as above,
        will be returned as a list and additional team_id's will be appended to
        the list. yahoo_team id is yahoo_league_id + team_id because team_id is 
        simply an integer that does not uniquely identify team.
        """
        self.data = None
        self.get = None
        
        self.yahoo_leagues_data = None
        self.yahoo_teams_data = None
        self.yahoo_players_data = None

        self.yahoo_league_id = None
        self.yahoo_team_id = None

    
    def return_data(self):
        """seems hacky. figures out what to return given arg input in views.py"""
        if self.get.lower() == 'teams':
            return self._parse_teams_data()
        if self.get.lower() == 'players':
            return self._parse_players_data()
        if self.get.lower() == 'players_v2':
            return self._parse_players_data_v2()
        if self.get.lower() == 'leagues':
            return self._parse_leagues_data()
        if self.get.lower() == 'user':
            return self._parse_user_data()
        if self.get.lower() == 'user_v2':
            return self._parse_user_data_v2()
        if self.get.lower() == 'team_stats':
            return self._parse_league_matchups()
        if self.get.lower() == 'weekly_stats':
            return self._parse_weekly_player_stats()
        else:
            raise Exception('something bad happened in return_data function')


    def import_json_data(self, json_data, get):
        """
        takes Yahoo JSON data as input. checks to see if the get=arg is valid 
        """
        accepted_args = [
                'user', 'players','players_v2', 'leagues', 
                'teams', 'team_stats', 'player_stats',
                'weekly_stats', 'user_v2'
                ]
        if get.lower() not in accepted_args:
            raise Exception('something is wrong with arg passed in')
        else:
            self.__init__() # clear the class variables
            self.get = get.lower()
        if json_data is not None:
            self.data = json_data
        else:
            raise Exception('no data was passed in, soemthing is wrong')

    def _parse_yahoo_team_id(self):
        """this method is used to parse yahoo_team_id. this value should actually be
        yahoo_league_id + team_id because team_ids are simply a number between 0-10
        if there are 10 people in the league so it is not unique."""
        pass

    def _parse_weekly_player_stats(self):
        """parses weekly stats for players on team 
        player_id => name, score
        
        """
        data = self.data
        prefix = data['fantasy_content']['team']
        want_meta = [u'team_key', u'team_id', u'name', u'url']
        meta_dict = dict()
        # stores in to meta_dict if data.keys() == want_meta
        for data in prefix[0]:
            if type(data) is dict:
                for item in want_meta:
                    if item in data.keys():
                        meta_dict[item] = data[item]
        data_dict = dict()
        players = prefix[1]['roster']['0']['players']
        current_week = prefix[1]['roster']['week']
        meta_dict['current_week'] = current_week
        for keys in players.keys():
            if keys != u'count':# and keys == u'0':
                a = {}
                for item in players[keys]['player']: # passed in keys from u'0' to u'14'
                    if type(item) is list and len(item) != 0:
                        for i in range(0, len(item)):
                            if type(item[i]) is dict:
                                for k, v in item[i].iteritems():
                                    if item[i].has_key(u'editorial_player_key'):
                                        a[u'player_key'] = v
                                        player_key = v
                                    if item[i].has_key(u'name'):
                                        a[u'name'] = v
                                        # more stupidness
                                        if a[u'name']['first'] == 'Stevie':
                                            a[u'name']['first'] = 'Steve'
                                        if a[u'name']['last'] == 'Shorts III':
                                            a[u'name']['last'] = 'Shorts'
                                        if a[u'name']['first'] == 'Giovani':
                                            a[u'name']['first'] = 'Gio'
                                    
                                    if item[i].has_key(u'editorial_team_full_name'):
                                        a[u'editorial_team_full_name'] = v
                                    if item[i].has_key(u'editorial_team_abbr'):
                                        a[u'editorial_team_abbr'] = v
                                        # stupid
                                        if a[u'editorial_team_abbr'] == 'Jax':
                                            a[u'editorial_team_abbr'] = 'JAC'
                                    if item[i].has_key(u'uniform_number'):
                                        a[u'uniform_number'] = v
                                    if item[i].has_key(u'eligible_positions'):
                                        a[u'eligible_positions'] = v
                                    if item[i].has_key(u'headshot'):
                                        a[u'headshot'] = v
                                    if item[i].has_key(u'bye_weeks'):
                                        a[u'bye_weeks'] = v
                                    if item[i].has_key("display_position"):
                                        a[u'display_position'] = v
                    if type(item) is dict:
                        if item.has_key(u'player_points'):
                            points = item['player_points']['total']
                            a[u'player_points'] = points
                        if item.has_key(u'selected_position'):
                            # this is the field that tells if player is BN
                            selected_pos = item['selected_position'][1]['position']
                            a[u'selected_pos'] = selected_pos
            data_dict[player_key] = a
        data_dict['meta'] = meta_dict
         
        return data_dict


    
    def _parse_league_matchups(self):
        """parses yahoo league's scoreboard.
        From JSON data, loops over the amount of matches e.g. if there are 10 players
        in the league, there will always be 5 matchups per week. and there are always
        2 participants to a matchup. Loops over each respective key,index and stores
        data in a new dictionary where: 
        {
        league_id => {
                        stat_1 : val_1,
                        stat_2 : val_2
                     }
        meta =>     {
                        league_name: val_x,
                        current_week: val_y
                    }            
        }
        the stats_dict consists of team_keys that return data for that specific team
        and a 'META' key whose values are meta data pertaining to all the teams.
        """
        assert self.data is not None
        data = self.data
        league_prefix = data['fantasy_content']['league'][0]
        
        league_name = league_prefix["name"]
        league_id=league_prefix['league_id']
        league_type = league_prefix["league_type"]
        last_update_timestamp = league_prefix["league_update_timestamp"]
        num_teams = league_prefix["num_teams"]
        scoring_type = league_prefix["scoring_type"]
        #current_week = league_prefix["current_week"]
        current_week = data['fantasy_content']['league'][1]['scoreboard']['week']
        scoreboard = data['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
        num_of_matchups = scoreboard['count']
        index = range(int(num_of_matchups))
        
        list_of_winners = list() # list of team_id for winners of the week
        stats_dict = dict() # mega important dictionary. key(team_id) -> ALL IMPORTANT VALUES
        for i in index:
            try:
                # this will not exist if there is no winner yet.
                list_of_winners.append(scoreboard[str(i)]['matchup']['winner_team_key'])
            except KeyError:
                list_of_winners.append("NULL")
            prefix = scoreboard[str(i)]['matchup']
            assert len(prefix['0']) == 1 # making sure it's only 1
            assert len(prefix['0']['teams']) == 3 # it's only 0,1,count
            # make sure count == 3 - 1
            assert (len(prefix['0']['teams'])-1) == (prefix['0']['teams']['count'])
            team = prefix['0']['teams']
            for j in range(len(team)-1):
                team_data = team[str(j)]['team'][0]
                scores_data = team[str(j)]['team'][1]
                team_key = team[str(j)]['team'][0][0]['team_key'] # used to test.
                
                if str(j) == '0':
                    # there are 2 children in a matchup 
                    # if you are the first child in the matchup, your opp is:
                    opp_team_key = team[(str(j+1))]['team'][0][0]['team_key']
                elif str(j) == '1':
                    # you are the second child.
                    opp_team_key = team[(str(j-1))]['team'][0][0]['team_key']
                else:
                    raise Exception('j is not 1 or 2 wtf')
                assert team_key is not opp_team_key
                
                stats_dict[(team_key)] = {
                        # create a dictionary where key = yahoo_team_id
                        'team_id': team_data[1]['team_id'],
                        'opp_team_key': opp_team_key,
                        'team_name': team_data[2]['name'],
                        'url': team_data[4]['url'],
                        'logo_url': team_data[5]['team_logos'][0]['team_logo']['url'],
                        'num_moves': team_data[9]['number_of_moves'],
                        'num_trades': team_data[10]['number_of_trades'],
                        'guid': team_data[13]['managers'][0]['manager']['guid'],
                        'nickname': team_data[13]['managers'][0]['manager']['nickname'],
                        'projected_points': scores_data['team_projected_points']['total'],
                        'total_points' : scores_data['team_points']['total']
                        }

        stats_dict['meta'] = {
                'league_name': league_name,
                'league_id':league_id,
                'league_type': league_type,
                'last_updated_timestamp': last_update_timestamp,
                'num_teams': num_teams,
                'scoring_type': scoring_type,
                'current_week': current_week,
                'list_of_winners' : list_of_winners # this is a list
                }        
        
        #got all this data. what to do with it?! FUN TIMEEEEEEEEEEEEE with Db_Helper
        #summon the beast
        """
        yahoo_db_helper=Db_Helper()
        key_list=stats_dict.keys()
        for k in key_list:
            if k!='meta':
                team_points_dict={}
                all_teams_matchups_dict={}
                yahoo_team_id=stats_dict[k]['team_id']
                yahoo_league_id=stats_dict['meta']['league_id']
                total_points=stats_dict[k]['total_points']
                projected_points=stats_dict[k]['projected_points']
                week_num=stats_dict['meta']['current_week']

                team_points_dict=dict(yahoo_league_id=yahoo_league_id,
                       yahoo_team_id=yahoo_team_id, points=total_points,
                       projected_points=projected_points,week_num=week_num)
                #pass dictionary to insert_f_team_points_per_week function 
                yahoo_db_helper.insert_f_team_points_per_week(team_points_dict)
                
                #pass dictionary to insert_f_matchups function
                all_teams_matchups_dict=dict(player1_f_team_id=stats_dict[k]['team_id'], 
                        player2_f_team_id=stats_dict[stats_dict[k]['opp_team_key']]['team_id'],
                        yahoo_league_id=yahoo_league_id,week_num=week_num )
                yahoo_db_helper.insert_f_league_matchups(all_teams_matchups_dict)
                
        """
        ## shuold return dictionary:
        return stats_dict
        #return stats_dict.keys(), stats_dict.values() # ,teams_dict.values()
    
    
    def _parse_user_data(self):
        """this method is called the first time the user registers for our site. this
        will parse users metadata and retrieve all the users league_ids and team_ids.
        from league_id and team_id, we construct yahoo_team_id which will uniquely
        identify a users team within a league. with yahoo_team_id, we can send API
        call and find all yahoo_player data within that league.
        
        read _parse_user_data_v2
        """
        assert self.data is not None
        data = self.data
        try:
            prefix = data['fantasy_content']['users']['0']['user']
            user_guid = prefix[0]['guid']
            # handled in get_user
            #league_id = prefix[1]['games']['0']['game'][1]['leagues']['0']['league'][0]['league_key']
            
            """
            league_id= data['fantasy_content']['users']['0']['user'][1]['games']['0']['game'][1]['leagues']['0']['league'][0]['league_key']
            user_guid= data['fantasy_content']['users']['0']['user'][0]['guid']
            yahoo_db= Db_Helper()
            yahoo_db.insert_yahoo_user_guid(user_id=session['user_id'], yahoo_guid=user_guid)
            """

        except Exception as e:
            raise Exception(e)

        #return league_id, user_guid
        return user_guid

    def _parse_user_data_v2(self):
        """returns a list of user_dicts. all data necessary for get_league
        is available. eliminate the need for get_league API call """
        data = self.data
        fc = data['fantasy_content']
        uc = fc['users']
        games_dict = uc['0']['user'][1]['games']
        yahoo_user_guid = uc['0']['user'][0]['guid']
        # change this to any other sport: nfl, nba, mlb
        accepted_game_types = ['pnfl', 'nfl']
        
        list_of_dicts = list()
        for key in games_dict.keys(): # pass in value of keya
            if key != 'count':
                for item in games_dict[key]:
                    if games_dict[key].has_key("game"):
                        l_of_leagues = games_dict[key]['game']
                        assert type(games_dict[key]['game']) is list
                        assert type(l_of_leagues) is list
                        assert len(l_of_leagues) == 2
                        if l_of_leagues[0]['code'] in accepted_game_types:
                            for k, v in l_of_leagues[1]['leagues'].iteritems():
                                if k != u'count':
                                    # yes this is extra long for no reason
                                    league_dict = {}
                                    game_key = l_of_leagues[0]['game_key']
                                    season_year = l_of_leagues[0]['season']
                                    _type = l_of_leagues[0]['type']
                                    league_id = v['league'][0]['league_id']
                                    league_type = v['league'][0]['league_type']
                                    start_week = v['league'][0]['start_week']
                                    end_week = v['league'][0]['end_week']
                                    league_name = v['league'][0]['name']
                                    start_date = v['league'][0]['start_date']
                                    end_date = v['league'][0]['end_date']
                                    num_teams = v['league'][0]['num_teams']
                                    league_url = v['league'][0]['url']
                                    
                                    league_dict[league_id] = {
                                        'game_key': game_key,
                                        'season_year': season_year,
                                        'type': _type,
                                        'league_name': league_name,
                                        'league_id': league_id,
                                        'league_type': league_type,
                                        'start_week': start_week,
                                        'end_week': end_week,
                                        'league_url': league_url,
                                        'start_date': start_date,
                                        'end_date': end_date,
                                        'num_teams': num_teams
                                        }
                                    list_of_dicts.append(league_dict)

        #need to return a list of dicts
        return list_of_dicts


    def _parse_players_data_v2(self):
        """this is beautiful isn't it? nested fruit loops """
        assert self.data is not None
        data = self.data
        data_dict = {}
        meta = {}

        team_key = data['fantasy_content']['team'][0][0]['team_key']
        list_team_key = team_key.split('.')
        yahoo_league_id = list_team_key[2]
        yahoo_team_id = list_team_key[4]
        meta['team_key'] = team_key
        meta['league_id'] = yahoo_league_id
        meta['team_id'] = yahoo_team_id
        players = data['fantasy_content']['team'][1]['roster']['0']['players']

        for key in players.keys():
            if key != u'count':
                a = {}
                for item in players[key]['player']:
                    if type(item) is list and len(item) != 0:
                        for i in range(0, len(item)):
                            if type(item[i]) is dict:
                                for k, v in item[i].iteritems():
                                    if item[i].has_key(u"player_key"):
                                        a[u'player_key'] = v
                                        player_key = v
                                    if item[i].has_key(u"player_id"):
                                        a[u'player_id'] = v
                                    if item[i].has_key(u"name"):
                                        a[u'name'] = v
                                        # retarded shit
                                        if v['first'] == 'Stevie':
                                            a[u'first_name'] = 'Steve'
                                            a[u'first_name_ascii'] = 'Steve'
                                            a[u'last_name'] = v['last']
                                            a[u'last_name_ascii'] = v['ascii_last']
                                        elif v['last'] == 'Shorts III':
                                            a[u'first_name'] = v['first']
                                            a[u'first_name_ascii'] = v['ascii_first']
                                            a[u'last_name'] = 'Shorts'
                                            a[u'last_name_ascii'] = 'Shorts'
                                        elif v['first'] == 'Giovani':
                                            a[u'first_name'] = 'Gio'
                                            a[u'first_name_ascii'] = 'Gio'
                                            a[u'last_name'] = v['last']
                                            a[u'last_name_ascii'] = v['ascii_last']
                                        else:
                                            a[u'first_name'] = v['first']
                                            a[u'last_name'] = v['last']
                                            a[u'first_name_ascii'] = v['ascii_first']
                                            a[u'last_name_ascii'] = v['ascii_last']
                                    if item[i].has_key(u"editorial_player_key"):
                                        a[u'editorial_player_key'] = v
                                    if item[i].has_key(u"editorial_team_key"):
                                        a[u'editorial_team_key'] = v
                                    if item[i].has_key(u"editorial_team_full_name"):
                                        a[u'editorial_team_full_name'] = v
                                    if item[i].has_key(u"editorial_team_abbr"):
                                        #if v[u"editorial_team_abbr"] == 'JAX' or 'jax':
                                        #    a[u"editorial_team_abbr"] = 'JAC'
                                        #else:
                                        a[u'editorial_team_abbr'] = v
                                        if a[u'editorial_team_abbr'] == 'Jax':
                                            a[u'editorial_team_abbr'] = 'JAC'
                                        #print a[u'editorial_team_abbr']
                                    if item[i].has_key(u"bye_weeks"):
                                        a[u'bye_weeks'] = v
                                    if item[i].has_key(u"uniform_number"):
                                        a[u'uniform_number'] = v
                                    if item[i].has_key(u"display_position"):
                                        a[u'display_position'] = v
                                    if item[i].has_key(u"image_url"):
                                        a[u'image_url'] = v
                                    if item[i].has_key(u"headshot"):
                                        a[u'headshot'] = v
                                    if item[i].has_key(u"eligible_positions"):
                                        a[u'eligible_positions'] = v
                                    if item[i].has_key(u"is_undroppable"):
                                        a[u'is_undroppable'] = v
                                    if item[i].has_key(u"position_type"):
                                        a[u'position_type'] = v
                    if type(item) is dict:
                        if item.has_key(u"selected_position"):
                            a[u'selected_position'] = item["selected_position"]
            data_dict[player_key] = a
        data_dict['meta'] = meta

    # this is what should be using 
    # yahoo_db_helper.insert_f_player(f_player_dict)
        return data_dict
     

    def _parse_players_data(self):
        """get all the yahoo players ROSTER. should be passing in the
        team key (i.e nfl.l.1173612.t.8)
        RETURNS : yahoo_team_key ( needs to be parsed into yahoo_league, yahoo team_id later),
        yahoo_first_name, yahoo_last_name, uniform_num, team_name for each, yahoo_player_key
        """
        assert self.data is not None
        data=self.data

        
        #dictionary to hold values necessary for f_player, f_def_player, and f_offense_player
        f_player_dict={}
        try:
            team_key=data['fantasy_content']['team'][0][0]['team_key']
            #need to parse thru string to get yahoo_league_id and yahoo_team_id to get team_id. Change to list. Split on '.'. Access by index values
            list_team_key=team_key.split('.')
            yahoo_league_id=list_team_key[2]
            yahoo_team_id=list_team_key[4]
        
            #Get number of players in you team. Create a list of string values within range of player count
            player_count= data['fantasy_content']['team'][1]['roster']['0']['players']['count']
            index= range(player_count)
            index=[str(i) for i in index]
            
            f_player_position=None
            f_player_uniform_number=None
            f_player_team_abbr=None

            #Not sure if nfldb player table stores values as unicode or just ascii so i will parse both
            for i in index:
                f_player_first_name=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['first']
                f_player_first_name_ascii=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['ascii_first']
                f_player_last_name=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['last']
                f_player_last_ascii=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['ascii_last']
            
                #need another for loop to get nfl team and uniform number. 
                #WARNING: Json structure differs from player to player_info
                j=len(data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0])
                index_j=range(j-1)
                for ind in index_j:
                    d=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][ind]
                    if type(d)==dict:
                        if d.has_key('editorial_team_abbr'):
                            for key, val in d.iteritems():
                                f_player_team_abbr = val
                        if d.has_key('uniform_number'):
                            for key, val in d.iteritems():
                                f_player_uniform_number = val
                        if d.has_key('display_position'):
                            for key, val in d.iteritems():
                                f_player_position = val
                
                # function to return f_team_id for f_player 
                print 'yahoo_league_id: %s' % yahoo_league_id
                print 'yahoo_team_id: %s' % yahoo_team_id
                yahoo_db_helper=Db_Helper()
                f_team_id=yahoo_db_helper.return_f_team_id(yahoo_league_id, yahoo_team_id)
                   
                #clear dictionary for next call
                f_player_dict={}
               
                f_player_dict=dict(
                            f_team_id=f_team_id,
                            f_player_first_name=f_player_first_name,
                            f_player_last_name=f_player_last_name,
                            f_player_first_name_ascii=f_player_first_name_ascii,
                            f_player_last_ascii=f_player_last_ascii,
                            f_player_team_abbr=f_player_team_abbr.upper(),
                            f_player_uniform_number=f_player_uniform_number,
                            f_player_position=f_player_position
                            )
                yahoo_db_helper.update_f_player(f_player_dict)                                  

        except Exception as e:
            raise Exception(e)
        

    def _parse_leagues_data(self):
        """This function is used to parse processed json data for get_league.
        Returns: league_name, yahoo_league_id, start_date, end_date, num_teams.
        Then calls yahoo_db_helper to insert data"""
        assert self.data is not None
        data= self.data
        f_league_dict = None
        try:
            yahoo_league_id= int(data['fantasy_content']['league'][0]['league_id'])
            
            #Have to parse start_date and end_date since they are strings and db columns are dates
            start_date = data['fantasy_content']['league'][0]['start_date']
            end_date = data['fantasy_content']['league'][0]['end_date']
            num_teams = data['fantasy_content']['league'][0]['num_teams']
            league_url = data['fantasy_content']['league'][0]['url']
            league_name = data['fantasy_content']['league'][0]['name']
            
            #Create a dictionary to pass to yahoo db helper
            f_league_dict = dict(
                    user_id = session['user_id'],
                    yahoo_league_id = yahoo_league_id,
                    start_date = start_date,
                    end_date = end_date,
                    num_teams = num_teams,
                    league_url = league_url,
                    league_name=league_name
                    )
            """
            yahoo_db_helper=Db_Helper()
            yahoo_db_helper.insert_f_league(f_league_dict)
            """
        except KeyError as error:
            raise Exception( error)
        except Exception as e:
            raise Exception(e)
       
       #return list for debugging of league info
        league_info=[]
        league_info.append(yahoo_league_id)
        league_info.append(start_date)
        league_info.append(end_date)
        league_info.append(num_teams)
        league_info.append(league_url)
        league_info.append(league_name)
        league_info.append(session['user_id'])
        ###^^ NOT USED ATM.
        assert f_league_dict is not None
        return f_league_dict

    # you should run this for every individual team. so the input
    # should only be on specific team.
    
    def _parse_teams_data_v2(self):
        pass
    
    def _parse_teams_data(self):
        """Process all teams in the leagues that you are in.
        RETURNS: confirm_yahoo_league_id(make sure it exists in F_league table), 
        yahoo_team_id, team_name, yahoo_team_url, yahoo_team_logo,
        yahoo_manager_name, yahoo_manager_id, yahoo_manager_guid."""
        
        yahoo_team_key = None
        yahoo_team_id = None
        yahoo_team_name = None
        
        assert self.data is not None        
        data = self.data
        try:
            yahoo_league_id = data['fantasy_content']['league'][0]['league_id']
            
            #Determine league_id by searching for yahoo_league_id. Woot?! Really? 
            f_league = F_League.query.filter_by(yahoo_league_id=yahoo_league_id).first()
            league_id = f_league.league_id

            #Determine user_yahoo_guid to match against yahoo_manager_guid to find owner of team 
            yahoo_user_guid = Yahoo_User_Guid.query.filter_by(user_id=session['user_id']).first()
            user_guid = yahoo_user_guid.yahoo_guid


            #Find number of teams in your league
            index= range(data['fantasy_content']['league'][1]['teams']['count'])
            index=[str(i) for i in index]
            #For loop to go and process the info for each team separately
            for i in index:
                yahoo_team_id=None
                yahoo_manager_name=None
                yahoo_manager_id=None
                yahoo_team_name=None
                yahoo_team_url=None
                yahoo_team_logo=None
                
                yahoo_team_id = data['fantasy_content']['league'][1]['teams'][i]['team'][0][1]['team_id']
                yahoo_manager_guid = data['fantasy_content']['league'][1]['teams'][i]['team'][0][13]['managers'][0]['manager']['guid']
                yahoo_manager_id = data['fantasy_content']['league'][1]['teams'][i]['team'][0][13]['managers'][0]['manager']['manager_id']
                yahoo_manager_name = data['fantasy_content']['league'][1]['teams'][i]['team'][0][13]['managers'][0]['manager']['nickname']
                yahoo_team_name = data['fantasy_content']['league'][1]['teams'][i]['team'][0][2]['name']
                yahoo_team_url = data['fantasy_content']['league'][1]['teams'][i]['team'][0][4]['url']
                yahoo_team_logo = data['fantasy_content']['league'][1]['teams'][i]['team'][0][5]['team_logos'][0]['team_logo']['url']
               
                
                #Create a dictionary to pass to yahoo_db_helper 
                f_team_dict = dict(
                        yahoo_team_id = yahoo_team_id,
                        yahoo_manager_guid = yahoo_manager_guid,
                        yahoo_manager_id = yahoo_manager_id,
                        yahoo_manager_name = yahoo_manager_name,
                        yahoo_team_name = yahoo_team_name,
                        yahoo_team_url = yahoo_team_url,
                        yahoo_team_logo = yahoo_team_logo,
                        league_id = league_id)

                yahoo_db_helper=Db_Helper()
                yahoo_db_helper.insert_f_league_teams(f_team_dict)
               
                #print yahoo_manager_guid, user_guid, f_team_dict['yahoo_team_id']
                if user_guid == yahoo_manager_guid:
                    print 'USER GUID:' + user_guid
                    print 'YAHOO MANAGER GUIDL: '+ yahoo_manager_guid
                    print f_team_dict['yahoo_team_id']
                    yahoo_db_helper.insert_f_team_owner(user_id=session['user_id'])

                """
                #for debugging only. DELETE LATER
                print 'Yahoo _League_ID: '+ yahoo_league_id
                print 'Yahoo Team ID: '+ yahoo_team_id
                print "Manager GUID: "+ yahoo_manager_guid
                print "Manager Name: "+yahoo_manager_name
                print "Team: Name" + yahoo_team_name
                print "Team URL: "+yahoo_team_url
                print "Team Logo: "+yahoo_team_logo
                print " "
                """
        

        except Exception as e:
            raise Exception(e)


if __name__=="__main__":
    # TEST PARSING OF TEAMS IN YOUR LEAGUE
    team_file=open('json_team_data.txt')
    team_json=json.load(team_file)
    yahoo_helper=YahooHelper()
    yahoo_helper.import_json_data(team_json, get="teams")
    yahoo_helper.return_data()
    


    






        
        
        
        
