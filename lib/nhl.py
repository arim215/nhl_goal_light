import requests
import datetime

NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"


def get_teams():
    """ Function to get a list of all the teams name"""

    url = '{}/teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        teams.append(team['franchise']['teamName'])

    return teams


def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    url = '{}/teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {}".format(team_name))


def fetch_score(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{}schedule?teamId={}&date={:%Y-%m-%d}'.format(NHL_API_URL, team_id,now)
    # Avoid request errors (might still not catch errors)
    try:
        # TODO proper JSON parsing
        score = requests.get(url)
        score = score.text[score.text.find('id\" : {}'.format(team_id)) - 37:score.text.find('id\" : {}'.format(team_id)) - 36]
        score = int(score)

        # Print score for test
        print(score, now.hour, now.minute, now.second)
        return score
    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0


def check_season():
    """ Function to check if in season. Returns True if in season, False in off season. """
    # Get current time
    now = datetime.datetime.now()
    if now.month in (7, 8, 9):
        return False
    else:
        return True


def check_if_game(team_id):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """

    
    # Set URL depending on team selected
    url = '{}schedule?teamId={}'.format(NHL_API_URL, team_id) #Only shows games after noon, so will sleep till 12:10 pm
    # Need test to make sure error is avoided
    try:
        gameday_url = requests.get(url)
        if "gamePk" in gameday_url.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:    # This is the correct syntax
        # Return True to allow for another pass for test
        print("Error encountered, returning True for check_game")
        return True

      
def check_game_end(team_id):
    """ Function to check if the game ofchosen team is over. Returns True if game, False if NO game. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{}schedule?teamId={}&date={:%Y-%m-%d}'.format(NHL_API_URL, team_id,now)
    # Avoid request errors (might still not catch errors)
    try:
        # TODO proper JSON parsing
        game_status = requests.get(url)
        game_status = game_status.text[game_status.text.find('statusCode\" : ') + 15:game_status.text.find('statusCode\" : ') + 16]
        game_status = int(game_status)
        if game_status == 7:
            return True
        else:
            return True
    except requests.exceptions.RequestException:    # This is the correct syntax
        # Return True to allow for another pass for test
        print("Error encountered, returning True for check_game_end")
        return False
