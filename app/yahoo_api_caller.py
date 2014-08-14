from app.yahoo_oauth import get_yahoo_api_data
from app.yahoo_db_helper import Db_Helper

class YahooAPICaller(object):
    """makes API calls to yahoo"""
    
    def __init__(self):
        self.token_1, self.token_2 = None, None
        self.yahoo_league_key = None
        self.yahoo_team_key = None
        self.yahoo_player_key = None
        self.data = None
        self.resp = None
        self.params = {}
        self.db_helper = Db_Helper()
        self.current_week = self.db_helper.return_current_week()
        self.api_call_count = 0
        pass
    
    def inc_api_counter(self):
        self.api_call_count += 1

    def return_api_call_count(self):
        return self.api_call_count

    def load_oauth_tokens(self, token_1, token_2):
        self.token_1, self.token_2 = token_1, token_2
        pass

    def load_yahoo_league_key(self, yahoo_league_key):
        self.yahoo_league_key = yahoo_league_key
        pass

    def load_yahoo_team_key(self, yahoo_team_key):
        self.yahoo_team_key = yahoo_team_key
        pass

    def load_yahoo_player_key(self, yahoo_player_key):
        self.yahoo_player_key = yahoo_player_key
        pass
    
    def get_weekly_stats_for_player(self):
        return self._get_player_fantasy_stats_for_week()

    def get_weekly_stats_for_all_players_in_league(self, week, league_key, num_teams):
        """bulk API call for entire league. get all player stats in a league by
        looping over team_key + week. team_key is built using league_key + num_teams """
        # need to pass in:
        # league_key, num_teams
        #num_teams = 10
        #league_key = '314.l.1173612'
        return self._get_all_fantasy_player_stats_for_week(week, league_key, num_teams)

    def get_user_info(self):
        return self._internal_get_user_info()
    
    def get_league_info(self):
        return self._internal_get_league_info()
    
    def get_team_info(self):
        return self._internal_get_team_info()

    def get_team_stats(self, week):
        return self._internal_get_team_stats(week)

    def get_players_data(self, week, team_key):
        return self._internal_get_players_data(week, team_key)

    def get_all_players_data(self, week, league_key, num_teams):
        """bulk API call for entire league. gets all players in a league by
        looping over team_key + week. the team_key is built using league_key + num_teams """
        #num_teams = 10
        #league_key = '314.l.1173612'
        return self._internal_get_all_players_data(week, league_key, num_teams)


    def _internal_get_team_stats(self, week):
        assert self.token_1 is not None
        assert self.token_2 is not None
        assert self.yahoo_league_key is not None
        # the week parameter should be passed in or caculated by the function.
        params = {'week': week }
        resp, content = get_yahoo_api_data('league/' + self.yahoo_league_key + '/scoreboard',
                self.token_1, self.token_2 ,extras=params)
        print '%s API_CALL: GET_TEAM_STATS. LEAGUE_KEY:%s WEEK:%s' % (resp['date'], self.yahoo_league_key, week)
        print resp.reason, '\n'
        self.inc_api_counter()
        return resp, content

    def _internal_get_team_info(self):
        assert self.token_1 is not None
        assert self.token_2 is not None
        assert self.yahoo_league_key is not None
        resp, content = get_yahoo_api_data('league/' + self.yahoo_league_key + '/teams',
                self.token_1, self.token_2)
        print '%s API_CALL: GET_TEAM_INFO. LEAGUE_KEY %s' % (resp['date'], self.yahoo_league_key)
        print resp.reason, '\n'
        self.inc_api_counter()
        return resp, content
    
    def _internal_get_league_info(self):
        assert self.token_1 is not None
        assert self.token_2 is not None
        assert self.yahoo_league_key is not None
        resp, content = get_yahoo_api_data('league/' + self.yahoo_league_key + '/metadata',
                self.token_1, self.token_2)
        print '%s API_CALL: GET_LEAGUE_INFO. LEAGUE_KEY %s' % (resp['date'], self.yahoo_league_key)
        print resp.reason, '\n'
        self.inc_api_counter()
        return resp, content

    def _internal_get_user_info(self):
        assert self.token_1 is not None
        assert self.token_2 is not None
        params = { 'use_login':'1', 'game_key':'nfl' }
        resp, content = get_yahoo_api_data('users/' + 'games/leagues',
                self.token_1, self.token_2, extras=params)
        print '%s API_CALL: GET_USER_INFO.' % (resp['date'])
        print resp.reason, '\n'
        print resp
        self.inc_api_counter()
        return resp, content

    def _internal_get_players_data(self, week, team_key):
        assert self.token_1 is not None
        assert self.token_2 is not None
        param = {'week': week }
        resp, content = get_yahoo_api_data('team/' + team_key + '/roster/players',
                self.token_1, self.token_2, extras=param)
        print "\n"
        print '%s API_CALL: GET_PLAYERS_DATA. TEAM_KEY:%s WEEK:%s' % (resp['date'], team_key, week)
        print resp.reason
        self.inc_api_counter()
        return resp, content

    def _internal_get_all_players_data(self, week, league_key, num_teams):
        assert self.token_1 is not None
        assert self.token_2 is not None
        assert league_key is not None

        # repeat code, can make method seperate
        def build_team_keys(league_key, num_teams):
            list_of_team_keys = list()
            for i in range(0, num_teams):
                list_of_team_keys.append(league_key + '.t.' + str(i+1))
            return list_of_team_keys

        def do_the_call(list_of_team_keys, week):
            list_of_returned_content = list()
            week = str(week)
            params = { 'week': week }
            for team_key in list_of_team_keys:
                resp, content = get_yahoo_api_data('team/' + team_key + '/roster/players',
                self.token_1, self.token_2, extras=params)
                print "\n"
                print '%s API_CALL: GET_ALL_PLAYERS_DATA. TEAM_KEY:%s WEEK:%s' % (resp['date'], team_key, week)
                print resp.reason
                self.inc_api_counter()
                list_of_returned_content.append(content)
            return list_of_returned_content
        
        list_of_keys = build_team_keys(league_key, num_teams)
        list_of_returned_content = do_the_call(list_of_keys, week)
        return list_of_returned_content

        
    def _get_all_fantasy_player_stats_for_week(self, week, league_key, num_teams):
        """as param, need ALL the team_keys. essentially does what
        _get_fantasy_player_stats_for_week does except it does it calls
        it for ALL the team_keys.
        """
        def build_team_keys(league_key, num_teams):
            list_of_team_keys = list()
            for i in range(0, num_teams):
                # build each team_key from league_key and num_teams
                # i+1 is used because teams start at 1 not 0.
                list_of_team_keys.append(league_key + '.t.' + str(i+1))
            return list_of_team_keys

        def do_the_callz(list_of_team_keys, week):
            list_of_returned_content = list()
            week = str(week)
            params = {'type':'week', 'week':week}
            # take each team_key and make API call.
            for team_key in list_of_team_keys:
                resp, content = get_yahoo_api_data("team/" + team_key + "/roster/players/stats",
                        self.token_1, self.token_2, extras=params)
                print '%s API_CALL: GET_PLAYER_STATS_FOR_WEEK. TEAM_KEY:%s WEEK:%s' % (resp['date'], team_key, week)
                print resp.reason, "\n"
                self.inc_api_counter()
                # append each returned JSON to a list.
                list_of_returned_content.append(content)
            return list_of_returned_content
        
        # more stuff that should be passed in to function.
        #week = self.current_week

        assert league_key == self.yahoo_league_key
        list_of_keys = build_team_keys(league_key, num_teams)
        list_of_returned_content = do_the_callz(list_of_keys, week)
        return list_of_returned_content

    
    def _get_player_fantasy_stats_for_week(self):
        """takes team key and week as a parameter and returns matchup points
        scored for that week, team
        
        should pass in weeks arg from views?
        """
        # this stuff is only here to get it working
        self.params = { 'type': 'week', 'week':'8' }
        team_key = team_key = '314.l.1173612.t.8'
        #^^^
        resp, content = get_yahoo_api_data('team/' + team_key + '/roster/players/stats',
                self.token_1, self.token_2, extras=self.params)
        print 'API_CALL: GET_PLAYER_STATS_FOR_WEEK. team_key:%s' % (team_key)
        # this should never happen anyways
        # take care of this condition in views.
        #if resp.status != 200:
        #    raise Exception("resp.status != 200")
        self.inc_api_counter()
        return resp, content        
        
    def _get_player_stats_for_season(self):
        pass



    

