import nfldb
import os
'''Ideas:
    scatter plot of height, weight of players + player position
    tds, yards vs age
    tds, yards vs height
    tds, yards vs weight
'''
current_path = os.getcwd() + '/config.ini'
db = nfldb.connect(config_path=current_path)
q = nfldb.Query(db)

class MyException(Exception):
    # for now...
    pass

def reception_leader_this_week(db=db, q=q):
    '''get reception leader for current week'''
    pass


# working
def get_height_weight(pos, db=db, q=q):
    '''
    USAGE: get_height_weight("QB") or get_height_weight("ALL")
    C, OG, OT, TE, WR, FB, RB, QB
    DE, DT, LB, CB, FS, SS, K, P
    
    should: return an array with:[name, weight, height]. using "ALL"
    should return array of every single player
    do moar: return as json object? or write another func
    '''
    valid_positions = [
            'C','OG', 'OT', 'TE', 'WR', 'FB', 'RB', 'QB',
            'DE', 'DT', 'LB', 'CB', 'FS', 'SS', 'K', 'P'
            ]

    def valid_input(pos=pos, valid_positions=valid_positions):
        if pos.upper() not in valid_positions:
            raise MyException('''not a valid position input ''')
        else:
            return True
    
    temp = list()
    def get_height(pos,db=db, q=q):
        q.player(position=pos)
        for p in q.as_players():
            name, weight, team = p.full_name, p.weight, p.team
            uniform_number  = p.uniform_number
            position = p.position
            height = cleanup_height(p.height)
            temp.append(
                    name + ',' + 
                    str(uniform_number) + ',' + 
                    team + ',' +
                    str(position) + ',' + 
                    weight + ',' + 
                    height
                    )
        return temp
    
    def cleanup_height(height):
        height = height.replace("'", "").replace("\"", "")
        if len(height) == 2:
            height = height[0:1] + "'" + height[1:2]
        elif len(height) == 3:
            height = height[0:1] + "'" + height [1:3]
        else:
            raise MyException("how in the world is len(height) != 2 or 3")
        return height

    def get_all(valid_positions=valid_positions):
        return 'asdf'
        pass

    if valid_input():
        return get_height(pos.upper())

print get_height_weight('WR')

# working
def most_wr_third_down_yards(db=db, q=q):
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    plays = q.as_plays()

    aggregated = nfldb.aggregate(plays)
    aggregated = sorted(aggregated, key=lambda p: p.rushing_att, reverse=True)
    for pp in aggregated[0:5]:
        name = pp.player
        statement = 'rushed for %s yards on 3rd down' %  pp.rushing_yds
        attempts = 'on %s attempts' % pp.rushing_att
        average = '@ %s yds/attempt' % (pp.rushing_yds / pp.rushing_att)
        print name, statement, attempts, average
    pass
#most_wr_third_down_yards()

#working
def most_yards_per_third_down(db=db, q=q):
    '''returns most yards/attempt on third down'''
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1, passing_yds__ne=0)
    plays = q.as_plays()

    aggregated = nfldb.aggregate(plays) # returns a list of PlayPlayer objects.
    aggregated = sorted(aggregated, key=lambda p: p.passing_yds, reverse=True)
    for pp in aggregated[0:5]:
        #print pp.player, pp.passing_yds, pp.passing_att
        name = pp.player
        statement = 'threw for %s passing yards on 3rd down' %  pp.passing_yds
        attempts = 'on %s attempts' % pp.passing_att
        average = '@ %s yds/attempt' % (pp.passing_yds / pp.passing_att)
        print name, statement, attempts, average
#most_yards_per_third_down()

def get_player_by_name(db=db, q=q):
    '''get player stats by name'''
    q.game(season_year=2013, season_type='Regular')
    q.player(position='WR')
    for pp in q.sort('height').as_players():
        print pp.full_name, pp.weight, pp.height
    pass

def current_reception_leaders(db=db, q=q):
    '''return reception leaders for 2013 season '''
    q.game(season_year=2013, season_type="Regular")
    q.player(position='WR')
    for pp in q.as_players():
        print pp.full_name, pp.weight
    pass

def get_tall_qbs(db=db, q=q):
    q.game(season_year=2013, season_type="Regular")
    q.player(position='QB')
    for pp in q.sort('height').as_players():
        print pp.player, pp.passing_att, pp.passing_tds

def get_players_by_height(db=db, q=q):
    q.game(season_year=2013, season_type="Regular")
    q.player(position='QB')
    for p in q.player():
        print p
    pass

def top_ten_qb_plays(db,q):
    q.game(season_year=2012, season_type='Regular')
    for pp in q.sort('passing_yds').limit(10).as_aggregate():
        print pp.player, pp.passing_yds

def top_ten_rb_plays(db,q):
    q.game(season=2013, season_type='Regular')
    for pp in q.sort('rushing_yds').limit(5).as_aggregate():
        print pp.player, pp.rushing_yds

def preseason(db, q):
    q.game(season_year=2013)
    q.game(season_type='Regular')
    for g in q.as_games():
        print g

#preseason(db,q)
def top_passing_play(db,q):
    # WOW THIS IS SLOW 
    q.game(season_year=2012, season_type='Regular')
    plays = sorted(q.as_plays(), key = lambda p: p.passing_yds, reverse = True)
    for play in plays[0:5]:
        print play

#top_passing_play(db,q)
def faster_top_passing_plays(db=db,q=q):
    q.game(season_year=2012, season_type='Regular')
    for play in q.sort('passing_yds').limit(5).as_plays():
        print play





