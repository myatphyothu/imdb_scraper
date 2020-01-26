import os,sys
import collections
from natsort import natsorted

#^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*
Movie = collections.namedtuple("Movie", ["name", "year", "rating", "votes", "gross", "metascore"])
# class Movie(object):

#     def __init__ (self, name, year, rating, votes, gross, metascore):
#         self.name = name
#         self.year = year
#         self.rating = rating
#         self.votes = votes
#         self.gross = gross
#         self.metascore = metascore

#     def __getitem__ (self, key):
#         if key == "name": return self.name
#         elif key == "year": return self.year
#         elif key == "rating": return self.rating
#         elif key == "votes": return self.votes
#         elif key == "gross": return self.gross
#         elif key == "metascore": return self.metascore
#         else: return None

#     def __str__(self):
#         dsp = "%s(%s),Rating:%s, Votes:%s, Metascore:%s, Gross:%s" % (self.name,self.year,self.rating,self.votes,self.metascore,self.gross)
#         return dsp
#^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*
class MovieCollection(object):

    def __init__ (self):
        self.master_collection = dict()

        self.attr_keys = ["rating", "votes", "metascore", "gross", "year"]
        self.__init_particular_collections(self.attr_keys)

    def __init_particular_collections(self, keys):
        self.particular_collections = dict()
        for key in keys:
            self.particular_collections[key] = dict()

    
    def __add_to_collection(self, key, movie, collection):
        attr_map = {
            "rating": movie.rating, "votes": movie.votes, 
            "metascore": movie.metascore, "gross":movie.gross, "year":movie.year
        }
        if key in collection:
            collection[attr_map[key]].append(movie.name)  
        else:
            collection[attr_map[key]] = [movie.name,]


    def add(self, movie):
        if movie is None:
            return

        self.master_collection[movie.name] = movie
        for key in self.attr_keys:
            self.__add_to_collection(key, movie, self.particular_collections[key])

    def add_list(self, movie_list):
        for movie in movie_list:
            self.add(movie)
        

    def __sorted_collection(self, key, mode="AESC"):
        if key not in self.particular_collections:    
            return None

        if mode != "AESC" and mode != "DESC":
            return None

        
        sorted_collection = dict()
        keys = self.particular_collections[key].keys()
        sorted_keys = natsorted(keys, reverse=(True if mode is "DESC" else False))
        for xkey in sorted_keys:
            sorted_collection[xkey] = self.particular_collections[key][xkey]
        return sorted_collection

    def sort(self, key=None, mode="AESC"):
        if key in self.attr_keys:
            return self.__sorted_collection(key, mode)
        else:
            return None
    
    def display(self):
        for movie in self.master_collection.values():
            print(movie)

    def display_sorted(self, key, mode="AESC"):
        sorted_collection = self.sort(key, mode)
        for key,movie_name in sorted_collection.items():
            print(key,"==>",movie_name)
    

if __name__ == "__main__":
    pass