import json
import nfldb
import types
import math
import re

ndb = nfldb.connect()

all_pos = [ "TE", "T", "OG", "OL", "QB", "NT", "OLB", "G",
"RB", "MLB", "OT", "SS", "WR", "LS", "SAF", "P", "DB", "K","CB","C","FB","LB","ILB","DT","DE","FS" ]
all_sta = ["Unknown", "Active", "InjuredReserve", "PUP"]
offense = ["G", "OT", "C", "QB", "WR", "TE" ,"RB"]
defense = ["NT", "DT", "DE", "DB", "CB", "OLB", "MLB", "SS","FS" ]

def valid_seasonYear(s):
	ss = list()
	for i in range(0,len(s)):		
		if s[i] == 0:
			return []
		elif int(s[i]) >= 2009 and int(s[i]) <= 2013:
			ss.append(int(s[i]))
		else :
			pass
	return ss

def valid_position(pos):
	posi = list()
	for i in range(0,len(pos)):		
		if pos[i].upper() == "ALL":
			return all_pos
		elif pos[i] in all_pos:
			posi.append(pos[i])
		else:
			pass
	if posi == []:
		return all_pos	
	return posi	

def valid_sta(sta):
	stat = list()
	for i in range(0,len(sta)):		
		if sta[i].upper() == 'ALL':
			return all_sta
		elif sta[i] in all_sta:
			stat.append(sta[i])
		else:
		    pass
	if stat == []:
		return all_sta
	return stat

def do_query(pos,sta,seasonYear): 
	tm = dict()
	for k in range (0,len(sta)):
		for m in range( 0, len(pos) ):
			if (len(seasonYear) == 0):
				q= nfldb.Query(ndb)
				q.player(status=sta[k])
				tm[sta[k] +pos[m]] = q.player(position=pos[m])
			else :
				for s in range(0,len(seasonYear)):
					q= nfldb.Query(ndb)
					q.player(status=sta[k])
					q.player(position=pos[m])
					tm[sta[k] +pos[m]+str(seasonYear[s])] = q.game(season_year=seasonYear[s])
	return tm		

def clean_height(hh):
	h0 = hh%12
	h1 = hh//12
	h = str(h1)+'-'+str(h0) + 'in'
	return h

def height_weight_bypos(pos,sta,seaY):
	seaY = valid_seasonYear(seaY)
	pos = valid_position(pos)
	sta = valid_sta(sta)
	qlen = len(sta) * len (pos) * len(seaY)
	dic, dic1, da = dict(), dict(), list()
	dic1 = do_query(pos,sta,seaY)
	oo = 'offense'
	dd = 'defense'
	for k,v in dic1.items():
		#if len(seaY) == 0:
		for p in v.as_players():
			if (p.weight is not None and p.height is not None):
				pid ,name, team, position, status= p.player_id, p.full_name,p.team, p.position, p.status
				height, weight = p.height, p.weight
				m1 =math.ceil(height*2.54*100)/100
				if len(seaY) == 0:
					if position.name in offense:
						dic[pid] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name, "off_def":oo } 
					elif position.name in defense:
						dic[pid] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name, "off_def": dd}
					else :
						dic[pid] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name,"off_def":"other" }
				else:
					seasonY = int(k[len(k)-4:len(k)])		
					if position.name in offense:
						dic[pid+ str(seasonY)] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name,"season_year":seasonY , "off_def": oo}
					elif position.name in defense:
						dic[pid+ str(seasonY)] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name,"season_year":seasonY , "off_def": dd}
					else :
						dic[pid+ str(seasonY)] = {"pid":pid, "name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), "status":status.name,"season_year":seasonY,"off_def":"other" }					
	for k,v in dic.items():
		da.append(v)
	return da

def top_passing_yds(w,y):
	top = list()
	dic = dict()
	q = nfldb.Query(ndb)
	q.game(season_year=y, season_type='Regular')
	for p in q.sort('passing_yds').limit(5).as_aggregate():
		dic[p.player_id] = {"name":p.player.full_name, "team":p.player.team, "mark0":"T", "period":"season", "passing_yds":p.passing_yds}
	if w != 0 :
		q = nfldb.Query(ndb)
		q.game(season_year=y, season_type='Regular', week=w)
		for p in q.sort('passing_yds').limit(5).as_aggregate():
			dic[p.player_id+str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark1":"T", "period":"seleted_week", "passing_yds":p.passing_yds}
		if (w-1) != 0 :
			q = nfldb.Query(ndb)
			q.game(season_year=y, season_type='Regular', week=(w-1))
			for p in q.sort('passing_yds').limit(5).as_aggregate():
				dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark2":"T", "period":"previous_week", "passing_yds":p.passing_yds}
	for k,v in dic.items():
		top.append(v)
	return top

def top_receiving_yds(w,y):
	top = list()
	dic = dict()
	q = nfldb.Query(ndb)
	q.game(season_year=y, season_type='Regular')
	for p in q.sort('receiving_yds').limit(5).as_aggregate():
		dic[p.player_id] = {"name":p.player.full_name, "team":p.player.team, "mark0":"T", "period":"season", "receiving_yds":p.receiving_yds}
	if w != 0 :
		q = nfldb.Query(ndb)
		q.game(season_year=y, season_type='Regular', week=w)
		for p in q.sort('receiving_yds').limit(5).as_aggregate():
			dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark1":"T", "period":"seleted_week", "receiving_yds":p.receiving_yds}
		if (w-1) != 0 :
			q = nfldb.Query(ndb)
			q.game(season_year=y, season_type='Regular', week=(w-1))
			for p in q.sort('receiving_yds').limit(5).as_aggregate():
				dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark2":"T", "period":"previous_week", "receiving_yds":p.receiving_yds}
	for k,v in dic.items():
		top.append(v)
	return top


def top_passing_tds(w,y):
	top = list()
	dic = dict()
	q = nfldb.Query(ndb)
	q.game(season_year=y, season_type='Regular')
	for p in q.sort('passing_tds').limit(5).as_aggregate():
		dic[p.player_id] = {"name":p.player.full_name, "team":p.player.team, "mark0":"T", "period":"season", "passing_tds":p.passing_tds}
	if w != 0 :
		q = nfldb.Query(ndb)
		q.game(season_year=y, season_type='Regular', week=w)
		for p in q.sort('passing_tds').limit(5).as_aggregate():
			dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark1":"T", "period":"seleted_week", "passing_tds":p.passing_tds}
		if (w-1) != 0 :
			q = nfldb.Query(ndb)
			q.game(season_year=y, season_type='Regular', week=(w-1))
			for p in q.sort('passing_tds').limit(5).as_aggregate():
				dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark2":"T", "period":"previous_week", "passing_tds":p.passing_tds}
	for k,v in dic.items():
		top.append(v)
	return top

def top_receiving_tds(w,y):
	top = list()
	dic = dict()
	q = nfldb.Query(ndb)
	q.game(season_year=y, season_type='Regular')
	for p in q.sort('receiving_tds').limit(5).as_aggregate():
		dic[p.player_id] = {"name":p.player.full_name, "mark0":"T", "period":"season", "team":p.player.team, "receiving_tds":p.receiving_yds}
	if w != 0 :
		q = nfldb.Query(ndb)
		q.game(season_year=y, season_type='Regular', week=w)
		for p in q.sort('receiving_tds').limit(5).as_aggregate():
			dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark1":"T", "period":"seleted_week", "receiving_tds":p.receiving_tds}
		if (w-1) != 0 :
			q = nfldb.Query(ndb)
			q.game(season_year=y, season_type='Regular', week=(w-1))
			for p in q.sort('receiving_tds').limit(5).as_aggregate():
				dic[p.player_id+ str(w)] = {"name":p.player.full_name, "team":p.player.team, "mark2":"T", "period":"previous_week", "receiving_tds":p.receiving_tds}
	for k,v in dic.items():
		top.append(v)
	return top

#def top_p():
#	top = list()
#	q = nfldb.Query(ndb)
#	q.game(week=17, season_year=2013)
#	play = sorted(q.as_games(), key= lambda p:p.passing_yds, reverse=True)
#	for p in play[0:10]:
#		top.append(p)
#	return top 
	
#play_player(rushing_yds_tds).sort().limit(5)
#p.player(position= "QB")
#for p in v.as_aggregate():
#	if (str(p.weight) is not None and str(p.height) is not None):
#		pid ,name, team, position, status= p.player_id, p.full_name,p.team, p.position, p.status
#		height, weight = p.height, p.weight
#		m1 =math.ceil((int(height[0])*30.48+int(height[1])*2.54)*100)/100
#		dic[pid] = {"name": name, "team":team, "position":position.name, "height":clean_height(height), "height_cm":m1, "weight": int(weight), #"status":status.name }

