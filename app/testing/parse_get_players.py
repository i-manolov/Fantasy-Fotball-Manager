import json

file=open('json_player_data.txt')
data=json.load(file)

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

	#Not sure if nfldb player table stores values as unicode or just ascii so i will parse both
	for i in index:
		f_player_first_name=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['first']
		f_player_first_name_ascii=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['ascii_first']
		f_player_last_name=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['last']
		f_player_last_ascii=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][2]['name']['ascii_last']
		
		f_player_team_abbr=None
		f_player_uniform_number=None
		f_player_position=None
		#need another for loop to get nfl team and uniform number. 
		#WARNING: Json structure differs from player to player_info
		j=len(data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0])
		index_j=range(j-1)
		for ind in index_j:
			d=data['fantasy_content']['team'][1]['roster']['0']['players'][i]['player'][0][ind]
			if type(d)==dict:
				if d.has_key('editorial_team_abbr'):
					for key,val in d.iteritems():
						f_player_team_abbr=val
				if d.has_key('uniform_number'):
					for key,val in d.iteritems():
						f_player_uniform_number=val
				if d.has_key('position'):
					for key,val in d.iteritems():
						f_player_position=val
		f_player_dict={}
		f_player_dict=dict(
				f_player_first_name=f_player_first_name,
				f_player_last_name=f_player_last_name,
				f_player_first_name_ascii=f_player_first_name_ascii,
				f_player_last_ascii=f_player_last_ascii,
				f_player_team_abbr=f_player_team_abbr,
				f_player_uniform_number=f_player_uniform_number,
				f_player_position=f_player_position
				)
		print f_player_dict
			
except Exception as e:
	raise Exception(e)
