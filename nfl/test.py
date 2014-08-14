import nflgame


game = nflgame.one(2011, 17, "NE", 'BUF')
for p in game.players.passing():
    print p, p.passing_cmp, p.passing_att, p.passing_yds


