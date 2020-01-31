import unittest, os, sys
from imdb_scraper.movie_collection import *

TEST_MOVIE_LIST = [
        Movie(name="Gladiator", year="2000", rating="8.5", metascore="67", votes="1260205", gross="$187.71M"),
        Movie(name="Mememto", year="2000", rating="8.4", metascore="60", votes="1061985", gross="$25.54M"),
        Movie(name="Mememto", year="2000", rating="8.3", metascore="55", votes="741288", gross="$30.33M"),
        Movie(name="Requiem for a Dream", year="2000", rating="8.3", metascore="68", votes="723425", gross="$3.64M"),
        Movie(name="X-Men", year="2000", rating="8.3", metascore="64", votes="549696", gross="$157.30M"),
        Movie(name="Baywatch", year="2017", rating="5.5", metascore="37", votes="148093", gross="$58.06M"),
        Movie(name="The Handmaid's Tale", year="2017-", rating="8.5", metascore="NA", votes="145352", gross="NA"),
        Movie(name="American Made", year="2017", rating="7.1", metascore="65", votes="143953", gross="$51.34M"),
        Movie(name="Big Little Lies", year="2017-2019", rating="8.5", metascore="NA", votes="130706", gross="NA"),
        Movie(name="Transformers: The Last Knight", year="2017", rating="5.2", metascore="27", votes="126285", gross="$130.17M"),
        Movie(name='Gotham', year='(2014–2019)', rating='7.8', votes='202694', gross='NA', metascore='NA'),
        Movie(name='Teenage Mutant Ninja Turtles', year='(2014)', rating='5.8', votes='195126', gross='$191.20M', metascore='31'),
        Movie(name='It Follows', year='(2014)', rating='6.8', votes='193689', gross='$14.67M', metascore='83'),
        Movie(name='The 100', year='(2014– )', rating='7.7', votes='188859', gross='NA', metascore='NA'),
        Movie(name='The Babadook', year='(2014)', rating='6.8', votes='181896', gross='$0.92M', metascore='86'),
        Movie(name='Star Wars: Episode VII - The Force Awakens', year='(2015)', rating='7.9', votes='824039', gross='$936.66M', metascore='81'),
        Movie(name='Mad Max: Fury Road', year='(2015)', rating='8.1', votes='816333', gross='$154.06M', metascore='90'),
        Movie(name='The Martian', year='(2015)', rating='8', votes='711315', gross='$228.43M', metascore='80'),
        Movie(name='Avengers: Age of Ultron', year='(2015)', rating='7.3', votes='697406', gross='$459.01M', metascore='66'),
        Movie(name='The Revenant', year='(2015)', rating='8', votes='654092', gross='$183.64M', metascore='76'),
        Movie(name='Inside Out', year='(I) (2015)', rating='8.2', votes='564669', gross='$356.46M', metascore='94'),
        Movie(name='Jurassic World', year='(2015)', rating='7', votes='554757', gross='$652.27M', metascore='59'),
        Movie(name='Ant-Man', year='(2015)', rating='7.3', votes='531196', gross='$180.20M', metascore='64'),
        Movie(name='The Hateful Eight', year='(2015)', rating='7.8', votes='472936', gross='$54.12M', metascore='68'),
        Movie(name='Spotlight', year='(I) (2015)', rating='8.1', votes='384800', gross='$45.06M', metascore='93'),
        Movie(name='Spectre', year='(I) (2015)', rating='6.8', votes='364133', gross='$200.07M', metascore='60'),
        Movie(name='Furious 7', year='(2015)', rating='7.2', votes='344127', gross='$353.01M', metascore='67'),
        Movie(name='Sicario', year='(2015)', rating='7.6', votes='344078', gross='$46.89M', metascore='82'),
        Movie(name='Room', year='(I) (2015)', rating='8.1', votes='335519', gross='$14.68M', metascore='86'),
        Movie(name='The Big Short', year='(2015)', rating='7.8', votes='327531', gross='$70.26M', metascore='81'),
        Movie(name='Mission: Impossible - Rogue Nation', year='(2015)', rating='7.4', votes='323470', gross='$195.04M', metascore='75'),
        Movie(name='Narcos', year='(2015–2017)', rating='8.8', votes='316140', gross='NA', metascore='NA'),
        Movie(name='Mr. Robot', year='(2015–2019)', rating='8.5', votes='304111', gross='NA', metascore='NA'),
        Movie(name='Fifty Shades of Grey', year='(2015)', rating='4.1', votes='285962', gross='$166.17M', metascore='46'),
        Movie(name='Bridge of Spies', year='(2015)', rating='7.6', votes='271628', gross='$72.31M', metascore='81'),
        Movie(name='Better Call Saul', year='(2015– )', rating='8.7', votes='267618', gross='NA', metascore='NA'),
        Movie(name='The Hunger Games: Mockingjay - Part 2', year='(2015)', rating='6.5', votes='264590', gross='$281.72M', metascore='65'),
        Movie(name='The Man from U.N.C.L.E.', year='(2015)', rating='7.3', votes='250075', gross='$45.45M', metascore='56'),
        Movie(name='Terminator Genisys', year='(2015)', rating='6.4', votes='246924', gross='$89.76M', metascore='38'),
        Movie(name='Creed', year='(II) (2015)', rating='7.6', votes='234111', gross='$109.77M', metascore='82'),
        Movie(name='Spy', year='(2015)', rating='7', votes='219702', gross='$110.83M', metascore='75'),
        Movie(name='Chappie', year='(2015)', rating='6.8', votes='219361', gross='$31.57M', metascore='41'),
        Movie(name='Maze Runner: The Scorch Trials', year='(2015)', rating='6.3', votes='208389', gross='$81.70M', metascore='43'),
        Movie(name='Southpaw', year='(2015)', rating='7.4', votes='206304', gross='$52.42M', metascore='57'),
        Movie(name='Insurgent', year='(2015)', rating='6.2', votes='206176', gross='$130.18M', metascore='42'),
        Movie(name='Minions', year='(2015)', rating='6.4', votes='201103', gross='$336.05M', metascore='56'),
        Movie(name='The Intern', year='(I) (2015)', rating='7.1', votes='200076', gross='$75.76M', metascore='51'),
        Movie(name='Focus', year='(II) (2015)', rating='6.6', votes='200043', gross='$53.86M', metascore='56'),
        Movie(name='San Andreas', year='(2015)', rating='6', votes='199884', gross='$155.19M', metascore='43'),
        Movie(name='The Lobster', year='(2015)', rating='7.2', votes='195629', gross='$8.70M', metascore='82'),

    ]
    
MOVIE_COLLECTION = MovieCollection()
MOVIE_COLLECTION.add_list(TEST_MOVIE_LIST)

class TestMovieCollection(unittest.TestCase):

    # def test_sort_by_rating(self):
    #     print("================================== Sort By Rating ==================================")
    #     MOVIE_COLLECTION.display_sorted(key="rating", mode="DESC")
    #     print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    # def test_sort_by_votes(self):
    #     print("=================================== Sort By Votes ==================================")
    #     MOVIE_COLLECTION.display_sorted(key="votes", mode="DESC")
    #     print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    # def test_sort_by_metascore(self):
    #     print("================================ Sort By Metascore =================================")
    #     MOVIE_COLLECTION.display_sorted(key="metascore", mode="DESC")
    #     print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    # def test_sort_by_gross(self):
    #     print("================================== Sort By Gross ==================================")
    #     MOVIE_COLLECTION.display_sorted(key="gross", mode="DESC")
    #     print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    # def test_sort_by_year(self):
    #     print("================================== Sort By Year ==================================")
    #     MOVIE_COLLECTION.display_sorted(key="year", mode="DESC")
    #     print("^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*")

    def test_interpret_value(self):
        def interpret_value(ivalue):
            sign_list = ["<=", ">=", "<", ">"]
            sign, final_value = None, None
            for xsign in sign_list:
                if ivalue.startswith(xsign):
                    final_value = ivalue.split(xsign)[1].strip()
                    sign = xsign
                    break
            if sign == None:
                final_value = ivalue
            return sign, final_value
        test_list = [
            ("<=3.5", ("<=", "3.5")),
            (">=4.85", (">=", "4.85")),
            ("<7.8", ("<","7.8")),
            (">9.5", (">", "9.5")),
            ("7.2", (None,"7.2"))
        ]
        for (idata,odata) in test_list:
            self.assertEqual(interpret_value(idata), odata)
    


if __name__ == "__main__":
    unittest.main()