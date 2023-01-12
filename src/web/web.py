from http.server import BaseHTTPRequestHandler
class MyServer(BaseHTTPRequestHandler):
    @classmethod
    def load(self, team_code: int):
        from fpl.fpl import FPL
        self.User = FPL()
        self.User.login('jasper.tres9@gmail.com', 'U*4E#AqHanC7%tR', team_code)

    def do_GET(self):
        url_line = self.path.split('/')
        team_id_code = 0
        team_gw = 0
        try:
            self.User.login('jasper.tres9@gmail.com', 'U*4E#AqHanC7%tR', int(url_line[1]))
            team_id_code = int(url_line[1])
        except:
            self.User.login('jasper.tres9@gmail.com', 'U*4E#AqHanC7%tR', 6574078)
            team_id_code = 6574078
        try:
            team = self.User.get_team(url_line[2])
            points = self.User.get_points(url_line[2])
            team_gw = url_line[2]
        except:
            team = self.User.get_team(self.User.get_gameweek())
            points = self.User.get_points(self.User.get_gameweek())
            team_gw = self.User.get_gameweek()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>FPL</title><style>h1 {color: red; text-align: center;}"
                               " a1 {text-align: center;}"
                               " h2 {color: blue; text-align: center;}"
                               " body {background-color: #fefbd8;}"
                               " p1 {color: blue;}"
                               " p2 {color: white;}"
                               " table, th, td {border: 1px solid; text-align: center;}"
                               " #green {color:green;}"
                               " #red {color:red;}"
                               " #redn {color:red; font-size: 80px; }"
                               " #blue {color:blue;}"
                               " #bluen {color:blue; font-size: 80px; }"
                               " #number {font-size: 80px; }"
                               " td {font-size: 20px; }"
                               " th {font-size: 30px; width: 300px;}"
                               "</style></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>FPL Points Live</h1>", "utf-8"))
        self.wfile.write(bytes("<h2>GameWeek " + str(team_gw) +"</h2>", "utf-8"))
        self.wfile.write(bytes("<center><a href='/" + str(team_id_code) + "/" + str(int(team_gw) -1) + "'>Prev</a>", "utf-8"))
        self.wfile.write((bytes("<p>                             </p>", "utf-8")))
        self.wfile.write(bytes("<a href='/" + str(team_id_code) + "/" + str(int(team_gw) + 1) + "'>Next</a></center>", "utf-8"))
        self.wfile.write(bytes("<table><tr>"
                               "<th id='green'>Player</th>"
                               "<th id='green'>Team</th>"
                               "<th id='blue'>Points</th>"
                               "<th id='green'>Img</th>"
                               "<th id='green'>Minutes</th>"
                               "<th id='green'>Goals Scored</th>"
                               "<th id='green'>Assists</th>"
                               "<th id='green'>BPS</th>"
                               "<th id='green'>Clean Sheets</th>"
                               "<th id='green'>Status</th></tr>", "utf-8"))
        for key, value in team.items():
            self.wfile.write(bytes("<tr><td>" + str(key) +
                                   "</td><td>" + '<img width="110" height="140" class="clubBadgeFallback t3" src="//resources.premierleague.com/premierleague/badges/t' + str(value[1]) + '.png" alt="'+ str(value[1]) + '">'
                                   "</td><td id='bluen'>" + str(value[0][0]) + "</td><td>" +
                                   '<img data-script="pl_player-image" width="110" height="140" data-widget="player-image" data-player="p121145" data-size="110x140" class="img" src="https://resources.premierleague.com/premierleague/photos/players/110x140/p'
                                   + str(value[2]).split('.')[0] +
                                   '.png" alt="' + str(value[0]) + '">' +
                                   "</td>"
                                   "<td id='number'>" + str(value[0][1]) + "</td>"
                                   "<td id='number'>" + str(value[0][2]) + "</td>"
                                   "<td id='number'>" + str(value[0][3]) + "</td>"
                                   "<td id='number'>" + str(value[0][4]) + "</td>"
                                   "<td id='number'>" + str(value[0][5]) + "</td>"
                                   "<td>" + str(value[0][6]) + "</td>"                            
                                   "</tr>", "utf-8"))

        self.wfile.write(bytes("<tr><td id='red'>Total Points</td><td></td><td id='redn'>" + str(points) + "</td><td></td></table>", "utf-8"))
        self.wfile.write(bytes('<a href="/5616897"> Jacob </a>', "utf-8"))
        self.wfile.write(bytes('<a href="/3726424"> Elis </a>', "utf-8"))
        self.wfile.write(bytes('<a href="/7531471"> Mike </a>', "utf-8"))
        self.wfile.write(bytes('<a href="/3927865"> Stew </a>', "utf-8"))
        self.wfile.write(bytes('<a href="/6574078"> Jasper </a>', "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))