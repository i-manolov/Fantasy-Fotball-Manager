from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, yahoo
from models import * #User, F_League, Week_Lookup, Yahoo_RSS_Data, Roto_RSS_Data, Roto_RSS_Player_Data
from forms import SignUpForm, LoginForm, ChangePasswordForm
from height_weight_bypos import *
from yahoo_api_helper import YahooHelper
from yahoo_api_caller import YahooAPICaller
from models import db_session
from app.yahoo_oauth import get_yahoo_api_data
from app.yahoo_db_helper import Db_Helper
from app.rss_parser import RSS_Parser
from sqlalchemy import desc
from nfl_db_helper import *
from datetime import datetime, date
import json

def getFormPositionData():
	pos =list()
	pos.append(request.args.get('pos1','', type=str))
	pos.append(request.args.get('pos2','', type=str))
	pos.append(request.args.get('pos3','', type=str))
	pos.append(request.args.get('pos4','', type=str))
	pos.append(request.args.get('pos5','', type=str))
	pos.append(request.args.get('pos6','', type=str))
	pos.append(request.args.get('pos7','', type=str))
	pos.append(request.args.get('pos8','', type=str))
	pos.append(request.args.get('pos9','', type=str))
	pos.append(request.args.get('pos10','', type=str))
	pos.append(request.args.get('pos11','', type=str))
	pos.append(request.args.get('pos12','', type=str))
	pos.append(request.args.get('pos13','', type=str))
	pos.append(request.args.get('pos14','', type=str))
	pos.append(request.args.get('pos15','', type=str))
	pos.append(request.args.get('pos16','', type=str))
	pos.append(request.args.get('pos17','', type=str))
	pos.append(request.args.get('pos18','', type=str))
	pos.append(request.args.get('pos19','', type=str))
	pos.append(request.args.get('pos20','', type=str))
	pos.append(request.args.get('pos21','', type=str))
	pos.append(request.args.get('pos22','', type=str))
	pos.append(request.args.get('pos23','', type=str))
	pos.append(request.args.get('pos24','', type=str))
	pos.append(request.args.get('pos25','', type=str))
	pos.append(request.args.get('pos26','', type=str))
	pos.append(request.args.get('pos27','', type=str))
	pos.append(request.args.get('pos28','', type=str))
	return pos

def getFormStatusData():
	sta = list()
	sta.append(request.args.get('sta1','', type=str))
	sta.append(request.args.get('sta2','', type=str))
	sta.append(request.args.get('sta3','', type=str))
	sta.append(request.args.get('sta4','', type=str))
	sta.append(request.args.get('sta5','', type=str))
	sta.append(request.args.get('sta6','', type=str))
	return sta

def getFormSeasonYearData():
	sY = list()
	sY.append(request.args.get('sey1',1, type=int))
	sY.append(request.args.get('sey2',1, type=int))
	sY.append(request.args.get('sey3',1, type=int))
	sY.append(request.args.get('sey4',1, type=int))
	sY.append(request.args.get('sey5',1, type=int))
	sY.append(request.args.get('sey6',1, type=int))
	return sY




@yahoo.tokengetter
def get_yahoo_token(token=None):
    return session.get('yahoo_token')

@login_manager.user_loader
def load_user(id):
    '''used by Flask-Login to get primary key for
    user authentication.'''
    return User.query.get(int(id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.before_request
def before_request():
    '''this will run before every function call'''
    g.user = current_user
    # if user is logged in, get the time & add that to database.
    # will probably remove this because don't want too many db insertions.
    
    #if g.user.is_authenticated():
        #g.user.last_seen = datetime.now()
        #db.session.commit()

@app.route('/authenticated')
def authenticated():
    flash('you are authenticated')
    return redirect(url_for('home'))


@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/_getJson')
def getJson():
	pos = getFormPositionData()
	sta = getFormStatusData()
	sY = getFormSeasonYearData()
	#return jsonify(result=pos+sta+sY)
	return json.dumps( height_weight_bypos( pos, sta, sY ))

#for offense graph
@app.route('/offense')
def offense():
    return render_template("/offense.html")

#for passing yard graph
@app.route('/passingyards')
def passingyards():
    week = request.args.get('week',17, type=int)
    year = request.args.get('year',2012,type= int)
    toppy = top_passing_yds(week,year)
    return render_template("passingyards.html",  toppy =toppy )

#for reciving yard graph
@app.route('/recivingyards')
def recivingyards():
    week = request.args.get('week',17, type=int)
    year = request.args.get('year',2012,type= int)
    topry = top_receiving_yds(week,year)
    return render_template("recivingyards.html",  topry =topry)


#for reciving touchdown graph
@app.route('/recivingtouchdowns')
def recivingtouchdowns():
    week = request.args.get('week',17, type=int)
    year = request.args.get('year',2012,type= int)
    toprt = top_receiving_tds(week,year)
    return render_template("recivingtouchdowns.html",  toprt =toprt)


#for passing touchdown graph
@app.route('/passingtouchdowns')
def passingtouchdowns():
    week = request.args.get('week',17, type=int)
    year = request.args.get('year',2012,type= int)
    toppt = top_passing_tds(week,year)
    return render_template("passingtouchdowns.html",  toppt =toppt)



@app.route('/data')
def data():	
	return render_template("/display_data2.html")

@app.route('/data1')
def data1():
	week = request.args.get('week',17, type=int)
	year = request.args.get('year',2012,type= int)
	topry = top_receiving_yds(week,year)
	toppy = top_passing_yds(week,year)
	toprt = top_receiving_tds(week,year)
	toppt = top_passing_tds(week,year)
	return render_template("test.html", topry = topry, toppy =toppy, toprt = toprt, toppt= toppt )

@app.route('/data2')
def data2():
	top = json.dumps(top_receiving_yds(17))
	return render_template("display_data1.html", top = top)

#topry, toppy, toprt, toppt = list(), list(), list(), list()
@app.route('/_getJpy1')
def getJpy1():
	week = request.args.get('week',17, type=int)
	year = request.args.get('year',2012,type= int)
	topry = top_receiving_yds(week,year)
	toppy = top_passing_yds(week,year)
	toprt = top_receiving_tds(week,year)
	toppt = top_passing_tds(week,year)
	return json.dumps({"topry":topry, "toppy":toppy, "toprt":toprt, "toppt":toppt})

@app.route('/_getJpy2')
def getJpy2():
	return json.dumps(top_receiving_yds(17))

@app.route('/_getJpy3')
def getJpy3():
	return json.dumps(top_passing_tds(17))

@app.route('/_getJpy4')
def getJpy4():
	return json.dumps(top_receiving_tds(17))

# top player
@app.route('/data')
def top_player():
	top = top_p()	
	return render_template("/top_players.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated():
    #    return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit(): # password is checked by custom validator
        user = User.query.filter_by(user_name = form.username.data).first()
        login_user(user)
        flash("logged in sucessfully :)")
        session['user_id']=user.user_id
        return redirect(request.args.get('next') or url_for('profile'))
    else:
        flash("incorrect password")
        return render_template('login.html',form=form)
    return render_template("login.html",form=form)

@app.route('/logout')
@login_required
def logout():
    #Update last_sign_out property of user
    user=User ()
    user.save_last_sign_out(user_id=session['user_id'])
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate():
        u = User(
                user_name = form.username.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                password = form.password.data
                )
        db.session.add(u)
        db.session.commit()
        session['email'] = u.email
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    message = 'this is the profile page, if you can see this, you are logged in'
    return render_template('profile.html', message=message)

@app.route('/oauth/yahoo')
@login_required
def yahoo_oauth():
    if 'yahoo_token' in session.keys():
        del session['yahoo_token']
    try:
        return yahoo.authorize(callback=url_for(
            'oauth_authorized', next=request.args.get('next') or request.referrer or None))
    except:
        return redirect(url_for('home'))

@app.route('/oauth/authorized')
@login_required
@yahoo.authorized_handler
def oauth_authorized(resp):
    """['xoauth_yahoo_guid', 'oauth_token_secret', 'oauth_expires_in', 
    'oauth_session_handle', 'oauth_authorization_expires_in', 'oauth_token']
    """
    next_url = request.args.get('next') or url_for('home')
    print resp
    print '\n'
    print "oauth_session_handle: %s" % resp['oauth_session_handle'], '\n'
    print "xoauth_yahoo_guid: %s" % resp['xoauth_yahoo_guid'], '\n'
    print "oauth_token_secret: %s" % resp['oauth_token_secret'], '\n'
    print "oauth_token: %s" % resp['oauth_token']
    
    if resp is None:
        flash (u'You denied the req to sign in to yahoo')
        return redirect(next_url)
    session['yahoo_token'] = (
            resp['oauth_token'],
            resp['oauth_token_secret']
            )
    return redirect(next_url)

@app.route('/rss/yahoo', methods=['GET', 'POST'])
@login_required
def get_yahoo_rss():
    """this test function parses RSS data from yahoo nfl rss and then
    sends the data to yahoo_db_helper where it checks if the current article
    is already in the database. if's already in the database, it does nothing.
    if it doesn't exist, it adds content to database.
    then, we make a db query to pull latest rss feeds
    """
    rss_parser = RSS_Parser()
    db_helper = Db_Helper()
    yahoo_rss_dict = rss_parser.return_yahoo_rss()
    db_helper.load_yahoo_rss_dict(yahoo_rss_dict)
    yahoo_rss_feed = Yahoo_RSS_Data.query.order_by(desc(Yahoo_RSS_Data.timestamp)).all()
    
    return render_template('yahoo_rss_feed.html', rss_feed=yahoo_rss_feed)

@app.route('/rss/rotoworld', methods=['GET', 'POST'])
@login_required
def get_roto_rss():
    """same idea as yahoo rss feed"""
    rss_parser = RSS_Parser()
    db_helper = Db_Helper()
    roto_rss_dict = rss_parser.return_roto_rss()
    db_helper.load_roto_rss_dict(roto_rss_dict)
    roto_rss_feed = Roto_RSS_Data.query.order_by(desc(Roto_RSS_Data.timestamp)).all()
    return render_template('rotoworld_rss_feed.html', rss_feed=roto_rss_feed)

@app.route('/rss/roto_players', methods=['GET', 'POST'])
@login_required
def get_roto_player():
    """used for player updates"""
    rss_parser = RSS_Parser()
    db_helper = Db_Helper()
    roto_player_dict = rss_parser.return_roto_players()
    db_helper.load_roto_players_dict(roto_player_dict)
    roto_player_feed = Roto_RSS_Player_Data.query.order_by(desc(Roto_RSS_Player_Data.timestamp)).all()
    return render_template('rotoworld_players_feed.html', rss_feed=roto_player_feed)


@app.route('/yahoo/do_everything', methods=['GET', 'POST'])
@login_required
def do_everything():
    """this function is executed for new users. this will populate the database
    with all necessary information.
    user_data -> league_data -> team_data -> team_stats -> ind_player_stats"""
    yahoo_parser = YahooHelper()
    yahoo_caller = YahooAPICaller()
    yahoo_db_helper = Db_Helper()
    # start timer that times API calls
    api_call_start_time = time.time()

    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('do_everything') or None))
    
    # load oauth tokens to yahoo
    yahoo_caller.load_oauth_tokens(session['yahoo_token'][0], session['yahoo_token'][1])
    
    # get_user()
    resp, content = yahoo_caller.get_user_info()
    yahoo_parser.import_json_data(content, get='user')
    user_guid = yahoo_parser.return_data()
    yahoo_league_id = ''
    list_of_user_dicts = yahoo_parser.import_json_data(content, get='user_v2')
    
    yahoo_db_helper.import_list_of_user_dicts(list_of_user_dicts)

    yahoo_db_helper.brians_import_user_info(
            user_id = session['user_id'], 
            user_guid = user_guid)

    # this does what parse_league currently does
    yahoo_db_helper.brian_import_user_info_v2(
            user_id = session['user_id'],
            yahoo_league_id = yahoo_league_id,
            start_date = start_date,
            end_date = end_date,
            num_teams = num_teams,
            league_url = league_url,
            league_name = league_name,
            game_key = game_key,
            season_year = season_year
            )
    
    # load league_id for parser
    yahoo_caller.load_yahoo_league_key(yahoo_league_id)
    
    #get_league()
    resp, content = yahoo_caller.get_league_info()
    yahoo_parser.import_json_data(content, get='leagues')
    f_league_dict = yahoo_parser.return_data()
    yahoo_db_helper.brians_import_league_info(f_league_dict)

    #get_team()
    resp, content = yahoo_caller.get_team_info()
    yahoo_parser.import_json_data(content, get='teams')
    processed_data = yahoo_parser.return_data()
    
    #yahoo_db_helper.brians_import_team_info(processed_data)
    #^ will need to rewrite to return a dictionary, as of now,
    # the db insert calls will stay inside yahoo_parser.
    
    nfl_league_key = yahoo_league_id
    league_id = yahoo_db_helper.return_league_id(session['user_id'])
    num_teams = yahoo_db_helper.return_num_teams(league_id)
    print "num_teams: %s" % num_teams
    print "nfl_league_key: %s" % nfl_league_key
    print "league_id: %s" % league_id


    def get_weeks():
        league = F_League.query.filter_by(user_id = session['user_id']).first()
        week = Week_Lookup.query.all()
        week_list = list()
        for w in week:
            if (w.start_date <= date.today()) and (w.start_date >= league.start_date):
                week_list.append(w.week_num)
        return week_list
    week_list = get_weeks()

    ## GET_PLAYERS() starts here
    #used temp to fix update_players
    
    #params : league_key, week, num_teams
    for week in week_list:
        # list of fantasy_players in entire league by week
        players_for_entire_league = yahoo_caller.get_all_players_data(week, nfl_league_key, num_teams)
        # loop over list of fantasy_players JSON data
        # parse the JSON and add them to database
        for players_per_week in players_for_entire_league:
            yahoo_parser.import_json_data(players_per_week, get='players_v2')
            processed_data = yahoo_parser.return_data()
            yahoo_db_helper.brians_import_players_data_v2(processed_data)
    ## GET_PLAYERS() ends here

    #get_team_stats()
    #^^^ will need to write a function to determine how many weeks the user has played.
    # for example if user started league in week 1 and it is currently week 10.
    # the function will need to call get_team_stats for EACH week.
    # right now, it is only handling one week.
    for week in week_list:
        resp, content = yahoo_caller.get_team_stats(week)
        yahoo_parser.import_json_data(content, get='team_stats')
        processed_data = yahoo_parser.return_data()              #<== stats_dict returned here
        yahoo_db_helper.brians_import_team_stats(processed_data) #<== stats_dict being parsed
    #^^ magical insert to DB happens here
    
    for week in week_list:
        scores_for_player = yahoo_caller.get_weekly_stats_for_all_players_in_league(
                week, nfl_league_key, num_teams)
        for player_pts_for_week in scores_for_player:
            yahoo_parser.import_json_data(player_pts_for_week, get='weekly_stats')
            parsed_data = yahoo_parser.return_data()
            yahoo_db_helper.import_player_stats(parsed_data)
            #parsed_scores.append(parsed_data)

    parsed_content=""
    
    api_call_end_time = time.time()
    api_call_time = api_call_end_time - api_call_start_time
    num_api_calls = yahoo_caller.return_api_call_count()
    
    resp = "API CALLS took: %s seconds." % api_call_time
    content = "API CALLS MADE: %s" % num_api_calls


    return render_template('yahoo.html',
            what_data = 'player_stats',
            resp = resp,
            content = content,
            processed_content = parsed_content)

@app.route('/yahoo/new/user_info')
@login_required
def new_user_info():
    yahoo_parser = YahooHelper()
    yahoo_caller = YahooAPICaller()
    yahoo_db_helper = Db_Helper()

    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('new_user_info') or None))
    yahoo_caller.load_oauth_tokens(session['yahoo_token'][0], session['yahoo_token'][1])
    
    resp, content = yahoo_caller.get_user_info()
    yahoo_parser.import_json_data(content, get='user')
    user_guid = yahoo_parser.return_data()
    yahoo_parser.import_json_data(content, get='user_v2')
    list_of_user_dicts = yahoo_parser.return_data()
    
    yahoo_db_helper.brians_import_user_info(
            user_id = session['user_id'],
            user_guid = user_guid)
    # list of n-fantasy_leagues here
    yahoo_db_helper.brians_import_user_info_v2(
            user_id = session['user_id'],
            list_of_user_dicts = list_of_user_dicts)
    return render_template('load_user_success.html')


@app.route('/yahoo/new/team_info/<league_id>')
@login_required
def get_team_info(league_id):

    f_league = F_League.query.filter_by(league_id=league_id).first()
    game_key = f_league.game_key
    yahoo_league_id = f_league.yahoo_league_id

    full_league_id = str(game_key) + '.l.' + str(yahoo_league_id)
    # assumption is that user is already yahoo-authenticated
    yahoo_parser = YahooHelper()
    yahoo_caller = YahooAPICaller()
    db_helper = Db_Helper()

    yahoo_caller.load_oauth_tokens(session['yahoo_token'][0], session['yahoo_token'][1])
    yahoo_caller.load_yahoo_league_key(full_league_id)
    resp, content = yahoo_caller.get_team_info()
    yahoo_parser.import_json_data(content, get='teams')
    # right now, the db insertion is done inside yahoo_parser
    team_data = yahoo_parser.return_data()
    return redirect(url_for('show_yahoo_teams', league_id=league_id))


@app.route('/yahoo/new/league_info/<game_key>/<yahoo_league_id>')
@login_required
def new_league_info(game_key, yahoo_league_id):
    """parameters necessary for parsing a specific league should be 
    passed in. then API calls are executed. this function should
    populate database with scores for player, scores for team, and 
    all teams in ONE league.    
    """
    full_league_id = str(game_key) + '.l.' + str(yahoo_league_id)
    # assumption is that user is already yahoo-authenticated
    yahoo_parser = YahooHelper()
    yahoo_caller = YahooAPICaller()
    db_helper = Db_Helper()
    
    yahoo_caller.load_oauth_tokens(session['yahoo_token'][0], session['yahoo_token'][1])
    yahoo_caller.load_yahoo_league_key(full_league_id)
    resp, content = yahoo_caller.get_team_info()
    yahoo_parser.import_json_data(content, get='teams')
    # right now, the db insertion is done inside yahoo_parser
    team_data = yahoo_parser.return_data()
    num_teams = db_helper.return_num_teams(yahoo_league_id)
    # the fantasy league
    f_league = F_League.query.filter_by(
            user_id = session['user_id'],
            game_key = game_key,
            yahoo_league_id = yahoo_league_id).first()

    if f_league is None:
        raise Exception('error, somehow this league doesnt exist')
    week_list = f_league.get_weeks()
    # get all players in league
    for week in week_list:
        entire_league_players = yahoo_caller.get_all_players_data(week, full_league_id, num_teams)
        for players_per_week in entire_league_players:
            yahoo_parser.import_json_data(players_per_week, get='players_v2')
            processed_data = yahoo_parser.return_data()
            db_helper.brians_import_players_data_v2(processed_data)
    # get all team stats
    for week in week_list:
        resp, content = yahoo_caller.get_team_stats(week)
        yahoo_parser.import_json_data(content, get='team_stats')
        processed_data = yahoo_parser.return_data()              
        db_helper.brians_import_team_stats(processed_data)
    # get individual player stats for every week
    for week in week_list:
        scores_for_player = yahoo_caller.get_weekly_stats_for_all_players_in_league(
                week, full_league_id, num_teams)
        for player_pts_for_week in scores_for_player:
            yahoo_parser.import_json_data(player_pts_for_week, get='weekly_stats')
            parsed_data = yahoo_parser.return_data()
            db_helper.import_player_stats(parsed_data)

    return render_template('load_league_success.html')


@app.route('/yahoo/show_leagues', methods=['GET', 'POST'])
@login_required
def show_yahoo_leagues():
    leagues = F_League.query.filter_by(user_id = session['user_id']).order_by(desc(F_League.season_year)).all()
    return render_template('show_yahoo_leagues.html',leagues=leagues)


@app.route('/yahoo/show_teams/<league_id>', methods=['GET', 'POST'])
@login_required
def show_yahoo_teams(league_id):
    teams = F_Team.query.filter_by(league_id=league_id).all()
    if len(teams) == 0:
        # if no teams show up, get them.
        print len(teams)
        return redirect(url_for('get_team_info', league_id=league_id))
    return render_template('show_yahoo_teams.html', teams=teams)

@app.route('/yahoo/show_players/<f_team_id>')
@login_required
def show_yahoo_players(f_team_id):
    #players = F_Player.query.filter_by(f_team_id=f_team_id, on_)
    pass

@app.route('/yahoo/player_status')
@login_required
def get_update_status():
     yahoo_parser = YahooHelper()
     yahoo_caller = YahooAPICaller()
     db_helper = Db_Helper()
     #status = db_helper.get_player_status_updates(user_id = 1)
     #nfl_player_id_list = list()
     status = NFL_Player_Status_Update.query.all()
     
     #for status in status:
     #    nfl_player_id_list.append(status)

     #print status
     #print status
     #if status is None:
     #    return 'none'
     return render_template('player_status.html', status=status)
    


@app.route('/yahoo/get_user_info', methods = ['GET', 'POST'])
@login_required
def get_yahoo_user_info():
    yahoo_helper = YahooHelper()
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('get_yahoo_user_info') or None))
    params = { 'use_login':'1', 'game_key':'nfl' }
    resp, content = get_yahoo_api_data('users/' + 'games/leagues',
            session['yahoo_token'][0], session['yahoo_token'][1], extras=params)
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('get_yahoo_user_info') or None))
    data, resp = content, resp
    #yahoo_helper.import_json_data(content, get='user')
    #processed_data = yahoo_helper.return_data()
    return render_template('yahoo.html',
            what_data = 'user',
            #league_id = processed_data[0],
            #user_guid = processed_data[1],
            data = data,
            resp = resp
            )

# this works
@app.route('/yahoo/get_league', methods=['GET', 'POST'])
@login_required
def yahoo_get_league():
    '''get own fantasy team roster. need to add these extra fields
    into to postgresql database.
    goal: be able to query fantasy_league_id -> fantasy_team_id -> fantasy_players list'''
    
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_league') or None))
    
    nfl_game_key = 'nfl'
    my_league_id = '1173612'
    my_league_key = nfl_game_key + '.l.' + my_league_id
    my_league_key = '314.l.1173612'

    resp, content = get_yahoo_api_data('league/' + my_league_key + '/metadata',
            session['yahoo_token'][0], session['yahoo_token'][1])
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_league') or None))

    #YAHOO HELPER goes here to process content (processed json)

    
    yahoo_helper = YahooHelper()
    yahoo_helper.import_json_data(content, get="leagues")
    processed_data=yahoo_helper.return_data()
    # note: still need to get team number in league
    return render_template('yahoo.html',
            what_data = 'league',
            resp = resp,
            data=content,
            league_id = processed_data[0],
            start_date = processed_data[1],
            end_date = processed_data[2],
            league_url = processed_data[4],
            num_teams = processed_data[3],
            user_id=processed_data[6]
            )

@app.route('/yahoo/get_team', methods=['GET', 'POST'])
@login_required
def yahoo_get_team():
    '''get own fantasy team roster'''
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_team') or None))
    
    yahoo_parser = YahooHelper()
    yahoo_caller = YahooAPICaller()
    yahoo_db_helper = Db_Helper()
    league_id = yahoo_db_helper.return_league_id(session['user_id'])

    league_key = '175.l.' + str(league_id)
    #params = { 'use_login':'1', 'game_key':'nfl' }

    resp, content = get_yahoo_api_data('league/' + league_key + '/teams',
            session['yahoo_token'][0], session['yahoo_token'][1], extras=params)
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_team') or None))
    
    processed_data = content
    data = ""
    return render_template('yahoo.html',
            what_data = 'test',
            resp = resp,
            processed_data = processed_data,
            data = data
            )

    # CALL YAHOO API HELPER 
    # done but won't be able to display on the page the way im doing it. Compile yahoo_api_helper file on its own to debug.
    
    #yahoo_helper=YahooHelper()
    #yahoo_helper.import_json_data(content, get="teams")
    #yahoo_helper.return_data()
    
    # ['fantasy_content']['league'][1]['teams'][TEAM NUM]
    # to get data for all teams, need to get list of teams, then loop over [TEAM NUM] element
    


    '''
    full_content = content['fantasy_content']['league'][1]['teams']['0']['team'][0][13]
    team_key = content['fantasy_content']['league'][1]['teams']['0']['team'][0][0]['team_key']
    yahoo_team_id = content['fantasy_content']['league'][1]['teams']['0']['team'][0][1]['team_id']
    yahoo_team_name = content['fantasy_content']['league'][1]['teams']['0']['team'][0][2]['name']
    yahoo_team_url = content['fantasy_content']['league'][1]['teams']['0']['team'][0][4]['url']
    yahoo_num_trades = content['fantasy_content']['league'][1]['teams']['0']['team'][0][11]
    yahoo_team_managers = content['fantasy_content']['league'][1]['teams']['0']['team'][0][13]
    
    return render_template('yahoo.html',
            what_data = 'team',
            resp = resp,
            data=content,
            full_content=full_content,
            team_key = team_key,
            yahoo_team_id = yahoo_team_id,
            yahoo_team_name = yahoo_team_name,
            yahoo_team_url = yahoo_team_url,
            yahoo_num_trades = yahoo_num_trades,
            yahoo_team_managers = yahoo_team_managers
            )
    '''

@app.route('/yahoo/get_team_stats', methods=['GET', 'POST']) 
@login_required
def get_stats():
    """get weekly fantasy scores by team"""
    yahoo_helper = YahooHelper()
    yahoo_api_caller = YahooAPICaller()
    yahoo_db_helper = Db_Helper()
    
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('get_stats') or None))
    
    ### !!!!!!!
    league_key = 'nfl.l.1173612'
    ### there should be a call to the database for league key here.

    token_1, token_2 = session['yahoo_token'][0], session['yahoo_token'][1]
    #yahoo_api_caller.load_keys(token_1=token_1, token_2=token_2)
    
    params = {'week':'9' }
    ## for current week
    resp, content = get_yahoo_api_data('league/' + league_key + '/scoreboard',
            session['yahoo_token'][0], session['yahoo_token'][1], extras=params)
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('get_stats') or None))

    yahoo_helper.import_json_data(content, get='team_stats')
    processed_data = yahoo_helper.return_data()       #<== stats_dict returned here
    yahoo_db_helper.brians_import_team_stats(processed_data) #<== stats_dict being parsed

    #
    # SHOULD MAKE DB CALLS HERE TO PULL DATA NOW.
    #

    return render_template('yahoo.html',
            what_data = 'stats',
            resp = resp,
            processed_data = processed_data,
            content = content
            )
    
    
@app.route('/yahoo/get_player_stats', methods=['GET', 'POST'])
@login_required
def get_player_stats():
    yahoo_helper = YahooHelper()
    yahoo_api_caller = YahooAPICaller()
    
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('get_player_stats') or None))
    
    team_key ='314.l.1173612.t.8'
    
    token_1, token_2 = session['yahoo_token'][0], session['yahoo_token'][1]
    
    # load keys to yahoo_api_caller
    yahoo_api_caller.load_oauth_tokens(token_1, token_2)
    # load the team_key parameter
    yahoo_api_caller.load_yahoo_team_key(team_key)
    resp, content = yahoo_api_caller.get_weekly_stats_for_player()
    
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('get_player_stats') or None))


    yahoo_helper.import_json_data(content, get='weekly_stats')
    processed_content = yahoo_helper.return_data()
    yahoo_db_helper=Db_Helper()
    yahoo_db_helper.import_player_stats(processed_content)

    #resp, content = get_yahoo_api_data('team/' + team_key + '/roster/players/stats',
    #        session['yahoo_token'][0], session['yahoo_token'][1], extras=params)

    #if resp.status == 401:
    #    return redirect(url_for('yahoo_oauth', next=url_for('get_player_stats') or None))
    
    return render_template('yahoo.html',
            what_data = 'player_stats',
            resp = resp,
            processed_content = processed_content,
            content = content
            )
        
    
@app.route('/yahoo/get_players', methods=['GET', 'POST'])
@login_required
def yahoo_get_players():
    #get own fantasy team players within a league
    if not 'yahoo_token' in session.keys():
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_players') or None))
    
    game_key = 'nfl'
    league_id = '1173612'
    team_id = '8'
    team_key_format = game_key + '.l.' + league_id + '.t.' + team_id

    #my_league_key = nfl_game_key + '.l.' + my_league_id
    my_league_key = '314.l.1173612'
    league_key = 'nfl.l.1173612'
    team_key = '314.l.1173612.t.8'
    temp = dict()
    
    # THIS SHOULDNT BE HARD CODED
    param = {'week':'12'}
    
    resp, content = get_yahoo_api_data('team/' + team_key + '/roster/players',
            session['yahoo_token'][0], session['yahoo_token'][1], extras=param)
    if resp.status == 401:
        return redirect(url_for('yahoo_oauth', next=url_for('yahoo_get_players') or None))
    
    # call yahoo api HELPER
    yahoo_api_helper=YahooHelper()
    yahoo_api_helper.import_json_data(content, get='players')
    yahoo_api_helper.return_data()

    # this gets team data from collection, may just only need one API call.
    #full_content = content['fantasy_content']['team'][0]
    
    #last ['14'] parameter represents the player
    #full_content = content['fantasy_content']['team'][1]['roster']['0']['players']['14']
    
    full_content = content['fantasy_content']['team'][1]['roster']['0']['players']['14']
    player_data = content['fantasy_content']['team'][1]['roster']['0']['players']['1']
    
    temp = player_data['player'][0][15]

    #iteritems() -> 
    #iterkeys()
    #itervalues()
    data_wanted = ["u'player_key"]#, "u'player_id"]
    
    isolated = list()
    temp_list = list()
    temp_list2 = list()
    temp_value = player_data['player'][0]
    for value in temp_value:
        temp_list.append(type(value))
        #for value in itertools.islice(value,4,5):
        #    isolated = value
        if type(value) == dict:
            for attr in data_wanted: 
                if value.has_key(u'player_key'):
                    isolated = value[u'player_key']
                pass
            for key, value in value.iteritems():
                temp_list2.append(key)
                #isolated.append(value)

    #else:
    #    temp_list = 'isn\'t a dict'
    
    roster_position = player_data['player'][1]['selected_position'][1]['position']
    yahoo_player_key = player_data['player'][0][0]['player_key']
    yahoo_player_id = player_data['player'][0][1]['player_id']
    yahoo_full_name = player_data['player'][0][2]['name']['full']
    yahoo_first_name = player_data['player'][0][2]['name']['first']
    yahoo_players_team = player_data['player'][0][5]
    #yahoo_last_name = player_data['player'][0][2]['name']['last']
    yahoo_last_name = player_data['player'][0][2]['name']
    #yahoo_players_bye_week = player_data['player'][0][7]['bye_weeks']['week']
    yahoo_players_bye_week = player_data['player'][0][7]
    #yahoo_players_team_abbr = player_data['player'][0][6]['editorial_team_abbr']
    yahoo_players_team_abbr = player_data['player'][0][6]
    #yahoo_players_number = player_data['player'][0][8]['uniform_number']
    yahoo_players_number = player_data['player'][0][8]
    #yahoo_players_position = player_data['player'][0][9]['display_position']
    yahoo_players_position = player_data['player'][0][9]

    #position = player_data['player'][1][]

    
    return render_template('yahoo.html',
            what_data = 'players',
            isolated = isolated,
            temp_list = temp_list,
            temp_list2 = temp_list2,
            temp = temp,
            resp = resp,
            data=content,
            player_data = player_data,
            full_content = content,
            roster_position = roster_position,
            yahoo_player_key = yahoo_player_key,
            yahoo_player_id = yahoo_player_id,
            yahoo_full_name = yahoo_full_name,
            yahoo_first_name = yahoo_first_name,
            yahoo_last_name = yahoo_last_name,
            yahoo_players_team = yahoo_players_team,
            yahoo_players_team_abbr = yahoo_players_team_abbr,
            yahoo_player_bye_week = yahoo_players_bye_week,
            yahoo_players_number = yahoo_players_number,
            yahoo_players_position = yahoo_players_position
            )

@app.route('/height_vs_weight')
def height_vs_weight():
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
    return render_template('height_weight.html', scatter_qb=scatter_qb,
                                scatter_ot =scatter_ot,
                                scatter_te= scatter_te,
                                scatter_ss=scatter_ss,
                                scatter_lb=scatter_lb,
                                scatter_rb=scatter_rb,
                                scatter_ls=scatter_ls,
                                scatter_nt=scatter_nt,
                                scatter_p=scatter_p,
                                scatter_olb=scatter_olb,
                                scatter_cb= scatter_cb,
                                scatter_ol=scatter_ol,
                                scatter_g=scatter_g,
                                scatter_og=scatter_og,
                                scatter_wr=scatter_wr,
                                scatter_de=scatter_de,
                                scatter_dt=scatter_dt,
                                scatter_k=scatter_k,
                                scatter_mlb=scatter_mlb,
                                scatter_db=scatter_db,
                                scatter_t=scatter_t,
                                scatter_fs=scatter_fs,
                                scatter_c=scatter_c,
                                scatter_fb=scatter_fb,
                                scatter_ilb=scatter_ilb,
                                scatter_saf=scatter_saf)

@app.route('/changepassword',methods =['GET','POST'])
@login_required
def changepassword():
    
    form= ChangePasswordForm() 
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_name = form.username.data).first()
        user.password=form.password.data
        db.session.merge(user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('changepassword.html', form=form)