import pandas as pd
from sklearn.neighbors import NearestNeighbors

data = {
    'title': ['Book1', 'Book2', 'Book3'],
    'genre': ['Fantasy', 'Science Fiction', 'Fantasy'],
    'rating': [4.7, 3.7, 4.8]
}

df = pd.DataFrame(data)
df['genre'] = df['genre'].astype('category').cat.codes

model = NearestNeighbors(n_neighbors=2, algorithm='ball_tree')
model.fit(df[['genre', 'rating']])


def recommend_books(genre, rating):
    genre_code = pd.Series([genre]).astype('category').cat.codes[0]
    distance, indices = model.kneighbors([[genre_code, rating]])
    return df.iloc[indices[0]].title.values.tolist()


