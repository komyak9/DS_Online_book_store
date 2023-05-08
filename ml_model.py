import pandas as pd
import warnings
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import difflib
import numpy as np

class Book_Suggestions():
    """
    Source:
    https://github.com/Saipavan790/Recommender-Systems/blob/main/iPython%20codes/Book%20Recomendation.ipynb
    """
    def __init__(self):
        self.book_data = []
        self.book_ratings = []
        self.clean_data = []
        self.pivot_table = None
        self.model = None
        warnings.filterwarnings('ignore')


    def read_data(self):
        self.book_data = pd.read_csv(r"data/BX-Books.csv", encoding="ISO-8859-1",
                                sep=";",
                                header=0,
                                names=['isbn', 'title', 'author'],  # selecting only relevent columns
                                usecols=['isbn', 'title', 'author'],
                                dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

        self.book_ratings = pd.read_csv(
                                r"data/BX-Book-Ratings.csv",
                                encoding="ISO-8859-1",
                                sep=";",
                                header=0,
                                names=['user', 'isbn', 'rating'],
                                usecols=['user', 'isbn', 'rating'],  # selecting only relevant columns
                                dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

    def extract_data(self):
        # Extract the users
        user_ratings = self.book_ratings['user'].value_counts() > 200
        y = user_ratings[user_ratings].index
        useful_ratings = self.book_ratings[self.book_ratings['user'].isin(y)]
        # Merge ratings with the books
        df = useful_ratings.merge(self.book_data, on='isbn')

        # Extract the books that have more than 10 ratings
        num_ratings = 10
        number_rating = df.groupby('title')['rating'].count().reset_index()
        # Group the titles based on number of ratings received
        number_rating.rename(columns={'rating': 'number_of_ratings'}, inplace=True)
        df1 = df.merge(number_rating, on='title')
        df2 = df1[df1['number_of_ratings'] > num_ratings]

        df2.drop_duplicates(['user', 'title'], inplace=True)
        self.clean_data = df2

    def build_model(self):
        # Create a pivot table
        self.pivot_table = self.clean_data.pivot_table(columns='user', index='title', values='rating')
        self.pivot_table.fillna(0, inplace=True)
        sparse_matrix = csr_matrix(self.pivot_table)
        # Create and train a model
        self.model = NearestNeighbors(algorithm='brute')
        self.model.fit(sparse_matrix)

    def get_recommendations(self, book_name, num_neighbors=3):
        try:
            close_match = difflib.get_close_matches(book_name, self.pivot_table.index.to_list())[0]
        except IndexError:
            return 'Book is not recognized.'
        idx = np.where(self.pivot_table.index == close_match)[0][0]
        neighbor_books_names = []
        distances, neighbours_ids = self.model.kneighbors(self.pivot_table.iloc[idx, :].values.reshape(1, -1), n_neighbors=num_neighbors+1)
        neighbours_ids = list(neighbours_ids[0])
        for i in range(len(neighbours_ids)):
            if i != 0:
                neighbor_books_names.append([self.pivot_table.index[neighbours_ids[i]], distances[0][i]][0])
        return neighbor_books_names