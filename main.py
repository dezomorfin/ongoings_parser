from bs4 import BeautifulSoup
import requests
import sqlite3

def parser(url):
    link_list = []
    name_list = []
    genres_list = []
    year_list = []
    page = 1
    while page != 6:
        res = requests.get(f'{url}?page={page}')
        soup = BeautifulSoup(res.text, 'lxml')
        animes = soup.find_all("div", class_='knb-cell')

        for anime in animes:
            try:
                link_elem = anime.find('a', class_='knb-card--image style_wrap___iepK').get('href')
                full_link = (f'https://kanobu.ru{link_elem}')
                name = anime.find("img", class_='knb-card--image').get('alt')
                genres = anime.find('div', class_='BaseElementCard_genres__FAQda').text
                year = anime.find('div', class_='BaseElementCard_date__sbPY9').text
            except AttributeError:
                continue
            link_list.append(full_link)
            name_list.append(name)
            genres_list.append(genres)
            year_list.append(year)
        page += 1
    hello_database(link_list, name_list, genres_list, year_list)



def hello_database(link_list, name_list, genres_list, year_list):
    con = sqlite3.connect('ongoings.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS ongoings (name TEXT, year TEXT, genres TEXT, link TEXT)')
    data = list(zip(name_list, year_list, genres_list, link_list))
    cur.executemany('INSERT INTO ongoings (name, year, genres, link) VALUES (?, ?, ?, ?)', data)
    con.commit()

if __name__ == '__main__':
    parser(url='https://kanobu.ru/anime/new/')