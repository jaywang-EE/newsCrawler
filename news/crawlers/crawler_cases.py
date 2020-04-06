from .utils import *

MAIN_URL = "https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html#map"
COUNTY_DATA_URL = "https://github.com/nytimes/covid-19-data/raw/master/us-counties.csv"
STATE_DATA_URL  = "https://github.com/nytimes/covid-19-data/raw/master/us-states.csv"

def get_county_data():
    data = download_github(COUNTY_DATA_URL)
    return data

def get_state_data():
    data = download_github(STATE_DATA_URL)
    return data

def get_county():
    soup = get_soup(MAIN_URL)
    states = soup.find("div", class_="g-footer-asset").find("ul", class_="columns svelte-mmjzxm").find_all("li", recursive=False)
    for state in states:
        url = state.find("a")["href"]
        print(state.text, url)
        craw_state(url)

def craw_state(state_url):
    soup = get_soup(state_url)
    total = soup.find("div", id="cases-top-presentation").find("div", class_="counts svelte-1aesbb8").find_all("div", recursive=False)
    total_comfirmed = comma_str2int(total[0].find_all("div", recursive=False)[1].text)
    total_death     = comma_str2int(total[1].find_all("div", recursive=False)[1].text)

    table = soup.find("div", id="county").find("table").find("tbody")
    print(table)

