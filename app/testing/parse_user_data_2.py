import json

"""
# why doesnt this work...
with open('json_private_user_data', 'r') as f:
    read_data = f.read()
data = read_data
data = json.load(data)
    
    # for reference
       
    data['fantasy_content'].keys()
    [u'yahoo:uri', u'users', u'refresh_rate', u'xml:lang', u'time', u'copyright']
    
    fc['users'].keys()
    [u'count', u'0'] 
    
    v['game'][0].keys()
    [u'game_key', u'code', u'name', u'url', u'season', u'game_id', u'type']

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

"""

file_1 = open('json_private_user_data')
file_2 = open('json_user_data.txt')
data = json.load(file_1)

fc = data['fantasy_content']
uc = fc['users']
games_dict = uc['0']['user'][1]['games']
yahoo_user_guid = uc['0']['user'][0]['guid']
# change this to any other sport: nfl, nba, mlb
accepted_game_types = ['pnfl', 'nfl']


if __name__ == '__main__':
    season_year_dict = {}
    list_of_dicts = list()
    for key in games_dict.keys(): # pass in value of key
        if key != 'count':
            for item in games_dict[key]:
                if games_dict[key].has_key("game"):
                    l_of_leagues = games_dict[key]['game']
                    assert type(games_dict[key]['game']) is list
                    assert type(l_of_leagues) is list
                    assert len(l_of_leagues) == 2
                    if l_of_leagues[0]['code'] in accepted_game_types:
                        #print "-- %s" % l_of_leagues[0]
                        #print l_of_leagues[1]
                        #print l_of_leagues[1]['leagues'].keys()
                        for k, v in l_of_leagues[1]['leagues'].iteritems():
                            if k != u'count':
                                league_dict = {}
                                #print "-- %s %s" % (l_of_leagues[0], type(l_of_leagues[0]))
                                game_key = l_of_leagues[0]['game_key']
                                season_year = l_of_leagues[0]['season']
                                _type = l_of_leagues[0]['type']
                                """
                                [u'league_type', u'end_week', u'name', u'draft_status', u'league_id',
                                u'start_week', u'current_week', u'is_pro_league', u'league_update_timestamp',
                                u'edit_key', u'url', u'start_date', u'end_date', u'scoring_type', u'is_finished',
                                u'password', u'league_key', u'num_teams', u'weekly_deadline']
                                """
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
                                #print v
                                #print v['league'][0].keys()
                                #print '\n'


    #print season_year_dict.keys()
    #print season_year_dict.values()
    #print season_year_dict['2010'].keys()
    print "uc_count = %s" % uc['count']
    print "yahoo_user_guid = %s" % yahoo_user_guid
    for item in list_of_dicts:
        for k, v in item.iteritems():
            print "built_team_key: %s.l.%s" % (v['game_key'], v['league_id'])
            print "league_id: %s" % v['league_id']
            print "start_date: %s" % v['start_date']
            print "end_date: %s" % v['end_date']
            print "league_url: %s" % v['league_url']
            print "num_teams %s" % v['num_teams']
            print "league_nam: %s" % v['league_name']
            print "game_key: %s" % v['game_key']
            print "season_year: %s" % v['season_year']
            print '\n'





        
