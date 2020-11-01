# ----------------------------------- importing library -----------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests as re
from bs4 import BeautifulSoup
import csv
import time

# -------------------------------------------------------------------------------------------

class Imdb():

    # ----------------------- constructor ----------------------------
    def __init__(self, url):
        self.url = url
        self.data = []


    # ------------------------------ function that open Mozila ---------------------
    def __OpenMozila(self):
        try:
            driver = webdriver.Firefox()
            driver.get(self.url)
            time.sleep(2)
            return driver
        except:
            print("Something went wrong.")


    # ----------------------- some element finding ------------------------------
    def __find_top_rated_movies(self):
        driver = self.__OpenMozila()
        try:
            menu = driver.find_element_by_id('imdbHeader-navDrawerOpen--desktop')
            menu.click()
            time.sleep(2)
            try:
                links = driver.find_elements_by_css_selector('a.ipc-list__item--indent-one')
                links[2].click()
                time.sleep(2)
                print(driver.current_url)
                return driver.current_url

            except:
                print('Can not find class')
        except:
            print('Can not find this id')

    # -------------------------- find each top rated movie--------------------
    def __find_each_top_rated_movie(self):
        child_data = []
        link = self.__find_top_rated_movies()
        try:
            req_1 = re.get(link)
            bs_1 = BeautifulSoup(req_1.text, 'html.parser')
            links_data = bs_1.find_all('td', attrs={
                'class':'titleColumn'
            })

            # ----------------finding chind ----------------------
            for link_data in links_data:
                child = link_data.contents[1]['href']
                child_data.append('https://www.imdb.com'+child)
            return child_data
        except:
            print(f'Error in finding link --<{link}')


    # --------------------------- find each movie detail -------------------

    def find_each_top_rated_movie_detail(self):
        movies = self.__find_each_top_rated_movie()
        for movie in movies:
            try:
                m = re.get(movie)
                time.sleep(2)
                b_m = BeautifulSoup(m.text, 'html.parser')
                try:
                    title = b_m.find('div', attrs={
                        'class':'originalTitle'
                    }).text
                except:
                    try:
                        title = b_m.find('div', {
                            'class': 'title_wrapper'
                        }).find('h1').text.split("\xa0")[0]
                    except:
                        print('Error in title find')
                try:
                    time_T = b_m.find('time').text
                except:
                    print('Error in time find')
                try:
                    rating = b_m.find('span', attrs={
                        'itemprop':'ratingValue'
                    }).text
                except:
                    print('Error in rating find')
                try:
                    total_r = b_m.find('span', attrs={
                        'itemprop':'bestRating'
                    }).text
                except:
                    print('Error in total find')
                try:
                    summary_text = b_m.find('div', attrs={
                        'class':'summary_text'
                    }).text.strip()
                except:
                    print('Error in summery text find')
                try:
                    director = b_m.find('div', attrs={
                        'class':'credit_summary_item'
                    }).findChild('a').text
                except:
                    print('Error in director find')
                try:
                    writters_all = b_m.find_all('div', attrs={
                        'class':'credit_summary_item'
                    })[1].findChildren("a")

                    writters = ''
                    for writter in writters_all:
                        writters += writter.text+', '
                except:
                    print('Error in writers find')
                try:
                    reviews = b_m.find('a', {
                        'href':'reviews'
                    }).text
                except:
                    print('Error in reviews find')

                self.data.append({
                    'Movie Title':title,
                    'Movie Time': time_T.strip(),
                    'Rating':rating,
                    'Total': total_r,
                    'About Movie': summary_text,
                    'Director':director,
                    'Writers':writters,
                    'Reviews':reviews

                })

                print(self.data)

            except:
                print(f'Error in movies : {movie}')



    # --------------------- save as csv file --------------------------------

    def save_file_as_csv(self):
        with open('IMDB_FILE.csv', 'w') as imdb_file:
            imdb_writer = csv.DictWriter(imdb_file, fieldnames=[
                'Movie Title',
                'Movie Time',
                'Rating',
                'Total',
                'About Movie',
                'Director',
                'Writers',
                'Reviews'

            ])
            imdb_writer.writeheader()
            for data in self.data:
                imdb_writer.writerow(data)
