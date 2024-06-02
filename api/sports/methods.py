import requests
from bs4 import BeautifulSoup
from constants import FOOTBALL_URL

def scrape_soccer_matches(day: int):
    match_details_list = []  # List to store match details
    
    data = requests.get(FOOTBALL_URL)
    html_content = data.text
    soup = BeautifulSoup(html_content, 'html.parser')
    daily_matches = soup.find_all("div", class_="football-matches__day")
    
    if daily_matches and day < len(daily_matches):
        tournaments = daily_matches[day].find_all("div", class_="football-table__container")
        
        if tournaments:
            for tournament in tournaments:
                games = tournament.find("tbody")
                if games:
                    for game in games.find_all("tr"):
                        game_time = game.find("time")
                        teams = game.find_all("span", class_="team-name__long")

                        # Extract team names and remove leading/trailing whitespaces and replace \xa0 with space
                        team1_name = teams[0].text.strip().replace('\xa0', ' ')
                        team2_name = teams[1].text.strip().replace('\xa0', ' ')

                        match_details = {
                            'event': tournament.find("a", class_="football-matches__heading").text.strip(),
                            'time': game_time.text.strip().replace('\xa0', ' '),
                            'team1': team1_name,
                            'team2': team2_name
                        }
                        
                        # Add match details to the list
                        match_details_list.append(match_details)
        else:
            return {"error":"no matches found"}
        return match_details_list