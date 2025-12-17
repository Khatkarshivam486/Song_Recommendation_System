from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import difflib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

Songs_data = pd.read_csv("spotify_millsongdata (1).csv")

selected_features = ["artist", "song", "link", "text"]

for feature in selected_features :
  Songs_data[feature] = Songs_data[feature].fillna("")

combined_features = Songs_data['artist']+' '+ Songs_data['song']+' '+ Songs_data['link']+' '+ Songs_data['text']

vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vectors)

list_of_all_titles = Songs_data['song'].to_list()

class SongRequest(BaseModel):
    Song: str

@app.get("/")
def root():
    return {"message": "Song Recommendation API"}

@app.post("/recommendation")
def recommend(request: SongRequest):
    Song_name = request.Song
    find_close_match = difflib.get_close_matches(Song_name, list_of_all_titles)
    close_match = find_close_match[0]

    index_of_the_Song = Songs_data[Songs_data['song'] == close_match].index[0]

    similarity_score = list(enumerate(similarity[index_of_the_Song]))

    sorted_similar_Song = sorted(similarity_score, key = lambda x:x[1], reverse = True)

    recommendations = []

    for i, Song in enumerate(sorted_similar_Song[1:30]):
        index = Song[0]
        title_from_index = Songs_data.iloc[index]['song']
        recommendations.append(title_from_index)

    return {
        "matched_song": close_match,
        "recommendations": recommendations
    }