import json
import nfldb
import re

db = nfldb.connect()
all_pos = [ "TE", "T", "OG","OL","QB","NT","OLB","G","UNK",
		"RB","MLB","OT","S","WR","LS","SAF","P","DB",
		"K","CB","C","FB","LB","ILB","DT","DE","FS" ]
all_sta = ["Unknown", "Active", "InjuredReseve", "PUP"]

pos =list()
sta = list()
pos.append(request.args.get('pos','QB', type=int))
sta.append(request.args.get('sta','Acitve', type=int))
json.dumps(height_weight_bypos( valid_position(pos),valid_sta(sta) ))

def valid_position(pos):
	posi = list()
	for i in range(0,len(pos)):
		if pos[i] == "all":
			return pos[i]
		elif pos[i] in all_pos:
			posi.append(pos[i])
		else:
			pass
	return posi

def valid_sta(sta):
	stat = list()
	for i in range(0,len(sta)):		
		if sta[i] == 'all':
			return sta
		if sta in all_pos:
			stat.append(sta[i])
		else:
		    pass
	return stat

def do_query(q,pos,sta):
	for i in range(0,len(pos)):
		q.player(position=pos[i])
	for i in range(0,len(sta)):
		q.player(status=sta[i])
	return q

def clean_height(hh):
    return re.sub(r'(\d)(\'|-)(\d{1,2})"?( )?$',r'\1-\3in',hh)

def height_weight_bypos(pos,sta):
	dic, tmp = dict(), list()
	q= nfldb.Query(db)
	do_query(q, pos, sta)
	for p in q.as_players():
		pid ,name, team, position= p.player_id, p.full_name,p.team, p.position
		height, weight = clean_height(p.height), p.weight
		dic[pid] = {"name": name, "team":team, "position":position.name, "height":height, "weight": int(weight) }
	for k,v in dic.items():
		tmp.append(v)
	return tmp

