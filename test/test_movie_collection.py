import unittest, os, sys
from imdb_scraper.movie_collection import *

TEST_MOVIE_LIST = [
        Movie(name="Gladiator", year="2000", rating="8.5", metascore="67", votes="1260205", gross="$187.71M"),
        Movie(name="Mememto", year="2000", rating="8.4", metascore="60", votes="1061985", gross="$25.54M"),
        Movie(name="Mememto", year="2000", rating="8.3", metascore="55", votes="741288", gross="$30.33M"),
        Movie(name="Requiem for a Dream", year="2000", rating="8.3", metascore="68", votes="723425", gross="$3.64M"),
        Movie(name="X-Men", year="2000", rating="7.4", metascore="64", votes="549696", gross="$157.30M"),
        Movie(name="Baywatch", year="2017", rating="5.5", metascore="37", votes="148093", gross="$58.06M"),
        Movie(name="The Handmaid's Tale", year="2017-", rating="8.5", metascore="NA", votes="145352", gross="NA"),
        Movie(name="American Made", year="2017", rating="7.1", metascore="65", votes="143953", gross="$51.34M"),
        Movie(name="Big Little Lies", year="2017-2019", rating="8.5", metascore="NA", votes="130706", gross="NA"),
        Movie(name="Transformers: The Last Knight", year="2017", rating="5.2", metascore="27", votes="126285", gross="$130.17M"),
    ]
    
MOVIE_COLLECTION = MovieCollection()
MOVIE_COLLECTION.add_list(TEST_MOVIE_LIST)

class TestMovieCollection(unittest.TestCase):

    def test_sort_by_rating(self):
        print("================================== Sort By Rating ==================================")
        MOVIE_COLLECTION.display_sorted(key="rating", mode="DESC")
        print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    def test_sort_by_votes(self):
        print("=================================== Sort By Votes ==================================")
        MOVIE_COLLECTION.display_sorted(key="votes", mode="DESC")
        print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    def test_sort_by_metascore(self):
        print("================================ Sort By Metascore =================================")
        MOVIE_COLLECTION.display_sorted(key="metascore", mode="DESC")
        print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    def test_sort_by_gross(self):
        print("================================== Sort By Gross ==================================")
        MOVIE_COLLECTION.display_sorted(key="gross", mode="DESC")
        print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    def test_sort_by_year(self):
        print("================================== Sort By Year ==================================")
        MOVIE_COLLECTION.display_sorted(key="year", mode="DESC")
        print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

if __name__ == "__main__":
    unittest.main()