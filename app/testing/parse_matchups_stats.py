import json

data = open('json_matchups_stats')
jsond = json.load(data)

league_prefix = jsond['fantasy_content']['league'][0]

league_name = league_prefix["name"]
league_type = league_prefix["league_type"]
league_id=league_prefix["league_id"]
league_id=league_prefix['league_id']
league_url=league_prefix['url']
last_update_timestamp = league_prefix["league_update_timestamp"]
num_teams = league_prefix["num_teams"]
scoring_type = league_prefix["scoring_type"]
current_week = league_prefix["current_week"]

scoreboard = jsond['fantasy_content']['league'][1]['scoreboard']['0']['matchups']
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
				'test':'test',
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
#print stats_dict.keys()
key_list=stats_dict.keys()
for k in key_list:
	if k!='meta':
		yahoo_team_id=stats_dict[k]['team_id']
		yahoo_league_id=stats_dict['meta']['league_id']
		total_points=stats_dict[k]['total_points']
		projected_points=stats_dict[k]['projected_points']
		week_num=stats_dict['meta']['current_week']

		team_points_dict=dict(yahoo_league_id=yahoo_league_id,
				yahoo_team_id=yahoo_team_id, points=total_points,
				projected_points=projected_points, week_num=week_num)
		#print stats_dict[k]['team_id']
		#print stats_dict[stats_dict[k]['opp_team_key']]['team_id']
		#print '------------------------------------------------------'
		all_team_matchups_dict=dict(player1=stats_dict[k]['team_id'], player2=stats_dict[stats_dict[k]['opp_team_key']]['team_id'] )
		print all_team_matchups_dict


	#print team_points_dict
"""
for k in key_list:
	if k!='meta':
		print stats_dict[k]['team_id']
"""
#print stats_dict['meta']['league_id']
	
