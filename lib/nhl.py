import requests
import datetime
from dateutil import tz
import pause
import json

NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"


def get_teams():
    """ Function to get a list of all the teams name"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        teams.append(team['franchise']['teamName'])

    return teams


def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()

    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {0}".format(team_name))


def fetch_score(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    try:
        score = requests.get(url).json()

        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])

        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second),end='\r')

        return score

    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0


def check_game_status(team_id,date):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """
    # Set URL depending on team selected and date
    url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date)

    try:
        #get game state from API (no state when no games on date)
        game_status = requests.get(url).json()
        game_status = game_status['dates'][0]['games'][0]['status']['detailedState']
        return game_status

    except IndexError:
        #Return No Game when no state available on API since no game
        return 'No Game'

    except requests.exceptions.RequestException:
        # Return No Game to keep going
        return 'No Game'


def get_next_game_date(team_id):
    "get the time of the next game"
    date_test = datetime.date.today()
    gameday = check_game_status(team_id,date_test)

    #Keep going until game day found
    while ("Scheduled" not in gameday):
        date_test = date_test + datetime.timedelta(days=1)
        gameday = check_game_status(team_id,date_test)

    #Get start time of next game
    url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date_test)
    utc_game_time = requests.get(url).json()
    utc_game_time = utc_game_time['dates'][0]['games'][0]['gameDate']
    next_game_time = convert_to_local_time(utc_game_time) + datetime.timedelta(minutes=1)

    return next_game_time

def convert_to_local_time(utc_game_time):
    "convert to local time from UTC"
    utc_game_time = datetime.datetime.strptime(utc_game_time, '%Y-%m-%dT%H:%M:%SZ')
    utc_game_time = utc_game_time.replace(tzinfo=tz.tzutc())
    local_game_time = utc_game_time.astimezone(tz.tzlocal())

    return local_game_time
