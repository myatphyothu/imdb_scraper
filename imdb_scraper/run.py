import os,sys
from time import sleep, time
from random import randint
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn

MAIN_URL = 'http://www.imdb.com/search/title?release_date='
HEADERS = {"Accept-Language": "en-US, en;q=0.5"}

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
    test_df = pd.DataFrame({'movie': [x["name"] for x in MOVIES_LIST],
        'year': [x["year"] for x in MOVIES_LIST],
        'rating': [x["rating"] for x in MOVIES_LIST],
        'metascore': [x["metascore"] for x in MOVIES_LIST],
        'votes': [x["votes"] for x in MOVIES_LIST],
        'gross': [x["gross"] for x in MOVIES_LIST]
        })
    print(test_df[['movie', 'year', 'rating', 'metascore', 'votes', 'gross']])
#--------------------------------------------------------------------------------------


def main(args):
    global MOVIES_LIST,HEADERS,MAIN_URL
    pages = [str(i) for i in range(1,5)]
    years_url = [str(i) for i in range(2000,2018)]  
    start_time = time()
    requests, expected_requests = 0, 72
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
                    year = get_year(movie_container)
                    metascore = get_metascore(movie_container)
                    rating = get_rating(movie_container)
                    votes,gross = get_votes_and_gross(movie_container)
                    MOVIES_LIST.append({"name":name,"year":year,"metascore":metascore,"rating":rating,"votes":votes,"gross":gross})
                
    sys.stdout.write("\nscraping completed....\n")
    display()       

if __name__ == "__main__":
    main(sys.argv[1:])