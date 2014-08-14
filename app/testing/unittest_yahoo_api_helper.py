import unittest
import json
from yahoo_api_helper import YahooHelper
import os

class TestCase(unittest.TestCase):

    def setUp(self):
        self.yahoo_helper = YahooHelper()
        pass
    
    def tearDown(self):
        pass
    
    def test_yahoo_api_helper_reset(self):
        """test to make sure that object resets itself when it is called
        again to import data"""
        self.assertEqual(self.yahoo_helper.data, None)
        imported_json = json.load(open('json_team_data.txt'))
        self.yahoo_helper.import_json_data(imported_json, get='user')
        self.assertEqual(self.yahoo_helper.data, None)
        

    def test_reuse_module(self):
        """test that when yahoo_api_helper is reused without instantation, that
        all data from older request is cleared. self.__init__() should do this."""
        # this seems stupid
        
        self.yahoo_helper.import_json_data(data, arg='')
        returned_data = self.yahoo_helper.return_data()
        
        pass

    def test_json_import(self):
        """test that data imported in to this module is an actual JSON
        object."""
        
        self.assertEqual(self.yahoo_helper.data, None)
        data = open('json_team_data.txt')
        jsond = json.load(data)
        self.yahoo_helper.import_json_data(jsond, get='teams')
        self.assertEqual(self.yahoo_helper.get, 'teams')

        #self.assertEqual(self.yahoo_helper.data, jsond)

    def test_json_import_exception(self):
        """test that import_json_data throws an exception when datatype is incorrect"""
        data = 'test data'
        self.yahoo_helper.import_json_data(data, get='teams')
        self.assertEqual(self.yahoo_helper.data, 'test data')
        self.assertRaises(Exception, self.yahoo_helper.import_json_data, 'not accepted' )
        self.assertRaises(Exception, data=self.yahoo_helper.return_data() )
        #json_data = "asdf"
        #self.assertRaises(Exception, self.yahoo_helper.import_json_data(data, get='zz'))

    def test_parse_user_info(self):
        """ 
        test that this correctly returns a list object of yahoo
        fantasy league id's.
        """
        pass


    def test_league_id_count(self):
        """ 
        test that the _parse_user_data method correctly determines
        the occurences of u'league_key'. this value is used to determine
        the amount of yahoo fantasy leagues the user is a part of.
        """
        pass


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
        pass

    def test_parse_yahoo_league_id(self):
        """
        _parse_yahoo_league_id should clean up league_id's returned from
        other methods. it should remove all uneeded information. return value
        should be yahoo_league_id with no extra characters.
        
        """

        pass




if __name__ == '__main__':
    unittest.main()
    #print os.getcwd()
    #print os.path.dirname(os.path.abspath(__file__))





