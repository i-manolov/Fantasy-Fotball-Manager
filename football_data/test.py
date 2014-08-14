import urllib2, re, time, pprint, csv

reTeamData = re.compile('/players/search\?category=team&amp;filter=([0-9]+)&amp;playerType=current">([^<]+)')
rePlayerData = re.compile('/([0-9]+)/profile">([^<]+)')
reNextPageURL = re.compile('href="([^"]+)">next</a>')
reURL = re.compile('href="/player/([^"]+)">')

def getTeamList():

    return reTeamData.findall(urllib2.urlopen('http://www.nfl.com/players/search?category=team&playerType=current').read())


def getTeamPlayers(teamID):
    
    teamPageHTML = urllib2.urlopen('http://www.nfl.com/players/search?category=team&filter=%s&playerType=current' % teamID).read()
    players = rePlayerData.findall(teamPageHTML)
    
    nextURL = reNextPageURL.findall(teamPageHTML)
    while len(nextURL) > 0:
        teamPageHTML = urllib2.urlopen('http://www.nfl.com' + nextURL[0].replace('&amp;','&')).read()
        players.extend(rePlayerData.findall(teamPageHTML))
        nextURL = reNextPageURL.findall(teamPageHTML)
    
    return players
    
reHeight = re.compile('>Height\S+:\s(\S\W\S)')
reWeight = re.compile('>Weight\S+:\s(\S+)')
reAge = re.compile('>Age\S+:\s(\S+)')
reCollege = re.compile('>College\S+:\s(\w+)')
reName = re.compile('"player-name">(\D+)&nbsp;&nbsp;<')
reTeam = re.compile('contentTitle = (\S+\s+\S+\s+\S+)')
reNumber = re.compile('<span class="player-number">(\W+\S+)')
rePosition = re.compile('<span class="player-number">\W+\S+\s+(\S+)</span>')

def getPlayerURL(teamID):
    teamPageHTML = urllib2.urlopen('http://www.nfl.com/players/search?category=team&filter=%s&playerType=current' % teamID).read()    
    URL =  reURL.findall(teamPageHTML) 
    return URL

#    for player in URL:
#        pageData = urllib2.urlopen('http://www.nfl.com/player/' + player).read()
#        name = reName.findall(pageData)
#        return name
                
def getPlayerStat(URL):
    try:
        pageData = urllib2.urlopen('http://www.nfl.com/player/' + address).read()
        heightTokens = reHeight.findall(pageData)[0].split('-')
        height = int(heightTokens[0]) * 12 + int(heightTokens[1])
        
        return {'name': reName.findall(pageData),
                'position': rePosition.findall(pageData),
                'number': reNumber.findall(pageData),
                'height': reHeight.findall(pageData),
                'weight': reWeight.findall(pageData),
                'age': reAge.findall(pageData),
                'college': reCollege.findall(pageData),
                'team': reTeam.findall(pageData)}
            
    except:
        print 'Failed to load', URL
                
teams = getPlayerURL(3300)

csvFile = csv.writer(open('NFLplayers.csv', 'w'), delimiter=',', quotechar='"')

for address in teams:
        stat = getPlayerStat(address)
        csvFile.writerow(stat.values())
        
