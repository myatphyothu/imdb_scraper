import os,sys,pickle
from time import sleep, time
from random import randint
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
from .movie_collection import *

MAIN_URL = 'http://www.imdb.com/search/title?release_date='
HEADERS = {"Accept-Language": "en-US, en;q=0.5"}
PICKLE_FILE="imdb_scraper/movie_collection.pickle"
MOVIE_COLLECTION = MovieCollection()
MOVIES_LIST = []

#--------------------------------------------------------------------------------------
def get_elem(parent, find_elem, elem_type, elem_name):
    if parent is None:
        return None
    elem = None
    try:
        if elem_type == "class":
            elem = parent.find(find_elem, class_=elem_name)
    except:
        elem = None
    return elem
#--------------------------------------------------------------------------------------

def get_metascore(movie_container):
    metascore = get_elem(movie_container, "div", "class", "inline-block ratings-metascore")
    if metascore is not None:
        return metascore.span.text.strip()
    else:
        return "NA"
    
#--------------------------------------------------------------------------------------
def get_rating(movie_container):
    rating = get_elem(movie_container,"div","class","inline-block ratings-imdb-rating")
    if rating is not None:
        return rating["data-value"]
    else:
        return "NA"
#--------------------------------------------------------------------------------------
def get_year(movie_container):
    year = get_elem(movie_container.h3, "span", "class", "lister-item-year text-muted unbold")
    if year is not None:
        return year.text
    else:
        return "NA"
#--------------------------------------------------------------------------------------
def get_votes_and_gross(movie_container):
    votes,gross = "NA","NA"
    voting_div = get_elem(movie_container, "p", "class", "sort-num_votes-visible")
    if voting_div:
        spans = voting_div.find_all("span", attrs={"name":"nv"})
        if len(spans) > 0:
            votes = spans[0]["data-value"]
        if len(spans) > 1:
            gross = spans[1].text
    return votes,gross
#--------------------------------------------------------------------------------------
def display():
    global MOVIES_LIST
    print("%d new movies added..." % len(MOVIES_LIST))
    test_df = pd.DataFrame({'movie': [x["name"] for x in MOVIES_LIST],
        'year': [x["year"] for x in MOVIES_LIST],
        'rating': [x["rating"] for x in MOVIES_LIST],
        'metascore': [x["metascore"] for x in MOVIES_LIST],
        'votes': [x["votes"] for x in MOVIES_LIST],
        'gross': [x["gross"] for x in MOVIES_LIST]
        })
    print(test_df[['movie', 'year', 'rating', 'metascore', 'votes', 'gross']])
#--------------------------------------------------------------------------------------
def load_movie_collection():
    global PICKLE_FILE,MOVIE_COLLECTION
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE,"rb") as pickle_file:
            MOVIE_COLLECTION = pickle.load(pickle_file)
#--------------------------------------------------------------------------------------
def scrape():
    global MOVIES_LIST,MOVIE_COLLECTION,PICKLE_FILE, HEADERS,MAIN_URL
    pages = [str(i) for i in range(1,5)]
    years_url = [str(i) for i in range(2000,2018)]  
    start_time = time()
    requests, expected_requests = 0, 72

    print("preparing to scrape...")

    for year_url in years_url:
        for page in pages:
            response = get(MAIN_URL + year_url + "&sort=num_votes,desc&page=" + page, headers=HEADERS)

            #pause the loop to avoid getting the IP banned
            #sleep(1)

            requests += 1
            elapsed_time = time() - start_time
            sys.stdout.write("request: %d; frequency: %2.8f req/s\r" % (requests, requests/elapsed_time))
            #clear_output(wait = True)

            # warning for non-200 status codes
            if response.status_code != 200:
                warn("request:{}; status_code: {]}".format(requests, response.status_code))

            if requests > expected_requests:
                warn("Number of requests greater than expected")
                break

            page_html = BeautifulSoup(response.text, "html.parser")

            # select all 50 movie containers from a single page
            movie_containers = page_html.find_all("div", class_="lister-item mode-advanced")

            # terminate loop if #requests > expected

    
            if len(movie_containers) > 0:
                for movie_container in movie_containers:
                    name = movie_container.h3.a.text

                    if MOVIE_COLLECTION.exists(name):
                        continue

                    year = get_year(movie_container)
                    metascore = get_metascore(movie_container)
                    rating = get_rating(movie_container)
                    votes,gross = get_votes_and_gross(movie_container)
                    
                    MOVIES_LIST.append({"name":name,"year":year,"metascore":metascore,"rating":rating,"votes":votes,"gross":gross})
                
    sys.stdout.write("\nscraping completed....\n")
    display()       
    for movie in MOVIES_LIST:
        movie = Movie(**movie)
        MOVIE_COLLECTION.add(movie)
    
    with open(PICKLE_FILE, "wb") as pickle_file:
        pickle.dump(MOVIE_COLLECTION, pickle_file)
    
#--------------------------------------------------------------------------------------
def display_movie_collection():
    global MOVIE_COLLECTION
    MOVIE_COLLECTION.display()
#--------------------------------------------------------------------------------------
def main(args):
    global MOVIE_COLLECTION

    load_movie_collection()

    if len(args) == 0:
        print("no args provided...")
        exit()

    if args[0] == "scrape":
        scrape()
    elif args[0] == "display":
        display_movie_collection()
    elif args[0] == "sort":
        sub_args = args[1:]
        if len(sub_args) == 0:
            print("insufficient arguments...")
            exit()
        else:
            pass

        print("Invalid args provided...")
        exit()

if __name__ == "__main__":
    main(sys.argv[1:])