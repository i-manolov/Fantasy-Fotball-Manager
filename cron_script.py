#!/home/brian/Envs/fantasyfootballtracker/bin/python
from app.yahoo_db_helper import Db_Helper
from app.rss_parser import RSS_Parser
""" this script is ran by linux cronjob.
Need to add logging functionality to record timestamp of updates & errors.
currently, for ubuntu systems, cron jobs are logged in /var/log/cron*

postgresql: /var/log/postgresql/postgresql-9.1-main.log

"""

rss_parser = RSS_Parser()
db_helper = Db_Helper()

## get dictionaries of new parsed RSS feed.
yahoo_rss_dict = rss_parser.return_yahoo_rss()
roto_rss_dict = rss_parser.return_roto_rss()
roto_player_dict = rss_parser.return_roto_players()

# insert dictionaries to database if there are new feeds.
db_helper.load_yahoo_rss_dict(yahoo_rss_dict)
db_helper.load_roto_rss_dict(roto_rss_dict)
db_helper.load_roto_players_dict(roto_player_dict)


