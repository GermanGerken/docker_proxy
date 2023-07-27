import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from extention import proxies

username = "TmeYnrhX"
password = "uKz58Zbn"
endpoint = "62.76.146.185"
port = "64072"

url = 'https://www.themoviedb.org/'

chrome_options = webdriver.ChromeOptions()

proxies_extension = proxies(username, password, endpoint, port)

chrome_options.add_extension(proxies_extension)
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("start-maximized")


def get_movie_info(driver, url):
    movie = {
        "name": "",
        "rating": "",
        "premier_date": "",
        "Overview": ""
    }
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    movie["name"] = soup.find("div", class_="title").find("a").text
    movie["rating"] = int(float(soup.find("div", class_="user_score_chart")["data-percent"]))
    try:
        movie["premier_date"] = str(soup.find("span", class_="release").text).strip("\n").strip()
    except:
        movie["premier_date"] = "not set"
    movie["Overview"] = soup.find("div", class_="overview").find("p").text

    return movie


def main():
    chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    chrome.get(url)
    time.sleep(3)
    chrome.find_element(By.XPATH, '//*[@id="main"]/section[2]/div/div/div/div[1]/div/div/div[2]/h3/a').click()
    time.sleep(3)
    html = chrome.page_source
    soup = BeautifulSoup(html, "html.parser")
    trending_container = soup.find("div", class_="column_content flex scroller loaded")
    movies = trending_container.find_all("div", class_="card style_1")

    list_of_movies = []

    for movie in movies:
        movie_link = "https://www.themoviedb.org" + str(movie.find("a", class_="image")["href"])
        list_of_movies.append(get_movie_info(chrome, movie_link))

    sorted_movies = sorted(list_of_movies, key=lambda x: x["rating"], reverse=True)

    print(sorted_movies)


if __name__ == "__main__":
    main()
