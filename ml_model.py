import pandas as pd
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

        print("Data was read.")

    def extract_data(self):
        # extracting the users
        user_ratings = self.book_ratings['user'].value_counts() > 200
        y = user_ratings[user_ratings].index
        useful_ratings = self.book_ratings[self.book_ratings['user'].isin(y)]
        print(f"Data partially extracted.")
        # merge these ratings with the books
        df = useful_ratings.merge(self.book_data, on='isbn')
        # let's extract the books that has more than 50 ratings
        number_rating = df.groupby('title')['rating'].count().reset_index()
        print(f"Ratings applied..")
        # Here we have grouped the titles based on number of ratings received
        number_rating.rename(columns={'rating': 'number_of_ratings'}, inplace=True)
        # Now merge this dataframe with your originalone
        df1 = df.merge(number_rating, on='title')
        df2 = df1[df1['number_of_ratings']>=30]
        df2.drop_duplicates(['user', 'title'], inplace=True)
        print(f"Data fully extracted.")
        self.clean_data = df2

    def build_model(self):
        # create a pivot table
        self.pivot_table = self.clean_data.pivot_table(columns='user', index='title', values='rating')
        self.pivot_table.fillna(0, inplace=True)
        sparse_matrix = csr_matrix(self.pivot_table)
        # feed this matrix to our model
        self.model = NearestNeighbors(algorithm='brute')
        self.model.fit(sparse_matrix)

    def get_recommendations(self, book_name):
        try:
            close_match = difflib.get_close_matches(book_name, self.pivot_table.index.to_list())[0]
        except IndexError:
            return 'Book is not available'
        idx = np.where(self.pivot_table.index == close_match)[0][0]
        ls = [close_match]
        distances, neighbours = self.model.kneighbors(self.pivot_table.iloc[idx, :].values.reshape(1, -1), n_neighbors=6)
        neighbours = list(neighbours[0])
        for i in range(len(neighbours)):
            if i != 0:
                ls.append([self.pivot_table.index[neighbours[i]], distances[0][i]])
        return ls


def main():
    m = Book_Suggestions()
    m.read_data()
    m.extract_data()
    m.build_model()

    book_name = None
    while book_name != 'exit':
        book_name = input('Enter your favourite book name: ')
        print()
        print(m.get_recommendations(book_name))


main()