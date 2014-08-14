import json

file = open('json_player_data.txt')
data = json.load(file)


"""
first_name
first_name_ascii
last_name
last_name_ascii


player_key
player_id
name
editorial_player_key
editorial_team_key
editorial_team_full_name
editorial_team_abbr
bye_weeks
uniform_number
display_position
image_url
headshot
is_undroppable
position_type
eligible_positions
has_player_notes


"""
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

if __name__ == '__main__':
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
                                    a[u'editorial_team_abbr'] = v
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
                        a[u'selected_position'] = item["selected_position"][1]['position']
        data_dict[player_key] = a
    data_dict['meta'] = meta

    print data_dict.keys()
    for k, v in data_dict.iteritems():
        if k != 'meta':
            print v['name']
            print v['last_name_ascii']
            print v['first_name_ascii']
            #print v['player_key']
            print 'display:', v['display_position']
            print 'selected:', v['selected_position']
            #print v['first_name']
            #print v['last_name']
            #print v['uniform_number']
            print v['editorial_team_abbr'].upper()
            print v['position_type']
            print '\n'

'''
print a['player_key']
print a['player_id']
print a['name']
print a['name']['first']
print a['name']['last']
print a['editorial_player_key']
print a['editorial_team_key']
print a['editorial_team_full_name']
print a['editorial_team_abbr']
print a['bye_weeks']['week']
print a['uniform_number']
print a['display_position']
print a['image_url']
print a['headshot']
print a['is_undroppable']
print a['position_type']
print a['eligible_positions']
'''





