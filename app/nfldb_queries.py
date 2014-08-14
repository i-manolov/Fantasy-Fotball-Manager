import nfldb
import os
from decorators import async

'''Ideas:
    scatter plot of height, weight of players + player position
    tds, yards vs age
    tds, yards vs height
    tds, yards vs weight
'''
class ValidationError(Exception):
    def __init__(self,  Errors):
        Exception.__init__(self)
        self.Errors = Errors

#config_path = os.getcwd() + '/config.ini'
config_path = os.path.dirname(os.getcwd()) + '/config.ini'
db = nfldb.connect(config_path=config_path)

def reception_leader_this_week(db=db):
    '''get reception leader for current week'''
    pass

# working
def get_height_weight(pos, db=db):
    """
    USAGE: get_height_weight("QB") or get_height_weight("ALL")
    C, OG, OT, TE, WR, FB, RB, QB, DE, DT, LB, CB, FS, SS, K, P
    
    do(): massages the data, cleans up the height and 
    returns [name, uniform_#, team, pos, weight, height]
    
    do moar: return as json object? or write another func
    """
    valid_positions = [
            'C','OG', 'OT', 'TE', 'WR', 'FB', 'RB', 'QB',
            'DE', 'DT', 'LB', 'CB', 'FS', 'SS', 'K', 'P'
            ]
    
    def valid_input(pos=pos, valid_positions=valid_positions):
        if pos.upper() == 'ALL':
            # this should return all
            return True, pos.upper()
        elif pos.upper() not in valid_positions:
            raise ValidationError('''not a valid position input ''')
        else:
            return True, pos.upper()
    
    def do(pos, db=db):
        def cleanup_height(height):
            height = height.replace("'", "").replace("\"", "")
            if len(height) == 2:   
                height = height[0:1] + "'" + height[1:2]
            elif len(height) == 3:
                height = height[0:1] + "'" + height [1:3]
            else:
                raise ValidationError("how in the world is len(height) != 2 or 3")
            return height
        
        q = nfldb.Query(db)
        temp = list()
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
    
    def get_all(valid_positions=valid_positions):
        '''want this to return all objects'''
        players_data = list()
        for positions in valid_positions:
            players_data.append(do(positions))
        # magic that flattens list of list
        return ([item for sublist in players_data for item in sublist])

    try:
        """all the magic and function calling happens here"""
        return_value, param = valid_input()
        if return_value:
            if param == 'ALL':
                return get_all(valid_positions)
            else:
                return do(pos.upper())
    except ValidationError:
        print 'error'
        raise


def recep_yds_per_third_down(db=db):
    """returns most yards/attempt on third down"""
    q = nfldb.Query(db)
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    for pp in q.sort('receiving_yds').limit(20).as_aggregate():
        name = pp.player
        recep = '%s recep yds on 3rd down' % pp.receiving_yds
        att = 'on %s targets' % pp.receiving_tar
        avg = '@ %.2f yds/tar' % (float(pp.receiving_yds) / float(pp.receiving_tar))
        cmp_rate = ' rec rate: %.2f' % (100 *(float(pp.receiving_rec) / float(pp.receiving_tar))) + '%'
        print name, recep, att, avg, cmp_rate

def rushing_yds_per_third_down(db=db):
    q = nfldb.Query(db)
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    for pp in q.sort('rushing_yds').limit(20).as_aggregate():
        name = pp.player
        rush = '%s rushing yds on 3rd down' % pp.rushing_yds
        att = 'on %s atts' % pp.rushing_att
        avg = '@ %.2f yds/att' % (float(pp.rushing_yds) / float(pp.rushing_att))
        #avg = '@ %s yds/att' % (pp.rushing_att)
        
        print name, rush, att, avg

#rushing_yds_per_third_down()


def dep_rushing_yds_per_third_down(db=db):
    q = nfldb.Query(db)
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    plays = q.as_plays()

    aggregated = nfldb.aggregate(plays)
    aggregated = sorted(aggregated, key=lambda p: p.rushing_yds, reverse=True)
    for pp in aggregated[0:10]:
        name = pp.player
        statement = 'rushed for %s yds on 3rd down' %  pp.rushing_yds
        attempts = 'on %s att' % pp.rushing_att
        average = '@ %.2f yds/att' % (float(pp.rushing_yds) / float(pp.rushing_att))
        print name, statement, attempts, average
    pass
#dep_rushing_yds_per_third_down()

#working
#@async
def passing_yds_per_third_down(db=db):
    q = nfldb.Query(db)
    '''returns most yards/attempt on third down'''
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    plays = q.as_plays()

    aggregated = nfldb.aggregate(plays) # returns a list of PlayPlayer objects.
    aggregated = sorted(aggregated, key=lambda p: p.passing_yds, reverse=True)
    for pp in aggregated[0:10]:
        #print pp.player, pp.passing_yds, pp.passing_att
        name = pp.player
        statement = 'threw for %s passing yds on 3rd down' %  pp.passing_yds
        attempts = 'on %s att' % pp.passing_att
        average = '@ %.2f yds/att' % (float(pp.passing_yds) / float(pp.passing_att))
        comp_rate = '.Comp rate: %.2f' % (100 *(float(pp.passing_cmp) / float(pp.passing_att))) + '%'
        print name, statement, attempts, average, comp_rate

#passing_yds_per_third_down()

def current_reception_leaders(db=db):
    q = nfldb.Query(db)
    '''return reception leaders for 2013 season '''
    q.game(season_year=2013, season_type="Regular")
    q.player(position='WR')
    for pp in q.as_players():
        print pp.full_name, pp.weight
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
def faster_top_passing_plays(db=db):
    q.game(season_year=2012, season_type='Regular')
    for play in q.sort('passing_yds').limit(5).as_plays():
        print play

# do not use this, very slow, here for reference
def NOTUSED_recep_yds_per_third_down(db=db):
    '''returns most yards/attempt on third down'''
    q.game(season_year=2012, season_type='Regular')
    q.play(third_down_att=1)
    plays = q.as_plays()
    aggregated = nfldb.aggregate(plays) # returns a list of PlayPlayer objects.
    aggregated = sorted(aggregated, key=lambda p: p.receiving_tar, reverse=True)
    for pp in aggregated[0:10]:
        name = pp.player
        statement = '%s recep yds on 3rd down' %  pp.receiving_yds
        attempts = 'on %s targets' % pp.receiving_tar
        average = '@ %.2f yds/target' % (float(pp.receiving_yds) / float(pp.receiving_tar))
        comp_rate = '.recep rate: %.2f' % (100 *(float(pp.receiving_rec) / float(pp.receiving_tar))) + '%'
        print name, statement, attempts, average, comp_rate


if __name__ == '__main__':
    print get_height_weight('ALL')


