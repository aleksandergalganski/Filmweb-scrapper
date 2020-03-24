from bs4 import BeautifulSoup
import requests
import sys
import re


class Film:
    def __init__(self, title, film_type, year, rating, director, actors):
        self._title = str(title)
        self._film_type = film_type
        self._year = str(year)
        self._rating = str(rating)
        self._director = director
        self._actors = actors
    
    @property
    def title(self):
        return self._title
    
    @property
    def film_type(self):
        return self._film_type
    
    @property
    def year(self):
        return self._year
    
    @property
    def rating(self):
        return self._rating
    
    @property
    def director(self):
        return self._director
    
    @property 
    def actors(self):
        return self._actors

    def __str__(self):
        print(f'Title: {self._title}')
        print(f'Type: {self._film_type}')
        print(f'Year: {self._year}')
        print(f'Rating: {self._rating}')
        print(f'Director: {self._director}')
        print('Actors: ')
        for person, role in self._actors.items():
            print(f' {person}: {role}')
    
    def print_stats(self):
        return self.__str__()


def validate_url(url):
    """ Checks if given url is valid """
    pattern = re.compile(r'https://www.filmweb.pl/(serial|film)?.')
    if re.match(pattern, url):
        return True
    return False



def check_type(filmweb_url):
    """ Checks if given film is movie or tv-show """
    pattern = re.compile(r'https://www.filmweb.pl/(serial|film)?.')
    match = re.match(pattern, filmweb_url)

    if match.group(1) == 'serial':
        return 'tv_show'
    return 'movie'


def scrape(filmweb_url):
    source = requests.get(filmweb_url).text
    soup = BeautifulSoup(source, 'lxml')

    # Film title
    title = soup.find('header', class_='filmCoverSection__info').h1.a.text
    
    # Year
    film_year = soup.find('span', class_='filmCoverSection__year').text

    # Rating
    film_rating = soup.find('span', class_='filmRating__rateValue').text

    # Director and Type  
    film_type = None

    if(check_type(filmweb_url) == 'movie'):    
        director_spans = soup.find('div', class_='filmInfo__info cloneToCast cloneToOtherInfo').a.contents
        director = re.split('[<>]', str(director_spans[3]))[2]
        film_type = 'Movie'
    else:
        director_spans = soup.find('div', class_='filmInfo__info cloneToCast').a.contents
        director = re.split('[<>]', str(director_spans[3]))[2]
        film_type = 'TV-show'

    # Actors
    actors = {}
 
    for person_container in soup.find_all('div', class_='personRole__container'):
        person = person_container.find('h3', class_='personRole__person').a.span.text
        role = person_container.find('div', class_='personRole__role').a.span.text

        actors[person] = role
    
    return Film(title, film_type, film_year, film_rating, director, actors)
    

def main():
    filmweb_url = sys.argv[1]
    if(validate_url(filmweb_url)):
        film = scrape(filmweb_url)
        film.print_stats()
    else:
        print('Invalid url')


if __name__ == '__main__':
    main()
