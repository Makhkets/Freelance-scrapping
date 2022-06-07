import requests
import json
from bs4 import BeautifulSoup

class Bot:
    def __init__(self):
        self.url = "https://freelance.habr.com/tasks"
        self.session = requests.session()
        self.session.headers.update({
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
                                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                                            "Accept-Language": "en-US,en;q=0.5",
                                            "Accept-Encoding": "gzip, deflate, br",
                                            "Upgrade-Insecure-Requests": "1",
                                    })


    def GetCountPages(self, soup):
        return int(soup.find("div", {"class": "pagination"}).find_all("a")[len(soup.find("div", {"class": "pagination"}).find_all("a")) - 2].text)

    def launch(self):
        data = {}
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        for page in range(self.GetCountPages(soup) + 1)[:5]:
            response = self.session.get(self.url + "?page=" + str(page))
            soup = BeautifulSoup(response.text, "lxml")
            for li in soup.find_all("li", {"class": "content-list__item"}):
                link = self.url + li.find("a")["href"]
                title = li.find("div", {"class": "task__title"}).text.strip()
                responses = "Нет откликов"
                if li.find("i", {"class": "params__count"}):
                    responses = li.find("i", {"class": "params__count"}).text.strip()
                views = "Нет просмотров"
                if li.find("i", {"class": "params__count"}):
                    views = li.find("i", {"class": "params__count"}).text.strip()
                time = li.find("span", {"class": "params__published-at icon_task_publish_at"}).text.strip()
                data[title] = {
                                            "title": title,
                                            "responses": responses,
                                            "views": views,
                                            "time": time,
                                            "url": link
                }
        return data

def main():
    file = "data.json"
    bot = Bot()
    response = bot.launch()
    with open(file, "w", encoding="utf-8") as file: json.dump(response, file, indent=4, ensure_ascii=False)
            
if __name__ == "__main__":
    main()

