#!.env/bin/python
import sys
import csv
import itertools
import re
import MySQLdb as db

''' Football Terminology
QUARTERBACK
g = games played
qb_rat = Quarterback Rating
Comp = # of completions, pass attempts caught by a reciever
att = # of attempts, # of times QB threw the ball
Pass_yds = Amount QB threw for
pass_yg = pass yards gained(?) im not even sure 
yds_att = yards per attempt (yards/pass attempts)
td  = touchdowns
inter = interceptions thrown, qb throws ball to opponent
rush = # of times QB tries to run the ball
rush_yds = # yds gained by QB running the ball
rush_yg = rush yards gained?
rush_avg = rush average (total rushing yds / # of rushing attempts)
rush_td = rush touchdowns
sack = # of times QB is hit and play ends
sack_yds = # of yards lost being sacked
fum = # of times drop or lose ball while under possesion of QB
fum_lost= # times lost the ball(only counts fumbles that turnover ball
to the other team)

WIDE RECIEVER
rec = # of receptions, catches
targets = # of times thrown to by QB, not caught
rec_yds = # of reception yards
rec_yg = not sure yet
rec_avg = (reception_yds / # of receptions)
lng = Longest catch in yards
yac = # of yards gained AFTER catching ball
rec_1stdown = # of receptions caught that resulted in a first down
rec_td = reception touchdown
kr = kickoff returns
kr_yds = yards gained during kickoff
kr_avg = avg yardage per for kickoff
kr_long = longest kickoff return in yds
kr_td = # of kickoff return Touchdowns
pr = punt returns
pr_yds = punt return yards
pr_avg = punt return average yards
pr_long = longest punt return
pr_td = punt return touchdowns
fum = fumbles
fum_lost = fumbles lost

RUNNING BACK: similar to WR except for:
rush = # of attempts rushing the ball
rush_yds = # of yards gained by rushing ball
rush_yg = ? again not sure what yg means

running backs can also catch the ball that's why they have
rec, rec_yds, rec_avg, rec_long


!!!THESE STATS ARE FOR THE 2012 SEASON!!!!

'''
QB_TABLE = 'QB_Stats'
RB_TABLE = 'RB_Stats'
WR_TABLE = 'WR_Stats'
KR_TABLE = 'KR_Stats'
DEF_TABLE = 'DEF_Stats'


def test_stuff(cursor):
    cursor.execute("SELECT VERSION()")
    ver = cursor.fetchone()
    print "Database version : %s " % ver

def drop_qb_table(cursor):
    cmd = '''DROP TABLE IF EXISTS QB_Stats'''
    cursor.execute(cmd)

def drop_rb_table(cusor):
    cmd = '''DROP TABLE IF EXISTS RB_Stats'''
    cursor.execute(cmd)

def drop_wr_table(cursor):
    cmd = '''DROP TABLE IF EXISTS WR_Stats'''
    cursor.execute(cmd)

def create_qb_table(cursor):
    '''
    name, team, G, QBRat, Comp, Att, Pct, Pass Yds, Yds Att,
    TD, Int, Rush, RushYds, Rush YG, Rush Avg, Rush TD, Sack,
    Sack Yds, Fum, FumL
    '''
    #21
    cmd = """CREATE TABLE IF NOT EXISTS QB_Stats(
    id INT PRIMARY KEY AUTO_INCREMENT,\
    name VARCHAR(64), team VARCHAR(32),\
    g INT, qb_rat FLOAT,\
    comp INT, att INT,\
    pct FLOAT, pass_yds INT,\
    pass_yg FLOAT, yds_att FLOAT,\
    td INT, inter INT,\
    rush INT, rush_yds INT,\
    rush_yg FLOAT, rush_avg FLOAT,\
    rush_td INT, sack INT,\
    sack_yds INT, fum INT,\
    fum_lost INT)"""
    cursor.execute(cmd)

def create_wr_table(cursor):
    #24
    cmd = """CREATE TABLE IF NOT EXISTS WR_Stats(
    id INT PRIMARY KEY AUTO_INCREMENT,\
    name VARCHAR(64), team VARCHAR(32),\
    rec INT, targets INT,\
    rec_yds INT, rec_yg FLOAT,\
    rec_avg FLOAT, lng INT,\
    yac FLOAT, rec_1stdown INT,\
    rec_td INT, kr INT,\
    kr_yds INT, kr_avg FLOAT,\
    kr_lng INT, kr_td INT,\
    pr INT, pr_yds FLOAT,\
    pr_lng INT, pr_td INT,\
    fum INT, fum_lost INT)"""
    cursor.execute(cmd)

def create_rb_table(cursor):
    #19
    cmd = """CREATE TABLE IF NOT EXISTS RB_Stats(
    id INT PRIMARY KEY AUTO_INCREMENT,\
    name VARCHAR(64), team VARCHAR(32),\
    g INT, rush INT,\
    rush_yds INT, rush_yg FLOAT,\
    rush_avg FLOAT, rush_td INT,\
    rec INT, targets INT,\
    rec_yds INT, rec_yg FLOAT,\
    rec_avg FLOAT, rec_long INT,\
    yac FLOAT, rec_1stdown INT,\
    rec_td INT, fum INT,\
    fum_lost INT)"""
    cursor.execute(cmd)

def insert_qb_data(cursor):
    with open('QB.csv', 'rb') as csvfile:
        next(csvfile)
        qb_data = csv.reader(csvfile, delimiter=',')
        for row in qb_data:
            print row
            cursor.execute("""INSERT INTO QB_Stats(name, team, g, qb_rat, comp, att,\
                            pct, pass_yds, pass_yg, yds_att, td, inter, rush, rush_yds, rush_yg,\
                            rush_avg, rush_td, sack, sack_yds, fum,\
                            fum_lost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row)

def insert_wr_data(cursor):
    with open('WR.csv', 'rb') as csvfile:
        next(csvfile)
        wr_data = csv.reader(csvfile, delimiter=',')
        for row in wr_data:
            print row
            cursor.execute("""INSERT INTO WR_Stats(name, team, rec, targets, rec_yds,\
                    rec_yg, rec_avg, lng, yac, rec_1stdown, rec_td, kr, kr_yds,\
                    kr_avg, kr_lng, kr_td, pr, pr_yds, pr_lng, pr_td, fum, fum_lost\
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s %s,\
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                            %s %s, %s, %s)""", row)

def insert_rb_data(cursor):
    with open('RB.csv', 'rb') as csvfile:
        next(csvfile)
        rb_data = csv.reader(csvfile, delimiter=',')
        for row in rb_data:
            print row
            cursor.execute("""INSERT INTO RB_Stats(name, team, g, rush,\
                    rush_yds, rush_yg, rush_avg, rush_td, rec, targets,\
                    rec_yds, rec_yg, rec_avg, rec_long, yac, rec_1stdown,\
                    rec_td, fum,fum_lost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s, %s, %s, %s)""", row)
            

# NOT USED            
def get_columns(cursor):
    temp = list()
    with open('QB.csv', 'r') as csvfile:
        #data = csv.reader(csvfile, delimiter=',')
        data = csv.DictReader(csvfile)
        for row in data:
            temp.append(row)
        print temp


# NOT USED
def get_top_row(csvfile):
    '''get top row elements from csv file for mysql inserts.
    could probably be done much cleaner...
    '''
    first_row = []
    with open(csvfile, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in itertools.islice(data, 1):
            # replace empty space with '_'. some list comprehension fun.
            first_row = [element.replace(' ','_').lower() for element in row]
            # join elements by ','
            first_row = ','.join(first_row)
            # remove _ from string if it occurs at end of element
            first_row = re.sub(r'_,', ',', first_row)
            # remove _ from end of string
            first_row = re.sub(r'_$', '', first_row)
            return first_row


def create_mysql_insert(cursor):
    qb_top_row = get_top_row('QB.csv')
    prefix = '''INSERT INTO %s''' % QB_TABLE
    prefix += '''( %s )''' % qb_top_row
    with open ('QB.csv', 'r') as csvfile:
        next(csvfile)
        qb_data = csv.reader(csvfile, delimiter=',')
        for row in qb_data:
            row = ','.join(row)
            data = ''' VALUES ( %s )''' % row
            cursor.execute(prefix + data)

# NOT USED
def mega_func(val):
    '''ONLY returns  '''
    try:
        if int(val) or val == '0':
            return '%s is an INT ' % val
    except ValueError:
        try:
            if float(val):
                return '%s is a FLOAT' % val
        except ValueError:
            return '%s is a STRING' % val

# NOT USED
def is_a_float(val):
    '''only creates STRING or FLOAT'''
    try:
        if val == '':
            return True
            #return '%s is a FLOAT' % val
        elif int(val) or val == '0':
            return True
            #return '%s is a FLOAT' % val
    except ValueError:
        try:
            if float(val):
                return True
                #return '%s is a FLOAT!' % val
        except ValueError:
            return False
            #return '%s is a STRING' % val

# NOT USED
def create_mysql_table(cursor):
    temp = dict()
    qb_top_row = get_top_row('QB.csv')
    top_row_list = qb_top_row.split(',')
    for column in top_row_list:
        temp[column] = 'NULL'
    print temp
    prefix = '''CREATE TABLE IF NOT EXISTS %s ''' % QB_TABLE
    print prefix
    csvfile = 'QB.csv'
    with open(csvfile, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in itertools.islice(data,1,2):
            print row
    pass
                #if is_a_float(row[number]): # returns True if float, else string
                    

                    
           
            #print row[number]
               # try:
               #     if int(row[number]):
               #         return '%s is an INT ' % row[number]
               #     elif float(row[number]):
               #         return '%s is a FLOAT' % row[number]
               # except ValueError:
               #     return '%s is a STRING' % row[number]
        
        #for row in itertools.islice(data,1,2):
            #for element in row:
            #    print element
            #    #get_type(element)
            #pass
            




if __name__ == "__main__":
    ''' this script should import sample data into your
    database automatically. 
    '''
    try:
        mydb = db.connect(
            host='localhost',
            user='apps',
            passwd='apps',
            db='apps'
            );
        cursor = mydb.cursor()
        create_mysql_table(cursor)
        
        #print get_top_row('QB.csv')
        #get_columns(cursor)
        #test_2(cursor)
        # less bugs this way..

        drop_qb_table(cursor)
        drop_wr_table(cursor)
        drop_rb_table(cursor)
        
        create_qb_table(cursor)
        create_wr_table(cursor)
        create_rb_table(cursor)

        insert_qb_data(cursor)
        insert_wr_data(cursor)
        insert_rb_data(cursor)

    except mydb.Error, e:
        print 'error is %s' %  e
        sys.exit(1)
    
    finally:
        if mydb:
            # this will only run if there are no errors
            mydb.commit()
            mydb.close()


