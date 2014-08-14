import nfldb
import os

config_path = os.getcwd() + '/config.ini'
nfl_db = nfldb.connect(config_path=config_path)
q = nfldb.Query(nfl_db)

class NFL_DB_Helper():
    def __init__(self):
        self.valid_positions=["OT","TE","SS","LB","RB","LS","NT","P","OLB","CB","OL","G","OG","WR","DE","DT","K","MLB","DB","T","FS","C","QB","FB","ILB","SAF"]
        self.valid_positions_offense=["WR","QB", "TE","C","G","T","RB", "FB","OT", "OL","OG"]
        self.valid_positions_defense=["DT","DE","MLB", "OLB", "CB", "SS", "FS", "SAF","ILB","DB","LB","NT"]
        self.db=nfl_db # this doesn't seem like it's used
        self.q=q   
        self.valid_input=None

    def get_height_weight(self, position, q=q, db=nfl_db):
        temp_list=[]
        temp={}
        q=nfldb.Query(db)
        q.player(position=position, status='Active')
        for p in q.as_players():
            player_full_name=p.full_name
            player_weight= self.convert_pds_to_kg(p.weight)
            player_team=p.team
            if p.uniform_number:
                player_uniform_number= p.uniform_number
            else:
                player_uniform_number=9999 
            player_position=p.position
            player_height=self.cleanup_height(p.height)                             
            temp=dict(f_name=player_full_name, number=player_uniform_number, team=player_team, position=str(player_position), y=player_height, x= player_weight)
            #temp=temp.update(dict(f_name=player_full_name, number=player_uniform_number, team=player_team, position=str(player_position), x=player_height, y= player_weight))
            temp_list.append(temp)
        return temp_list



    def cleanup_height(self,height):
        height = str(height)
        height=height.replace("'", "").replace("\"", "")
        if len(height)==2:
            height=height[0:1] + "'" + height[1:2]
        elif len(height)==3:
            height=height[0:1] + "'" + height[1:3]
        else:
            raise Exception('invalid height input from nfldb database')
        return self.convert_to_cm(height)

    def convert_to_cm(self, height):
        feet=int(height[:1])
        inches=int(height[2:])
        feet_to_inch=feet*12
        centimeters=(feet_to_inch+inches)*2.54
        return round(centimeters, 2)

    def convert_pds_to_kg(self, weight):
        weight=int(weight)
        kilos= weight*0.45359237
        return round(kilos, 2)


if __name__=="__main__":
    nfl_db_helper=NFL_DB_Helper()   

    scatter_qb= nfl_db_helper.get_height_weight('QB')
    scatter_ot=nfl_db_helper.get_height_weight('OT')
    scatter_te=nfl_db_helper.get_height_weight('TE')
    scatter_ss=nfl_db_helper.get_height_weight('SS')
    scatter_lb=nfl_db_helper.get_height_weight('LB')
    scatter_rb=nfl_db_helper.get_height_weight('RB')
    scatter_ls=nfl_db_helper.get_height_weight('LS')
    scatter_nt=nfl_db_helper.get_height_weight('NT')
    scatter_p=nfl_db_helper.get_height_weight('P')
    scatter_olb=nfl_db_helper.get_height_weight('OLB')
    scatter_cb=nfl_db_helper.get_height_weight('CB')
    scatter_ol=nfl_db_helper.get_height_weight('OL')
    scatter_g= nfl_db_helper.get_height_weight('G')
    scatter_og=nfl_db_helper.get_height_weight('OG')
    scatter_wr=nfl_db_helper.get_height_weight('WR')
    scatter_de=nfl_db_helper.get_height_weight('DE')
    scatter_dt=nfl_db_helper.get_height_weight('DT')
    scatter_k=nfl_db_helper.get_height_weight('K')
    scatter_mlb=nfl_db_helper.get_height_weight('MLB')
    scatter_db=nfl_db_helper.get_height_weight('DB')
    scatter_t=nfl_db_helper.get_height_weight('T')
    scatter_fs=nfl_db_helper.get_height_weight('FS')
    scatter_c=nfl_db_helper.get_height_weight('C')
    scatter_fb=nfl_db_helper.get_height_weight('FB')
    scatter_ilb=nfl_db_helper.get_height_weight('ILB')
    scatter_saf=nfl_db_helper.get_height_weight('SAF')

    print scatter_g
    print scatter_qb

    print scatter_qb,
    scatter_ot,
    scatter_te,
    scatter_ss,
    scatter_lb,
    scatter_rb,
    scatter_ls,
    scatter_nt,
    scatter_p,
    scatter_ol,
    scatter_cb,
    scatter_ol,
    scatter_g,
    scatter_og,
    scatter_wr,
    scatter_de,
    scatter_dt,
    scatter_k,
    scatter_mlb,
    scatter_db,
    scatter_t,
    scatter_fs,
    scatter_c,
    scatter_fb,
    scatter_ilb,
    scatter_saf
