import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import uuid
import json
#from flask import Flask, request, jsonify, render_template

#app = Flask(__name__)

session_id = str(uuid.uuid4())

def callAPI(url, params):
    headers = {
        "X-Session-ID": session_id,
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers = headers, params = params)
    # print("Response from " + url + ": " + str(response.status_code))
    if (response.status_code != 200):
        return None
    return response.json()["data"]

def getLeagueStats():
    data = callAPI("https://ch.tetr.io/api/general/stats", {})
    count = data["rankedcount"]
    stats = []
    data = callAPI("https://ch.tetr.io/api/users/by/league", {"limit": 100})
    for entry in data["entries"]:
        stats.append(entry["league"])
    last_prisecter = data["entries"][-1]["p"]
    for i in range(1, int(count / 100)):
        after = f'{last_prisecter["pri"]}:{last_prisecter["sec"]}:{last_prisecter["ter"]}'
        data = callAPI("https://ch.tetr.io/api/users/by/league", {"limit": 100, "after": after})
        for entry in data["entries"]:
            stats.append(entry["league"])
        last_prisecter = data["entries"][-1]["p"]
        # print(i)
    after = f'{last_prisecter["pri"]}:{last_prisecter["sec"]}:{last_prisecter["ter"]}'
    data = callAPI("https://ch.tetr.io/api/users/by/league", {"limit": count % 42706, "after": after})
    for entry in data["entries"]:
        stats.append(entry["league"])
    # print(len(stats))
    with open("league_stats.json", "w") as f:
        f.write(str(stats))

def regression(x, y, degree):
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x)
    model = LinearRegression()
    model.fit(x_poly, y)
    # print("Model R² score:", model.score(x_poly, y))
    return model, poly

def statsToGlicko(apm, pps, vs):
    with open("league_stats.json", "r") as f:
        data = json.load(f)
    x = np.array([[player['apm'], player['pps'], player['vs'], player['apm'] / player['pps'], player['vs'] / player['pps'], player['vs'] / player['apm']] for player in data])
    y = np.array([player["glicko"] for player in data])
    model, poly = regression(x, y, 2)
    apmpps = apm / pps
    vspps = vs / pps
    vsapm = vs / apm
    input_features = np.array([[apm, pps, vs, apmpps, vspps, vsapm]])
    predicted_glicko = model.predict(poly.transform(input_features))
    return predicted_glicko[0]

def estimateGlicko(player):
    data = callAPI("https://ch.tetr.io/api/users/" + player + "/summaries/league", {})
    return (f"{player}'s estimated glicko is: {statsToGlicko(data['apm'], data['pps'], data['vs'])}")

def getPlaystyle(player):
    data = callAPI("https://ch.tetr.io/api/users/" + player + "/summaries/league", {})
    glicko = data["glicko"]
    pps = data["pps"]
    apm = data["apm"]
    vs = data["vs"]
    dsm = vs * 60 / 100 - apm
    dsp = dsm / (pps * 60)
    app = apm / (pps * 60)
    plonk = vs / (pps * 60)
    defense = vs / apm
    with open("league_stats.json", "r") as f:
        data = json.load(f)
    x = np.array([[player["glicko"]] for player in data])
    y = np.array([player["pps"] for player in data])
    pps_model, pps_poly = regression(x, y, 3)
    x = np.array([[player["glicko"]] for player in data])
    y = np.array([player["apm"] for player in data])
    apm_model, apm_poly = regression(x, y, 3)
    x = np.array([[player["glicko"]] for player in data])
    y = np.array([player["vs"] for player in data])
    vs_model, vs_poly = regression(x, y, 3)
    playstyle = ""
    playstyle += (player + " analysis:" + "\n")
    playstyle += (player + " glicko: " + f"{glicko}" + "\n")
    playstyle += ("Category | " + player + " stats | Expected stats at " + f"{glicko}" + " glicko" + "\n")
    col_width = len(player) + 9
    pps_predict = pps_model.predict(pps_poly.transform([[glicko]]))[0]
    playstyle += ("pps:       " + f"{pps:<{col_width}.2f}{pps_predict:.2f}" + "\n")
    apm_predict = apm_model.predict(apm_poly.transform([[glicko]]))[0]
    playstyle += ("apm:       " + f"{apm:<{col_width}.2f}{apm_predict:.2f}" + "\n")
    vs_predict = vs_model.predict(vs_poly.transform([[glicko]]))[0]
    playstyle += ("vs:        " + f"{vs:<{col_width}.2f}{vs_predict:.2f}" + "\n")
    app_predict = apm_predict / (pps_predict * 60)
    playstyle += ("app:       " + f"{app:<{col_width}.2f}{app_predict:.2f}" + "\n")
    dsm_predict = vs_predict * 60 / 100 - apm_predict
    playstyle += ("dsm:       " + f"{dsm:<{col_width}.2f}{dsm_predict:.2f}" + "\n")
    dsp_predict = dsm_predict / (pps_predict * 60)
    playstyle += ("dsp:       " + f"{dsp:<{col_width}.2f}{dsp_predict:.2f}" + "\n")
    plonk_predict = vs_predict / (pps_predict * 60)
    playstyle += ("plonk:     " + f"{plonk:<{col_width}.2f}{plonk_predict:.2f}" + "\n")
    defense_predict = vs_predict / apm_predict
    playstyle += ("defense:   " + f"{defense:<{col_width}.2f}{defense_predict:.2f}")
    return playstyle

def getLeagueRecord(player, after):
    if (after == None):
        data = callAPI("https://ch.tetr.io/api/users/" + player + "/records/league/recent", {"limit": 10})
    else:
        data = callAPI("https://ch.tetr.io/api/users/" + player + "/records/league/recent", {"limit": 10, "after": after})
    return data["entries"]

def getMatchupModel(player):
    data = getLeagueRecord(player, None)
    x_reg = []
    y_reg = []
    for match in data:
        if match["results"]["leaderboard"][0]["username"] == player:
            opp = match["results"]["leaderboard"][1]["username"]
            oppPps = match["results"]["leaderboard"][1]["stats"]["pps"]
            oppApm = match["results"]["leaderboard"][1]["stats"]["apm"]
            oppVs = match["results"]["leaderboard"][1]["stats"]["vsscore"]
            winrate = match["results"]["leaderboard"][0]["wins"] / (match["results"]["leaderboard"][0]["wins"] + match["results"]["leaderboard"][1]["wins"])
        else:
            opp = match["results"]["leaderboard"][0]["username"]
            oppPps = match["results"]["leaderboard"][0]["stats"]["pps"]
            oppApm = match["results"]["leaderboard"][0]["stats"]["apm"]
            oppVs = match["results"]["leaderboard"][0]["stats"]["vsscore"]
            winrate = match["results"]["leaderboard"][1]["wins"] / (match["results"]["leaderboard"][0]["wins"] + match["results"]["leaderboard"][1]["wins"])
        oppApmpps = oppApm / oppPps
        oppVspps = oppVs / oppPps
        oppVsapm = oppVs / oppApm
        oppData = getLeagueRecord(opp, f'{match["p"]["pri"]}:{match["p"]["sec"]}:{match["p"]["ter"]}')
        oppPpsAvg = 0.0
        oppApmAvg = 0.0
        oppVsAvg = 0.0
        count = 0
        for oppMatch in oppData:
            if oppMatch["results"]["leaderboard"][0]["stats"]["pps"] == None or oppMatch["results"]["leaderboard"][1]["stats"]["pps"] == None:
                break
            if oppMatch["results"]["leaderboard"][0]["username"] == opp:
                oppPpsAvg += oppMatch["results"]["leaderboard"][0]["stats"]["pps"]
                oppApmAvg += oppMatch["results"]["leaderboard"][0]["stats"]["apm"]
                oppVsAvg += oppMatch["results"]["leaderboard"][0]["stats"]["vsscore"]
            else:
                oppPpsAvg += oppMatch["results"]["leaderboard"][1]["stats"]["pps"]
                oppApmAvg += oppMatch["results"]["leaderboard"][1]["stats"]["apm"]
                oppVsAvg += oppMatch["results"]["leaderboard"][1]["stats"]["vsscore"]
            count += 1
        oppPpsAvg /= count
        oppApmAvg /= count
        oppVsAvg /= count
        oppApmppsAvg = oppApmAvg / oppPpsAvg
        oppVsppsAvg = oppVsAvg / oppPpsAvg
        oppVsapmAvg = oppVsAvg / oppApmAvg
        x_reg.append([oppPps, oppApm, oppVs, oppApmpps, oppVspps, oppVsapm, oppPpsAvg, oppApmAvg, oppVsAvg, oppApmppsAvg, oppVsppsAvg, oppVsapmAvg])
        y_reg.append(winrate)
    return regression(x_reg, y_reg, 3)

def getMatchupPlayers(player1, player2):
    model1, poly1 = getMatchupModel(player1)
    model2, poly2 = getMatchupModel(player2)
    data1 = callAPI("https://ch.tetr.io/api/users/" + player1 + "/summaries/league", {})
    pps1 = data1["pps"]
    apm1 = data1["apm"]
    vs1 = data1["vs"]
    apmpps1 = apm1 / pps1
    vspps1 = vs1 / pps1
    vsapm1 = vs1 / apm1
    data2 = callAPI("https://ch.tetr.io/api/users/" + player2 + "/summaries/league", {})
    pps2 = data2["pps"]
    apm2 = data2["apm"]
    vs2 = data2["vs"]
    apmpps2 = apm2 / pps2
    vspps2 = vs2 / pps2
    vsapm2 = vs2 / apm2
    win1 = model1.predict(poly1.transform(np.array([[pps2, apm2, vs2, apmpps2, vspps2, vsapm2, pps2, apm2, vs2, apmpps2, vspps2, vsapm2]])))
    win2 = model2.predict(poly2.transform(np.array([[pps1, apm1, vs1, apmpps1, vspps1, vsapm1, pps1, apm1, vs1, apmpps1, vspps1, vsapm1]])))
    winrate = win1 * 100 / (win1 + win2)
    return (f"{player1} has a {winrate[0]}% chance of beating {player2}")

def getMatchupStats(player, apm, pps, vs):
    model, poly = getMatchupModel(player)
    winrate = model.predict(poly.transform(np.array([[pps, apm, vs, apm / pps, vs / pps, vs / apm, pps, apm, vs, apm / pps, vs / pps, vs / apm]]))) * 100
    return (f"{player} has a {winrate[0]}% chance of beating those stats")

def getOpenerCoefficient(player):
    data = getLeagueRecord(player, None)
    times = []
    wins = []
    for match in data:
        for round in match["results"]["rounds"]:
            if round[0]["username"] == player:
                wins.append(round[0]["stats"]["kills"])
                times.append([round[0]["lifetime"]])
            else:
                wins.append(round[1]["stats"]["kills"])
                times.append([round[1]["lifetime"]])
    x = np.array(times)
    y = np.array(wins)
    model = LinearRegression()
    model.fit(x, y)
    winrate = model.coef_[0] * 100
    return (f"For every second a round takes, {player}'s win rate changes by about {winrate}%")
'''
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if data["function"] == "statsToGlicko":
            return jsonify({"result": statsToGlicko(data["apm"], data["pps"], data["vs"])})
        elif data["function"] == "estimateGlicko":
            return jsonify({"result": estimateGlicko(data["player"])})
        elif data["function"] == "getPlaystyle":
            return jsonify({"result": getPlaystyle(data["player"])})
        elif data["function"] == "getMatchupPlayers":
            return jsonify({"result": getMatchupPlayers(data["player"], data["opponent"])})
        elif data["function"] == "getMatchupStats":
            return jsonify({"result": getMatchupStats(data["player"], data["apm"], data["pps"], data["vs"])})
        elif data["function"] == "getOpenerCoefficient":
            return jsonify({"result": getMatchupStats(data["player"])})
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input."}), 400
'''
# Start the server (Render detects and exposes this)
# if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=10000)
print(getPlaystyle("pentag"))