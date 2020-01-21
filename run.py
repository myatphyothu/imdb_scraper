import os,sys
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

MAIN_URL = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'


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

def main(args):
    global MOVIES_LIST
    page_response = get(MAIN_URL)
    html_soup = BeautifulSoup(page_response.text, "html.parser")
    movie_containers = html_soup.find_all("div", class_="lister-item mode-advanced")

    if len(movie_containers) > 0:
        for movie_container in movie_containers:
            name = movie_container.h3.a.text
            year = get_year(movie_container)
            metascore = get_metascore(movie_container)
            rating = get_rating(movie_container)
            votes,gross = get_votes_and_gross(movie_container)
            MOVIES_LIST.append({"name":name,"year":year,"metascore":metascore,"rating":rating,"votes":votes,"gross":gross})
            #print("%-50s %-15s Rating: %-5s Metascore: %-5s Votes: %-10s Gross: %-8s" % (name,year,rating,metascore, votes, gross))
        
        #X = [x["gross"] for x in MOVIES_LIST]
        #print("\n".join(X))
        display()

if __name__ == "__main__":
    main(sys.argv[1:])