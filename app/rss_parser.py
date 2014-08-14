import feedparser
from bs4 import BeautifulSoup
from time import mktime
from datetime import datetime
import re

class RSS_Parser(object):
    """how i think it should work:...this module should be regularly called...
    each rss feed should be it's own entity that is entered in to the database.
    if the object has already been entered, throw it out, if not, enter it.

    """

    def __init__(self):
        self.yahoo_rss = 'http://sports.yahoo.com/nfl/rss.xml'
        self.rotoworld_rss = 'http://www.rotoworld.com/rss/feed.aspx?sport=nfl&ftype=article&count=12&format=rss'
        self.roto_player_rss = 'http://www.rotoworld.com/rss/feed.aspx?sport=nfl&ftype=news&count=15&format=rss'
        self.yahoo_rss_dict = dict()
        self.roto_rss_dict = dict()
        self.roto_player_dict = dict()

    def _reset(self):
        self.__init__()

    def _get_roto_player_rss(self):
        """
        ['summary_detail', 'updated_parsed', 'links', 'title', 'updated',
        'summary', 'guidislink', 'title_detail', 'link', 'id']
        """
        roto_rss = feedparser.parse(self.roto_player_rss)
        for entry in roto_rss.entries:
            title = entry.title
            player_link = entry.link
            content = entry.summary
            dt = datetime.fromtimestamp(mktime(entry.updated_parsed))
            rss_id = entry.id
            #m = re.search("(alt=\")(.*?)(\" border=)", str(content))
            parsed_title = title.split(" - ")[1]
            player = parsed_title.split("|")[0]
            team = parsed_title.split("|")[1].strip(" ")
            first_name = player.split(" ")[0]
            last_name = player.split(" ")[1]
            full_name = player.rstrip()
            fixed_title = title.split(" - ")[0]
            self.roto_player_dict[rss_id] = {
                    'title': fixed_title,
                    'content': content,
                    'player_url': player_link,
                    'full_name': full_name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'team_abbr': team,
                    'rss_id': rss_id,
                    'timestamp': dt
                    }
            """
            print full_name
            print first_name
            print last_name
            print team
            print title
            print content
            print player_link
            print dt
            print rss_id
            print "\n"
            """ 

    def _get_roto_rss(self):
        """
        ['summary_detail', 'updated_parsed', 'links', 'title', 'updated',
        'summary', 'guidislink', 'title_detail', 'link', 'id']
        """
        roto_rss = feedparser.parse(self.rotoworld_rss)
        for entry in roto_rss.entries:
            """
            print "\n"
            print entry.title
            print entry.summary_detail.value
            print entry.link
            print entry.id
            print datetime.fromtimestamp(mktime(entry.updated_parsed))
            """
            title = entry.title
            content = entry.summary_detail.value
            url = entry.link
            link_id = entry.id
            dt = datetime.fromtimestamp(mktime(entry.updated_parsed))
            self.roto_rss_dict[link_id] = {
                    'title': title,
                    'content': content,
                    'url': url,
                    'ts': dt,
                    'rss_id': link_id
                    }


    def _get_yahoo_rss(self):
        yahoo_rss = feedparser.parse(self.yahoo_rss)
        for entry in yahoo_rss.entries:
            soup = BeautifulSoup(entry.summary_detail.value)
            title = entry.title
            m = re.search("(.*?) (\(Yahoo Sports\))", str(title))
            if m:
                # if regex to remove (Yahoo Sports) works:
                title = m.group(1)

            if len(soup.find_all("p")) >= 2:    
                content_1 = soup.find_all("p")[0]
                content_2 = soup.find_all("p")[1]
                m = re.search("(\<p>)(.*?)(\</p>)", str(content_2))
                if m:
                    # remove html tags
                    content_2 = m.group(2)
            elif len(soup.find_all("p")) == 0:
                # because some RSS feeds do not have paragraphs
                content_2 = entry.summary_detail.value
                content_1 = None
            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
            url = entry.links[0].href
            rss_id = entry.id.split(',')
            rss_id = rss_id[-1:]
            if entry.has_key("media_content"):
                media_content_url = entry['media_content'][0]['url']
                soup2 = BeautifulSoup(entry.summary)
                soup2 = soup2.img
                media_content_info = None
                m = re.search("(alt=\")(.*?)(\" border=)", str(soup2))
                if m:
                    media_content_info = m.group(2)
                else:
                    media_content_info = None
            else:
                media_content_url = None
                media_content_info = None
            self.yahoo_rss_dict[rss_id[0]] = {
                    'datetime': dt,
                    'title': title,
                    'url': url,
                    'rss_id': rss_id[0],
                    'content_1': str(content_1),
                    'content_2': str(content_2),
                    'media_url': media_content_url,
                    'media_inf': media_content_info
                    }
            '''
            print len(soup.find_all("p"))
            #print rss_id
            #print entry.summary_detail
            #print entry.summary_detail.value
            soup2 = BeautifulSoup(entry.summary)
            soup2 = soup2.img
            if entry.has_key("media_content"):
                m = re.search("(alt=\")(.*?)(\" border=)", str(soup2))
                if m:
                    print '-'
                    print m.group(1)
                    print m.group(2) # this is what we want
                    print m.group(3)
                    print '-'
            print '--'
            if entry.has_key("summary"):
                print entry['summary']
            if entry.has_key("media_content"):
                print entry['media_content'][0]['url']
            #print entry.keys()
            '''

    def return_roto_rss(self):
        self._reset
        self._get_roto_rss()
        return self.roto_rss_dict

    def return_yahoo_rss(self):
        self._reset
        self._get_yahoo_rss()
        return self.yahoo_rss_dict
    
    def return_roto_players(self):
        self._get_roto_player_rss()
        return self.roto_player_dict


if __name__ == '__main__':
    rss_parser = RSS_Parser()
    roto_dict = rss_parser.return_roto_players()
    print roto_dict.keys()
    for k,v in roto_dict.iteritems():
        print v['player_url']
        print "\n"
    #roto_dict = rss_parser._get_yahoo_rss()
    #yahoo_dict = rss_parser.return_yahoo_rss()
    #print yahoo_dict.keys()

