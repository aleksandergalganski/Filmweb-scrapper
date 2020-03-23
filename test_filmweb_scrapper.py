import unittest

from filmweb_scrapper import validate_url, check_type, scrape


class TestValidateUrl(unittest.TestCase):
    
    def setUp(self):
        self.invalid_url = 'https://w.filmweb'
        self.valid_serial_url = 'https://www.filmweb.pl/serial/Czarnobyl-2019-799827'
        self.valid_film_url = 'https://www.filmweb.pl/film/Skyfall-2012-451244'
        self.valid_shorter_serial_url = 'https://www.filmweb.pl/Sherlock.Holmes' 
        self.blank_url = ''
    
    def test_invalid_url(self):
        self.assertFalse(validate_url(self.invalid_url))
    
    def test_valid_serial_url(self):
        self.assertTrue(validate_url(self.valid_serial_url))

    def test_valid_film_url(self):
        self.assertTrue(validate_url(self.valid_film_url))

    def test_valid_shorter_film_url(self):
        self.assertTrue(validate_url(self.valid_shorter_serial_url))
    def test_blank_url(self):
        self.assertFalse(validate_url(self.blank_url))


class TestCheckType(unittest.TestCase):
    
    def setUp(self):
        self.serial_url = 'https://www.filmweb.pl/serial/House+of+Cards-2013-620036'
        self.film_url = 'https://www.filmweb.pl/film/Parasite-2019-798143'
    
    def test_tvshow_type(self):
        self.assertEqual(check_type(self.serial_url), 'tv_show')
    
    def test_film_type(self):
        self.assertEqual(check_type(self.film_url), 'movie')


class TestScrape(unittest.TestCase):

    def setUp(self):
        self.movie_url = 'https://www.filmweb.pl/film/Skyfall-2012-451244'
        self.movie = scrape(self.movie_url)
        self.tvshow_url = 'https://www.filmweb.pl/serial/House+of+Cards-2013-620036'
        self.tvshow = scrape(self.tvshow_url)

    def test_title(self):
        valid_movie_title = 'Skyfall'
        valid_tvshow_title = 'House of Cards'
        self.assertEqual(self.tvshow.title, valid_tvshow_title)
        self.assertEqual(self.movie.title, valid_movie_title)
    
    def test_film_type(self):
        self.assertEqual(self.tvshow.film_type, 'TV-show')
        self.assertEqual(self.movie.film_type, 'Movie')

    def test_year(self):
        self.assertEqual(self.tvshow.year, '2013-2018')
        self.assertEqual(self.movie.year, '2012')

    def test_rating(self):
        self.assertEqual(self.tvshow.film_type, 'TV-show')
        self.assertEqual(self.movie.film_type, 'Movie')

    def test_directors(self):
        self.assertEqual(self.tvshow.director, 'Beau Willimon')
        self.assertEqual(self.movie.director, 'Sam Mendes')

    def test_three_actors(self):
        movie_actors = [
            ('Daniel Craig', 'James Bond'),
            ('Judi Dench', 'M'),
            ('Javier Bardem', 'Raoul Silva')
        ]

        tvshow_actors = [
            ('Kevin Spacey', 'Francis Underwood'),
            ('Robin Wright', 'Claire Underwood'),
            ('Michael Kelly', 'Doug Stamper')
        ]
        self.assertEqual(list(self.tvshow.actors.items())[:3], tvshow_actors)
        self.assertEqual(list(self.movie.actors.items())[:3], movie_actors)


if __name__ == '__main__':
    unittest.main()