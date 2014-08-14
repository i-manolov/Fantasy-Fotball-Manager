from coverage import coverage
from app.yahoo_api_helper import YahooHelper
import unittest
import json
import os
from config import basedir

cov = coverage(branch = True, omit = ['config.py', 'config.ini', 'db_schema/*',
    'football_data/*', 'unittest_yahoo_api_helper.py',
    '/home/brian/Envs/fantasyfootballtracker/lib/python2.7/*']
    )
cov.start()

json_files_path = os.getcwd() + '/app/testing/'

class TestCase(unittest.TestCase):

    def setUp(self):
        self.yahoo_helper = YahooHelper()
    
    def tearDown(self):
        pass
    
    def test_sample(self):
        self.assertEqual(1,2)
    
    def test_parse_user_info(self):
        """this test should check that yaho_api_helper correctly
        parses yahoo_user_info from JSON data"""
        known_league_id = u'314.l.1173612'
        known_user_guid = u'UAVLBB4IITTQT5S5JSR6JWXHZM'
        imported_json = json.load(open(json_files_path + 'json_user_data.txt'))
        self.yahoo_helper.import_json_data(imported_json, get='user')
        league_id, user_guid = self.yahoo_helper.return_data()
        print league_id
        print user_guid
        self.assertEqual(known_league_id, league_id)
        self.assertEqual(known_user_guid, user_guid)

    def test_parse_league_info(self):
        """this test should check that yahoo_api_heler correctly
        parses yahoo_league_info"""
        
        imported_json = json.load(open(json_files_path + 'json_league_data.txt'))
        self.yahoo_helper.import_json_data(imported_json, get='leagues')
        f_league_dict = self.yahoo_helper.return_data()
        # does not work right now because it requires a session['user_id']
        self.assertEqual(f_league_dict, 0)
        pass

    def test_parse_league_matchups(self):
        imported_json = json.load(open(json_files_path + 'json_matchups_stats'))
        self.yahoo_helper.import_json_data(imported_json, get='team_stats')
        stats_dict = self.yahoo_helper.return_data()
        #self.assertEqual(stats_dict, 0)

        # known stuff
        team_1 = u'314.l.1173612.t.1'
        team_2 = u'314.l.1173612.t.2'
        team_3 = u'314.l.1173612.t.3'
        team_4 = u'314.l.1173612.t.4'
        team_5 = u'314.l.1173612.t.5'
        team_6 = u'314.l.1173612.t.6'
        team_7 = u'314.l.1173612.t.7'
        team_8 = u'314.l.1173612.t.8'
        team_9 = u'314.l.1173612.t.9'
        team_10 = u'314.l.1173612.t.10'
        league_id = u'1173612'
        current_week = u'9'
        # end known stuff

        # assert dictionary correctly returns team_id
        self.assertEqual(stats_dict[team_1]['team_id'], u'1')
        self.assertEqual(stats_dict[team_2]['team_id'], u'2')
        self.assertEqual(stats_dict[team_3]['team_id'], u'3')
        self.assertEqual(stats_dict[team_4]['team_id'], u'4')
        self.assertEqual(stats_dict[team_5]['team_id'], u'5')
        self.assertEqual(stats_dict[team_6]['team_id'], u'6')
        self.assertEqual(stats_dict[team_7]['team_id'], u'7')
        self.assertEqual(stats_dict[team_8]['team_id'], u'8')
        self.assertEqual(stats_dict[team_9]['team_id'], u'9')
        self.assertEqual(stats_dict[team_10]['team_id'], u'10')
        # assert dictionary correctly returns league_id, current_week
        self.assertEqual(stats_dict['meta']['league_id'], league_id )
        self.assertEqual(stats_dict['meta']['current_week'], current_week )

    def test_parse_weekly_player_stats(self):
        """this test should check that yahoo_api_heler correctly parses 
        yahoo_weekly_player_stats
        keys:
        [u'nfl.p.8813', u'nfl.p.6783', u'nfl.p.100034', u'nfl.p.23996', u'nfl.p.24788',
        u'nfl.p.23999', u'nfl.p.8298', u'nfl.p.25712', 'meta', u'nfl.p.8447', u'nfl.p.9293',
        u'nfl.p.8868', u'nfl.p.8832', u'nfl.p.7544', u'nfl.p.26681', u'nfl.p.100020']
        
        {u'url': u'http://football.fantasysports.yahoo.com/f1/1173612/8',
        'current_week': u'8', u'team_id': u'8',
        u'team_key': u'314.l.1173612.t.8', u'name': u"brian's Team"} != 0

        
        """
        imported_json = json.load(open(json_files_path + 'json_individual_player_stats'))
        self.yahoo_helper.import_json_data(imported_json, get='weekly_stats')
        data_dict = self.yahoo_helper.return_data()
        
        # test the meta key returns right values
        self.assertEqual(data_dict['meta']['team_key'], u'314.l.1173612.t.8')
        self.assertEqual(data_dict['meta']['current_week'], u'8')
        self.assertEqual(data_dict['meta']['name'], u'brian\'s Team')

                

        self.assertEqual(data_dict['meta'], 0)
        
    
    def test_yahoo_api_helper_reset(self):
        """test to make sure that object resets itself when it is called
        again to import data"""
        self.assertEqual(self.yahoo_helper.data, None)
        #imported_json = json.load(open('json_team_data.txt'))
        imported_json = json.load(open(json_files_path+'json_team_data.txt'))
        self.yahoo_helper.import_json_data(imported_json, get='user')
        # assert that imported json is the same
        self.assertEqual(self.yahoo_helper.data, imported_json)
        

    def test_reuse_module(self):
        """test that when yahoo_api_helper is reused without instantation, that
        all data from older request is cleared. self.__init__() should do this."""
        # this seems stupid
        '''
        data = json.load(open(json_files_path + 'json_individual_player_stats'))
        self.yahoo_helper.import_json_data(data, get='player_stats')
        returned_data = self.yahoo_helper.return_data()
        assert returned_data is not None
        '''

    def test_json_import(self):
        """test that data imported in to this module is an actual JSON
        object."""
        # stupid test, removing it.
        #self.assertEqual(self.yahoo_helper.data, None)
        #data = open('json_team_data.txt')
        #jsond = json.load(data)
        #self.yahoo_helper.import_json_data(jsond, get='teams')
        #self.assertEqual(self.yahoo_helper.get, 'teams')
        #self.assertEqual(self.yahoo_helper.data, jsond)

    def test_json_import_exception(self):
        """test that import_json_data throws an exception when datatype is incorrect"""
        
        '''
        data = 'test data'
        self.yahoo_helper.import_json_data(data, get='teams')
        self.assertEqual(self.yahoo_helper.data, 'test data')
        self.assertRaises(Exception, self.yahoo_helper.import_json_data, 'not accepted' )
        self.assertRaises(Exception, data=self.yahoo_helper.return_data() )
        #json_data = "asdf"
        #self.assertRaises(Exception, self.yahoo_helper.import_json_data(data, get='zz'))
        '''
        pass



    def test_league_id_count(self):
        """ 
        test that the _parse_user_data method correctly determines
        the occurences of u'league_key'. this value is used to determine
        the amount of yahoo fantasy leagues the user is a part of.
        """


    def test_more_than_one_league(self):
        """
        test _parse_user_data is able to handle the occurence of more
        than one fantasy league per user. method should simply append
        all fantasy league_id's to a list which is later returned

        """


    def test_league_id_exception(self):
        """
        test that _parse_user_data correctly throws an exception when:
        1. the team count happens to be 0 or a negative number.
        2. there is no parsed data using regex to parse league_key
        
        """

    def test_parse_yahoo_league_id(self):
        """
        _parse_yahoo_league_id should clean up league_id's returned from
        other methods. it should remove all uneeded information. return value
        should be yahoo_league_id with no extra characters.
        
        """





if __name__ == '__main__':
    #unittest.main()
    try:
        unittest.main()
    except:
        print 'there was an exception'
        pass
    #print 'asdf'
    
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory = 'tmp/coverage')
    cov.erase()





