import json
from pprint import pprint

data = open('json_individual_player_stats')
jsond = json.load(data)

prefix = jsond['fantasy_content']['team']
want_data = [u'team_key', u'team_id', u'name', u'url']
meta_dict = dict()
#for i in range(0, len(prefix)):
    #print i
for data in prefix[0]:
    if type(data) is dict:
        for item in want_data:
            if item in data.keys():
                meta_dict[item] = data[item]
"""
worst possible code to debug
"""
list_of_dicts = list()
data_dict = {}
players = prefix[1]['roster']['0']['players']
for keys in players.keys():
    if keys != u'count':# and keys == u'0':
        a = {}
        for item in players[keys]['player']: # passed in keys from u'0' to u'14'
            if type(item) is list and len(item) != 0:
                for i in range(0, len(item)):
                    if type(item[i]) is dict:
                        for k, v in item[i].iteritems():
                            if u'editorial_player_key' in k:
                                a[u'player_key'] = v
                                player_key = v
                            if u'name' in k and type(v) is dict:
                                a[u'name'] = v
                            if u'editorial_team_abbr' in k:
                                a[u'editorial_team_abbr'] = v
                            if u'uniform_number' in k:
                                a[u'uniform_number'] = v
                            if u'eligible_positions' in k:
                                a[u'uniform_number'] = v
                            if u'headshot' in k:
                                a[u'headshot'] = v
                            if u'bye_weeks' in item[i].keys():
                                a[u'bye_weeks'] = v
                            if u'display_position' in item[i].keys():
                                a[u'display_position'] = v

            if type(item) is dict:
                if u'player_points' in item.keys():
                    points = item['player_points']['total']
                    a[u'player_points'] = points 
                if u'selected_position' in item.keys():
                    selected_pos = item['selected_position'][1]['position']
                    a[u'selected_pos'] = selected_pos
        data_dict[player_key] = a

"""
[u'nfl.p.8813', u'nfl.p.6783', u'nfl.p.100034', u'nfl.p.23996', u'nfl.p.24788', u'nfl.p.23999', u'nfl.p.8298', u'nfl.p.25712', u'nfl.p.8447', u'nfl.p.9293', u'nfl.p.8868', u'nfl.p.8832', u'nfl.p.7544', u'nfl.p.26681', u'nfl.p.100020']
"""
#print data_dict[u'nfl.p.100034']['player_points']
#print prefix[1]['roster']['0']['players']['0']['player'][1].keys()
for k,v in data_dict.iteritems():
    #print v['selected_pos']
    print "first_name: %s" % v['name']['first']
    print "last_name: %s" % v['name']['last']
    print "display_pos: %s" % v['display_position']
    print "selected_pos: %s " % v['selected_pos']
    print '\n'
'''
for k,v in data_dict.iteritems():
    print v['name']['full'], v['selected_pos'], v['editorial_team_abbr']
    print v['player_points']
    print v['bye_weeks']
#print data_dict['nfl.p.8813'].keys()
#print data_dict[u'nfl.p.100034']['player_points']
print data_dict.keys()
key_list=data_dict.keys()
#reiterate thru dict by player keys
print '*****Key_List*****' 
for k in key_list:
	print data_dict[k]['name']['full']
'''






