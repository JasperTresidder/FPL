import requests
import json
import pandas as pd
from pandas import json_normalize

class FPL:
    def __init__(self):
        self.team_elements = None
        self.session = requests.Session()
        self.team_id = None
        self.team = None
        response = self.session.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        responseStr = response.text
        self.player_data = json.loads(responseStr)
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        responseStr = response.text
        basic_data = json.loads(responseStr)
        self.basic_data_elements = json_normalize(basic_data['elements'])
        from src.fpl.functions import Player
        self.players = []
        for i, row in self.basic_data_elements.iterrows():
            self.players.append(Player(row))
        print('initilised')

    def print(self):
        print(self.team)


    def get_player_name(self, id: int):
        for player_ in self.player_data['elements']:
            if player_['id'] == id:
                return player_['first_name'] + ' ' + player_['second_name'] + '<br>(' + player_['web_name'] + ')'

    def get_player_points(self, id: int):
        pass

    def get_gameweek(self):
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        responseStr = response.text
        basic_data = json.loads(responseStr)
        basic_data_events = basic_data['events']
        for i in basic_data_events:
            if dict(i)['is_current'] == True:
                return str(dict(i)['id'])

    def login(self, username : str, password: str, id: int):
        headers = {
            'authority': 'users.premierleague.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://fantasy.premierleague.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://fantasy.premierleague.com/my-team',
            'accept-language': 'en-US,en;q=0.9,he;q=0.8',
        }
        data = {
            "login": username,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/"
        }
        self.team_id = id
        url = "https://users.premierleague.com/accounts/login/"
        res = self.session.post(url, data=data, headers=headers)
        print('login code: ' + str(res.status_code))

    def get_team(self):
        gameweek = self.get_gameweek()
        team_url = "https://fantasy.premierleague.com/api/entry/" + str(self.team_id) + "/event/" + gameweek + "/picks/"
        res = self.session.get(team_url)
        manager_data = json.loads(res.content)
        self.team_ = [dict(i) for i in manager_data['picks']]
        self.team = dict()
        self.team_elements = []
        for element in self.team_:
            self.team_elements.append(int(element['element']))
            for i in self.players:
                if i.id == element['element']:
                    self.team[str(self.get_player_name(element['element']))] = [self.get_element_points(int(element['element'])), i.team_code, i.photo]
        return self.team


    def get_element_points(self, id: int):
        response = self.session.get(
            "https://fantasy.premierleague.com/api/event/" + str(self.get_gameweek()) + "/live/")
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        responseStr = response.text
        live_fixture_data = pd.read_json(responseStr)
        for i, row in live_fixture_data.iterrows():
            for k in self.team_:
                if i + 1 == k['element'] and k['element'] == id:
                    temp = json_normalize(row.elements)
                    #hi = temp['stats.minutes']
                    #print('hi')
                    return [k['multiplier'] * int(temp['stats.total_points']), temp['stats.minutes'][0], temp['stats.goals_scored'][0], temp['stats.assists'][0], temp['stats.bps'][0], temp['stats.clean_sheets'][0], 'Benched' if k['multiplier'] == 0 else 'Active']
        return 0

    def get_points(self):
        points = 0
        response = self.session.get("https://fantasy.premierleague.com/api/event/" + str(self.get_gameweek()) + "/live/")
        if response.status_code != 200:
            raise Exception("Response was code " + str(response.status_code))
        responseStr = response.text
        live_fixture_data = pd.read_json(responseStr)
        for i, row in live_fixture_data.iterrows():
            for k in self.team_:
                if i + 1 == k['element']:
                    temp = json_normalize(row.elements)
                    for player in self.players:
                        if player.id == i + 1:
                            break
                    points += k['multiplier'] * int(temp['stats.total_points'])
        return points