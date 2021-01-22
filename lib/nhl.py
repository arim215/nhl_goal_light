import requests
import datetime

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
        score = requests.get(url)
        score = score.json()
        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])
        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second))
        return score
    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0


def check_if_game(team_id):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id) #Only shows games after noon, so will sleep till 12:10 pm
    try:
        gameday_url = requests.get(url)
        if "gamePk" in gameday_url.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        # Return True to allow for another pass for test
        print("Error encountered, returning True for check_game")
        return True

def check_game_end(team_id):
    """ Function to check if the game ofchosen team is over. Returns True if game, False if NO game. """

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors
    try:
        game_status = requests.get(url)
        game_status = game_status.json()
        game_status = int(game_status['dates'][0]['games'][0]['status']['detailedState'])
        if game_status == "Final":
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        # Return False to allow for another pass for test
        print("Error encountered, returning False for check_game_end")
        return False
