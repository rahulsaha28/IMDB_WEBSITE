# -------------------------------------- importing all library--------------------------------
from IMDB import Imdb

# ------------------------------------------------------------------------------------------


imdb = Imdb('https://www.imdb.com/')

imdb.find_each_top_rated_movie_detail()

imdb.save_file_as_csv()


