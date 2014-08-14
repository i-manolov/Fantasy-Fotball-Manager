from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine('postgres://nfldb:nfldb@localhost/nfldb')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

try:
    from sqlalchemy.dialects.postgresql import *
except ImportError:
    from sqlalchemy.databases.postgres import *
drive = Table(u'drive', metadata,
    Column(u'gsis_id', VARCHAR(), ForeignKey('game.gsis_id'), primary_key=True),
    Column(u'drive_id', SMALLINT(), primary_key=True),
    Column(u'start_field', TEXT),
    Column(u'start_time', TEXT, nullable=False),
    Column(u'end_field', TEXT),
    Column(u'end_time', TEXT, nullable=False),
    Column(u'pos_team', TEXT, ForeignKey('team.team_id'), nullable=False),
    Column(u'pos_time', TEXT),
    Column(u'first_downs', SMALLINT()),
    Column(u'result', TEXT()),
    Column(u'penalty_yards', SMALLINT(), nullable=False),
    Column(u'yards_gained', SMALLINT(), nullable=False),
    Column(u'play_count', SMALLINT()),
    Column(u'time_inserted', TIMESTAMP()),
    Column(u'time_updated', TIMESTAMP()),
)

f_playedforweek = Table(u'f_playedforweek', metadata,
    Column(u'fplayed_id', INTEGER(), primary_key=True, nullable=False),
    Column(u'fplayer_id', INTEGER(), ForeignKey('f_player.fplayer_id')),
    Column(u'week_id', INTEGER(), ForeignKey('week_lookup.week_id')),
    Column(u'played', BIT(length=1)),
)

f_player = Table(u'f_player', metadata,
    Column(u'fplayer_id', INTEGER(), primary_key=True, nullable=False),
    Column(u'player_id', VARCHAR(length=10), ForeignKey('player.player_id')),
    Column(u'team_id', INTEGER(), ForeignKey('f_team.team_id')),
)

play = Table(u'play', metadata,
    Column(u'gsis_id', VARCHAR(), ForeignKey('drive.gsis_id'), ForeignKey('game.gsis_id'), primary_key=True),
    Column(u'drive_id', SMALLINT(), ForeignKey('drive.drive_id'), primary_key=True),
    Column(u'play_id', SMALLINT(), primary_key=True),
    Column(u'time', TEXT, nullable=False),
    Column(u'pos_team', VARCHAR(length=3), ForeignKey('team.team_id'), nullable=False),
    Column(u'yardline', TEXT),
    Column(u'down', SMALLINT()),
    Column(u'yards_to_go', SMALLINT()),
    Column(u'description', TEXT()),
    Column(u'note', TEXT()),
    Column(u'time_inserted', TIMESTAMP()),
    Column(u'time_updated', TIMESTAMP()),
    Column(u'first_down', SMALLINT(), nullable=False),
    Column(u'fourth_down_att', SMALLINT(), nullable=False),
    Column(u'fourth_down_conv', SMALLINT(), nullable=False),
    Column(u'fourth_down_failed', SMALLINT(), nullable=False),
    Column(u'passing_first_down', SMALLINT(), nullable=False),
    Column(u'penalty', SMALLINT(), nullable=False),
    Column(u'penalty_first_down', SMALLINT(), nullable=False),
    Column(u'penalty_yds', SMALLINT(), nullable=False),
    Column(u'rushing_first_down', SMALLINT(), nullable=False),
    Column(u'third_down_att', SMALLINT(), nullable=False),
    Column(u'third_down_conv', SMALLINT(), nullable=False),
    Column(u'third_down_failed', SMALLINT(), nullable=False),
    Column(u'timeout', SMALLINT(), nullable=False),
    Column(u'xp_aborted', SMALLINT(), nullable=False),
)

play_player = Table(u'play_player', metadata,
    Column(u'gsis_id', VARCHAR(), ForeignKey('drive.gsis_id'), ForeignKey('play.gsis_id'), ForeignKey('game.gsis_id'), primary_key=True),
    Column(u'drive_id', SMALLINT(), ForeignKey('play.drive_id'), ForeignKey('drive.drive_id'), primary_key=True),
    Column(u'play_id', SMALLINT(), ForeignKey('play.play_id'), primary_key=True),
    Column(u'player_id', VARCHAR(length=10), ForeignKey('player.player_id'), primary_key=True, nullable=False),
    Column(u'team', VARCHAR(length=3), ForeignKey('team.team_id'), nullable=False),
    Column(u'defense_ast', SMALLINT(), nullable=False),
    Column(u'defense_ffum', SMALLINT(), nullable=False),
    Column(u'defense_fgblk', SMALLINT(), nullable=False),
    Column(u'defense_frec', SMALLINT(), nullable=False),
    Column(u'defense_frec_tds', SMALLINT(), nullable=False),
    Column(u'defense_frec_yds', SMALLINT(), nullable=False),
    Column(u'defense_int', SMALLINT(), nullable=False),
    Column(u'defense_int_tds', SMALLINT(), nullable=False),
    Column(u'defense_int_yds', SMALLINT(), nullable=False),
    Column(u'defense_misc_tds', SMALLINT(), nullable=False),
    Column(u'defense_misc_yds', SMALLINT(), nullable=False),
    Column(u'defense_pass_def', SMALLINT(), nullable=False),
    Column(u'defense_puntblk', SMALLINT(), nullable=False),
    Column(u'defense_qbhit', SMALLINT(), nullable=False),
    Column(u'defense_safe', SMALLINT(), nullable=False),
    Column(u'defense_sk', REAL(), nullable=False),
    Column(u'defense_sk_yds', SMALLINT(), nullable=False),
    Column(u'defense_tkl', SMALLINT(), nullable=False),
    Column(u'defense_tkl_loss', SMALLINT(), nullable=False),
    Column(u'defense_tkl_loss_yds', SMALLINT(), nullable=False),
    Column(u'defense_tkl_primary', SMALLINT(), nullable=False),
    Column(u'defense_xpblk', SMALLINT(), nullable=False),
    Column(u'fumbles_forced', SMALLINT(), nullable=False),
    Column(u'fumbles_lost', SMALLINT(), nullable=False),
    Column(u'fumbles_notforced', SMALLINT(), nullable=False),
    Column(u'fumbles_oob', SMALLINT(), nullable=False),
    Column(u'fumbles_rec', SMALLINT(), nullable=False),
    Column(u'fumbles_rec_tds', SMALLINT(), nullable=False),
    Column(u'fumbles_rec_yds', SMALLINT(), nullable=False),
    Column(u'fumbles_tot', SMALLINT(), nullable=False),
    Column(u'kicking_all_yds', SMALLINT(), nullable=False),
    Column(u'kicking_downed', SMALLINT(), nullable=False),
    Column(u'kicking_fga', SMALLINT(), nullable=False),
    Column(u'kicking_fgb', SMALLINT(), nullable=False),
    Column(u'kicking_fgm', SMALLINT(), nullable=False),
    Column(u'kicking_fgm_yds', SMALLINT(), nullable=False),
    Column(u'kicking_fgmissed', SMALLINT(), nullable=False),
    Column(u'kicking_fgmissed_yds', SMALLINT(), nullable=False),
    Column(u'kicking_i20', SMALLINT(), nullable=False),
    Column(u'kicking_rec', SMALLINT(), nullable=False),
    Column(u'kicking_rec_tds', SMALLINT(), nullable=False),
    Column(u'kicking_tot', SMALLINT(), nullable=False),
    Column(u'kicking_touchback', SMALLINT(), nullable=False),
    Column(u'kicking_xpa', SMALLINT(), nullable=False),
    Column(u'kicking_xpb', SMALLINT(), nullable=False),
    Column(u'kicking_xpmade', SMALLINT(), nullable=False),
    Column(u'kicking_xpmissed', SMALLINT(), nullable=False),
    Column(u'kicking_yds', SMALLINT(), nullable=False),
    Column(u'kickret_fair', SMALLINT(), nullable=False),
    Column(u'kickret_oob', SMALLINT(), nullable=False),
    Column(u'kickret_ret', SMALLINT(), nullable=False),
    Column(u'kickret_tds', SMALLINT(), nullable=False),
    Column(u'kickret_touchback', SMALLINT(), nullable=False),
    Column(u'kickret_yds', SMALLINT(), nullable=False),
    Column(u'passing_att', SMALLINT(), nullable=False),
    Column(u'passing_cmp', SMALLINT(), nullable=False),
    Column(u'passing_cmp_air_yds', SMALLINT(), nullable=False),
    Column(u'passing_incmp', SMALLINT(), nullable=False),
    Column(u'passing_incmp_air_yds', SMALLINT(), nullable=False),
    Column(u'passing_int', SMALLINT(), nullable=False),
    Column(u'passing_sk', SMALLINT(), nullable=False),
    Column(u'passing_sk_yds', SMALLINT(), nullable=False),
    Column(u'passing_tds', SMALLINT(), nullable=False),
    Column(u'passing_twopta', SMALLINT(), nullable=False),
    Column(u'passing_twoptm', SMALLINT(), nullable=False),
    Column(u'passing_twoptmissed', SMALLINT(), nullable=False),
    Column(u'passing_yds', SMALLINT(), nullable=False),
    Column(u'punting_blk', SMALLINT(), nullable=False),
    Column(u'punting_i20', SMALLINT(), nullable=False),
    Column(u'punting_tot', SMALLINT(), nullable=False),
    Column(u'punting_touchback', SMALLINT(), nullable=False),
    Column(u'punting_yds', SMALLINT(), nullable=False),
    Column(u'puntret_downed', SMALLINT(), nullable=False),
    Column(u'puntret_fair', SMALLINT(), nullable=False),
    Column(u'puntret_oob', SMALLINT(), nullable=False),
    Column(u'puntret_tds', SMALLINT(), nullable=False),
    Column(u'puntret_tot', SMALLINT(), nullable=False),
    Column(u'puntret_touchback', SMALLINT(), nullable=False),
    Column(u'puntret_yds', SMALLINT(), nullable=False),
    Column(u'receiving_rec', SMALLINT(), nullable=False),
    Column(u'receiving_tar', SMALLINT(), nullable=False),
    Column(u'receiving_tds', SMALLINT(), nullable=False),
    Column(u'receiving_twopta', SMALLINT(), nullable=False),
    Column(u'receiving_twoptm', SMALLINT(), nullable=False),
    Column(u'receiving_twoptmissed', SMALLINT(), nullable=False),
    Column(u'receiving_yac_yds', SMALLINT(), nullable=False),
    Column(u'receiving_yds', SMALLINT(), nullable=False),
    Column(u'rushing_att', SMALLINT(), nullable=False),
    Column(u'rushing_loss', SMALLINT(), nullable=False),
    Column(u'rushing_loss_yds', SMALLINT(), nullable=False),
    Column(u'rushing_tds', SMALLINT(), nullable=False),
    Column(u'rushing_twopta', SMALLINT(), nullable=False),
    Column(u'rushing_twoptm', SMALLINT(), nullable=False),
    Column(u'rushing_twoptmissed', SMALLINT(), nullable=False),
    Column(u'rushing_yds', SMALLINT(), nullable=False),
)

meta = Table(u'meta', metadata,
    Column(u'version', SMALLINT()),
    Column(u'last_roster_download', TIMESTAMP()),
    Column(u'season_type', Enum(u'Preseason', u'Regular', u'Postseason', name=u'season_phase')),
    Column(u'season_year', SMALLINT()),
    Column(u'week', SMALLINT()),
)

class Drive(DeclarativeBase):
    __table__ = drive


    #relation definitions
    game = relation('Game', primaryjoin='Drive.gsis_id==Game.gsis_id')
    team = relation('Team', primaryjoin='Drive.pos_team==Team.team_id')
    teams = relation('Team', primaryjoin='Drive.gsis_id==Play.gsis_id', secondary=play, secondaryjoin='Play.pos_team==Team.team_id')
    plays = relation('Play', primaryjoin='Drive.gsis_id==PlayPlayer.gsis_id', secondary=play_player, secondaryjoin='PlayPlayer.drive_id==Play.drive_id')


class FLeague(DeclarativeBase):
    __tablename__ = 'f_league'

    __table_args__ = {}

    #column definitions
    league_id = Column(u'league_id', INTEGER(), primary_key=True, nullable=False)
    league_name = Column(u'league_name', VARCHAR(length=100))
    user_id = Column(u'user_id', INTEGER(), ForeignKey('users.user_id'))

    #relation definitions
    users = relation('User', primaryjoin='FLeague.user_id==User.user_id')


class FPlayedforweek(DeclarativeBase):
    __table__ = f_playedforweek


    #relation definitions
    f_player = relation('FPlayer', primaryjoin='FPlayedforweek.fplayer_id==FPlayer.fplayer_id')
    week_lookup = relation('WeekLookup', primaryjoin='FPlayedforweek.week_id==WeekLookup.week_id')


class FPlayer(DeclarativeBase):
    __table__ = f_player


    #relation definitions
    player = relation('Player', primaryjoin='FPlayer.player_id==Player.player_id')
    f_team = relation('FTeam', primaryjoin='FPlayer.team_id==FTeam.team_id')
    week_lookups = relation('WeekLookup', primaryjoin='FPlayer.fplayer_id==FPlayedforweek.fplayer_id', secondary=f_playedforweek, secondaryjoin='FPlayedforweek.week_id==WeekLookup.week_id')


class FTeam(DeclarativeBase):
    __tablename__ = 'f_team'

    __table_args__ = {}

    #column definitions
    league_id = Column(u'league_id', INTEGER(), ForeignKey('f_league.league_id'))
    team_id = Column(u'team_id', INTEGER(), primary_key=True, nullable=False)
    team_name = Column(u'team_name', VARCHAR(length=100))

    #relation definitions
    f_league = relation('FLeague', primaryjoin='FTeam.league_id==FLeague.league_id')
    players = relation('Player', primaryjoin='FTeam.team_id==FPlayer.team_id', secondary=f_player, secondaryjoin='FPlayer.player_id==Player.player_id')


class Game(DeclarativeBase):
    __tablename__ = 'game'

    __table_args__ = {}

    #column definitions
    away_score = Column(u'away_score', SMALLINT())
    away_score_q1 = Column(u'away_score_q1', SMALLINT())
    away_score_q2 = Column(u'away_score_q2', SMALLINT())
    away_score_q3 = Column(u'away_score_q3', SMALLINT())
    away_score_q4 = Column(u'away_score_q4', SMALLINT())
    away_score_q5 = Column(u'away_score_q5', SMALLINT())
    away_team = Column(u'away_team', VARCHAR(length=3), ForeignKey('team.team_id'), nullable=False)
    away_turnovers = Column(u'away_turnovers', SMALLINT())
    day_of_week = Column(u'day_of_week', Enum(u'Sunday', u'Monday', u'Tuesday', u'Wednesday', u'Thursday', u'Friday', u'Saturday', name=u'game_day'), nullable=False)
    finished = Column(u'finished', BOOLEAN(), nullable=False)
    gamekey = Column(u'gamekey', VARCHAR(length=5))
    gsis_id = Column(u'gsis_id', VARCHAR(), primary_key=True)
    home_score = Column(u'home_score', SMALLINT())
    home_score_q1 = Column(u'home_score_q1', SMALLINT())
    home_score_q2 = Column(u'home_score_q2', SMALLINT())
    home_score_q3 = Column(u'home_score_q3', SMALLINT())
    home_score_q4 = Column(u'home_score_q4', SMALLINT())
    home_score_q5 = Column(u'home_score_q5', SMALLINT())
    home_team = Column(u'home_team', VARCHAR(length=3), ForeignKey('team.team_id'), nullable=False)
    home_turnovers = Column(u'home_turnovers', SMALLINT())
    season_type = Column(u'season_type', Enum(u'Preseason', u'Regular', u'Postseason', name=u'season_phase'), nullable=False)
    season_year = Column(u'season_year', SMALLINT())
    start_time = Column(u'start_time', TIMESTAMP())
    time_inserted = Column(u'time_inserted', TIMESTAMP())
    time_updated = Column(u'time_updated', TIMESTAMP())
    week = Column(u'week', SMALLINT())

    #relation definitions
    teams = relation('Team', primaryjoin='Game.gsis_id==Drive.gsis_id', secondary=drive, secondaryjoin='Drive.pos_team==Team.team_id')


class Play(DeclarativeBase):
    __table__ = play


    #relation definitions
    team = relation('Team', primaryjoin='Play.pos_team==Team.team_id')
    game = relation('Game', primaryjoin='Play.gsis_id==Game.gsis_id')
    drive = relation('Drive', primaryjoin="and_(Play.gsis_id==Drive.gsis_id, Play.drive_id==Drive.drive_id)")
    drives = relation('Drive', primaryjoin='Play.drive_id==PlayPlayer.drive_id', secondary=play_player, secondaryjoin='PlayPlayer.gsis_id==Drive.gsis_id')


class PlayPlayer(DeclarativeBase):
    __table__ = play_player


    #relation definitions
    team = relation('Team', primaryjoin='PlayPlayer.team==Team.team_id')
    game = relation('Game', primaryjoin='PlayPlayer.gsis_id==Game.gsis_id')
    player = relation('Player', primaryjoin='PlayPlayer.player_id==Player.player_id')
    drive = relation('Drive', primaryjoin="and_(PlayPlayer.gsis_id==Drive.gsis_id, PlayPlayer.drive_id==Drive.drive_id)")
    play = relation('Play', primaryjoin="and_(PlayPlayer.gsis_id==Play.gsis_id, PlayPlayer.drive_id==Play.drive_id, PlayPlayer.play_id==Play.play_id)")


class Player(DeclarativeBase):
    __tablename__ = 'player'

    __table_args__ = {}

    #column definitions
    birthdate = Column(u'birthdate', VARCHAR(length=75))
    college = Column(u'college', VARCHAR(length=255))
    first_name = Column(u'first_name', VARCHAR(length=100))
    full_name = Column(u'full_name', VARCHAR(length=100))
    gsis_name = Column(u'gsis_name', VARCHAR(length=75))
    height = Column(u'height', VARCHAR(length=100))
    last_name = Column(u'last_name', VARCHAR(length=100))
    player_id = Column(u'player_id', VARCHAR(length=10), primary_key=True, nullable=False)
    position = Column(u'position', Enum(u'C', u'CB', u'DB', u'DE', u'DL', u'DT', u'FB', u'FS', u'G', u'ILB', u'K', u'LB', u'LS', u'MLB', u'NT', u'OG', u'OL', u'OLB', u'OT', u'P', u'QB', u'RB', u'SAF', u'SS', u'T', u'TE', u'WR', u'UNK', name=u'player_pos'), nullable=False)
    profile_id = Column(u'profile_id', INTEGER())
    profile_url = Column(u'profile_url', VARCHAR(length=255))
    status = Column(u'status', Enum(u'Active', u'InjuredReserve', u'NonFootballInjury', u'Suspended', u'PUP', u'UnsignedDraftPick', u'Exempt', u'Unknown', name=u'player_status'), nullable=False)
    team = Column(u'team', VARCHAR(length=3), ForeignKey('team.team_id'), nullable=False)
    uniform_number = Column(u'uniform_number', SMALLINT())
    weight = Column(u'weight', VARCHAR(length=100))
    years_pro = Column(u'years_pro', SMALLINT())

    #relation definitions
    team = relation('Team', primaryjoin='Player.team==Team.team_id')
    f_teams = relation('FTeam', primaryjoin='Player.player_id==FPlayer.player_id', secondary=f_player, secondaryjoin='FPlayer.team_id==FTeam.team_id')
    drives = relation('Drive', primaryjoin='Player.player_id==PlayPlayer.player_id', secondary=play_player, secondaryjoin='PlayPlayer.gsis_id==Drive.gsis_id')


class Team(DeclarativeBase):
    __tablename__ = 'team'

    __table_args__ = {}

    #column definitions
    city = Column(u'city', VARCHAR(length=50), nullable=False)
    name = Column(u'name', VARCHAR(length=50), nullable=False)
    team_id = Column(u'team_id', VARCHAR(length=3), primary_key=True, nullable=False)

    #relation definitions
    games = relation('Game', primaryjoin='Team.team_id==Drive.pos_team', secondary=drive, secondaryjoin='Drive.gsis_id==Game.gsis_id')
    drives = relation('Drive', primaryjoin='Team.team_id==PlayPlayer.team', secondary=play_player, secondaryjoin='PlayPlayer.gsis_id==Drive.gsis_id')


class User(DeclarativeBase):
    __tablename__ = 'users'

    __table_args__ = {}

    #column definitions
    email = Column(u'email', VARCHAR(length=100))
    first_name = Column(u'first_name', VARCHAR(length=100))
    last_name = Column(u'last_name', VARCHAR(length=100))
    last_sign_out = Column(u'last_sign_out', TIMESTAMP())
    password = Column(u'password', VARCHAR(length=100))
    user_id = Column(u'user_id', INTEGER(), primary_key=True, nullable=False)
    user_name = Column(u'user_name', VARCHAR(length=100))

    #relation definitions


class WeekLookup(DeclarativeBase):
    __tablename__ = 'week_lookup'

    __table_args__ = {}

    #column definitions
    week_description = Column(u'week_description', VARCHAR(length=50))
    week_id = Column(u'week_id', INTEGER(), primary_key=True, nullable=False)

    #relation definitions
    f_players = relation('FPlayer', primaryjoin='WeekLookup.week_id==FPlayedforweek.week_id', secondary=f_playedforweek, secondaryjoin='FPlayedforweek.fplayer_id==FPlayer.fplayer_id')


