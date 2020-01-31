import os,sys
import collections
from natsort import natsorted

#^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*
Movie = collections.namedtuple("Movie", ["name", "year", "rating", "votes", "gross", "metascore"])

class MovieCollection(object):

    def __init__ (self):
        self.master_collection = dict()

        self.attr_keys = ["rating", "votes", "metascore", "gross", "year"]
        self.__init_particular_collections(self.attr_keys)

    def __init_particular_collections(self, keys):
        self.particular_collections = dict()
        for key in keys:
            self.particular_collections[key] = dict()

    def populate_particular_collections(self):
        for i,movie in enumerate(self.master_collection.values()):
            for key in self.attr_keys:
                self.__add_to_collection(key, movie)

    
    def __add_to_collection(self, key, movie):
        attr_map = {
            "rating": movie.rating, "votes": movie.votes, 
            "metascore": movie.metascore, "gross":movie.gross, "year":movie.year
        }
        attr_key = attr_map[key]
        if attr_key in self.particular_collections[key].keys():
            if movie.name not in self.particular_collections[key][attr_key]:
                self.particular_collections[key][attr_key].append(movie.name)  
        else:
            self.particular_collections[key][attr_key] = [movie.name,]

    def exists(self, name):
        if name in self.master_collection.keys():
            return True
        return False

    def add(self, movie, overwrite="no"):
        if movie is None or (overwrite == "no" and self.exists(movie.name)):
            return
        
        self.master_collection[movie.name] = movie
        for key in self.attr_keys:
            self.__add_to_collection(key, movie)


    def add_list(self, movie_list):
        for movie in movie_list:
            self.add(movie)
        

    def __sorted_collection(self, key, mode="AESC", value=None):
        def interpret_value(ivalue):
            sign_list = ["greater than equal to", "less than equal to", "less than", "greater than"]
            sign, final_value = None, None
            for xsign in sign_list:
                if ivalue.startswith(xsign):
                    final_value = ivalue.split(xsign)[1].strip()
                    sign = xsign
                    break
            if sign == None:
                final_value = ivalue
            return sign, final_value
                

        if key not in self.particular_collections:    
            return None

        if mode != "AESC" and mode != "DESC":
            return None


        sorted_collection = dict()
        keys = self.particular_collections[key].keys()
        sorted_keys = natsorted(keys, reverse=(True if mode is "DESC" else False))
        sign, final_value = None, None
    
        for xkey in sorted_keys:
            if value is not None:
                sign, final_value = interpret_value(value)
                if sign is not None:
                    if sign == "greater than equal to":
                        if float(xkey) >= float(final_value):
                            
                            sorted_collection[xkey] = self.particular_collections[key][xkey]
                    elif sign == "less than equal to":
                        if float(xkey) <= float(final_value):
                            sorted_collection[xkey] = self.particular_collections[key][xkey]
                    elif sign == "less than":
                        if float(xkey) < float(final_value):
                            sorted_collection[xkey] = self.particular_collections[key][xkey]
                    elif sign == "greater than":
                        if float(xkey) > float(final_value):
                            sorted_collection[xkey] = self.particular_collections[key][xkey]
                else:

                    if xkey == value:
                        sorted_collection[xkey] = self.particular_collections[key][xkey]
            else:
                sorted_collection[xkey] = self.particular_collections[key][xkey]
        return sorted_collection

    def sort(self, key=None, mode="AESC", value=None):
        if key in self.attr_keys:
            return self.__sorted_collection(key, mode, value)
        else:
            return None
    
    def display(self):
        for movie in self.master_collection.values():
            print(movie)

    def save_to_file(self, filename):
        with open(filename, "w") as  f:
            for movie in self.master_collection.values():
                f.write(str(movie)+"\n")

    def sort_by(self, key, mode="ASEC", value=None):
        sorted_collection = self.sort(key, mode, value)
        return sorted_collection

    @staticmethod
    def display_sorted(sorted_collection,title=""):

        if sorted_collection == None or len(sorted_collection) == 0:
            print("[ERR]: empty data...")
            exit()

        
        for ikey,movie_names in sorted_collection.items():
            print(title,ikey)
            for idx,movie in enumerate(movie_names):
                print("%4d. %s" % (idx+1,movie))
            print("====================================================================================")
    
if __name__ == "__main__":
    pass