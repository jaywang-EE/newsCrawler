from .utils import *

def get_news():
    return get_newsAPI()

def craw_gov():
    return {
        "michigan": craw_gov_michgan(),
    }

def craw_gov_michgan():
    url = "https://www.michigan.gov/coronavirus/0,9753,7-406-98158---,00.html"
    soup = get_soup(url)

    divs = soup.find("div", class_="monthlyIndex").find_all("div", class_="indexRow", recursive=False)

    news = []
    for div in divs:
        try:
            title = div.find("a", class_="bodylinks")
            d     = int(div.find("span", class_="date").text)
            m     = monthToInt(div.find("span", class_="month").text)
            y     = int(div.find("span", class_="year").text)
            news.append({"title": title["href"], "url": title.text, "date": "%d-%02d-%02d"%(y, m, d)})
        except:
            print("can't parse craw_gov_michgan: "+str(div))

    return news

if __name__ == '__main__':
    print(get_news())