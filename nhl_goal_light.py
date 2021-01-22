#!/usr/bin/python

import datetime
import time
import os
import pause
from lib import nhl
from lib import light

def sleep(sleep_period):
    """ Function to sleep if not in season or no game.
    Inputs sleep period depending if it's off season or no game."""

    # Get current time
    now = datetime.datetime.now()
    # Set sleep time for no game today
    delta = datetime.timedelta(hours=sleep_period)
    next_day = datetime.datetime.today() + delta
    next_day = next_day.replace(hour=12, minute=10)
    sleep = next_day - now
    sleep = sleep.total_seconds()
    time.sleep(sleep)


def setup_nhl():
    """Function to setup the nhl_goal_light.py with team,
    team_id and delay"""

    """Try to find a settings.txt file in the folder to automaticly setup
    the goal light with pre-desired team and delay.
    settings.txt file should as such : Enter team_id and delay,
    each on a separate line in this order. LEAVE EMPTY if you want to
    manually input every time. If program can't find settings.txt file or if
    file is empty, it will ask for user input.
    """

    lines = ""
    team = ""
    team_id = ""
    settings_file = '/home/pi/nhl_goal_light/settings.txt'
    if os.path.exists(settings_file):
        # get settings from file
        f = open(settings_file, 'r')
        lines = f.readlines()

    # find team_id
    try:
        team_id = lines[1].strip('\n')
    except IndexError:
        team_id = ""
    if team_id == "":
        team = input("Enter team you want to setup (without city) (Default: Canadiens) \n")
        if team == "":
            team = "Canadiens"
        else:
            team = team.title()
        # query the api to get the ID
        team_id = nhl.get_team_id(team)

    # find delay
    try:
        delay = lines[2].strip('\n')
    except IndexError:
        delay = ""
    if delay is "":
        delay = input("Enter delay required to sync : \n")
        if delay is "":
            delay = 0
    delay = float(delay)

    return (team_id, delay)


if __name__ == "__main__":

    old_score = 0
    new_score = 0
    gameday = False
    season = False

    light.setup()

    team_id, delay = setup_nhl()
    game_time = nhl.test_time(team_id)

    try:

        while (True):

            time.sleep(1)

            # check game
            gameday = nhl.check_if_game(team_id)

            if gameday:

                # check end of game
                game_end = nhl.check_game_end(team_id)

                if not game_end:

                    # Check score online and save score
                    new_score = nhl.fetch_score(team_id)

                    # If score change...
                    if new_score != old_score:
                        time.sleep(delay)
                        if new_score > old_score:
                            # save new score
                            print("GOAL!")
                            # activate_goal_light()
                            light.activate_goal_light()
                        old_score = new_score


                else:
                    print("Game Over!")
                    old_score = 0 # Reset for new game
                    sleep("day")  # sleep till tomorrow
            else:
                print("No Game Today!")
                sleep(12)  # sleep till tomorrow

    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
        light.cleanup()
