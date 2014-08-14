import json

# why doesnt this work...
'''
with open('json_private_user_data', 'r') as f:
    read_data = f.read()

data = read_data
data = json.load(data)
'''
file = open('json_private_user_data')
data = json.load(file)

fc = data['fantasy_content']
uc = fc['users']
games_dict = uc['0']['user'][1]['games']


if __name__ == '__main__':
    """
    data['fantasy_content'].keys()
    [u'yahoo:uri', u'users', u'refresh_rate', u'xml:lang', u'time', u'copyright']
    
    fc['users'].keys()
    [u'count', u'0'] 
    
    v['game'][0].keys()
    [u'game_key', u'code', u'name', u'url', u'season', u'game_id', u'type']

    """
    #print fc.keys()
    #print fc['yahoo:uri'], '\n'
    #print fc['users'], '\n'
    print uc['0']['user'][0]
    #print uc['0']['user'][1]['games']
    for k, v in games_dict.iteritems():
        if k != u'count':
            #print k
            if v.has_key("game"):
                #print "%s %s" % (type(v['game']), v['game'])
                #print "length: %s " % len(v['game'])
                name = v['game'][0]['name']
                code = v['game'][0]['code']
                game_prefix = v['game'][0]
                                #  not handling pfnl
                if v['game'][0]['name'] == 'Football':
                    #print game_prefix.keys(), '\n'
                    game_key = game_prefix['game_key']
                    code = game_prefix['code']
                    name = game_prefix['name']
                    url = game_prefix['url']
                    season = game_prefix['season']
                    game_id = game_prefix['game_id']
                    _type = game_prefix['type']
                    docstr="""
                    game_key: %s
                    code:     %s
                    name:     %s
                    url:      %s
                    season:   %s
                    game_id:  %s
                    type:     %s
                    """ %(
                    game_key, code, name, url, season, game_id, _type)
                    
                    game_pref2 = v['game'][1]['leagues']
                    if type(game_pref2) is dict:
                        for k,v in game_pref2.iteritems():
                            if k != 'count':
                                print k
                                print v
                                print '\n'

                    # print docstr
                if v['game'][0]['name'] == 'Football PLUS':
                    #print name, code
                    pme = game_prefix['name']
                    url = game_prefix['url']
                    season = game_prefix['season']
                    game_id = game_prefix['game_id']
                    _type = game_prefix['type']
                    docstr="""
                    game_key: %s
                    code:     %s
                    name:     %s
                    url:      %s
                    season:   %s
                    game_id:  %s
                    type:     %s
                    """ %(
                    game_key, code, name, url, season, game_id, _type)
                '''
                game_pref2 = v['game'][1]['leagues']
                if type(game_pref2) is dict:
                    for k,v in game_pref2.iteritems():
                        if k != 'count':
                            print k
                            print v
                            print '\n'
                '''








