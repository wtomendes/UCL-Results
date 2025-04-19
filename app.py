from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.football-data.org/v4/competitions/CL/matches'


@app.route('/') 
def home():
    return champions_league_results()

@app.route('/champions-league-results')
def champions_league_results():
    headers = {'X-Auth-Token': API_KEY}
    params = {'status': 'FINISHED', 'limit': 10}
    
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        matches = sorted(
            data['matches'],
            key=lambda m: m['utcDate'],
            reverse=True
        )

        jogos = [
            {
                'date': match['utcDate'][:10],
                'home': match['homeTeam']['name'],
                'away': match['awayTeam']['name'],
                'score': f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}",
                'stage': match['stage']  
            }
            for match in matches
        ]

        return render_template('index.html', jogos=jogos)
    
    else:
        return f"Erro ao buscar os dados da API: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)



