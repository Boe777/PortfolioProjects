from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from datetime import datetime
from django.utils.text import slugify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Veri setini yükle
movies_df = pd.read_csv('db/tmdb_5000_movies.csv')

# TF-IDF vectors
tfidf = TfidfVectorizer(stop_words='english')
movies_df['overview'] = movies_df['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(movies_df['overview'])

# Calculate the similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        selected_genre = request.POST.get('genre')
        selected_year = request.POST.get('year')
        min_score = float(request.POST.get('min_score', 0))
        max_score = float(request.POST.get('max_score', 10))

        filtered_df = movies_df[movies_df['genres'].str.contains(selected_genre, na=False)]

        if selected_year:
            filtered_df = filtered_df[filtered_df['release_date'].str.startswith(selected_year)]

        filtered_df = filtered_df[(filtered_df['vote_average'] >= min_score) & (filtered_df['vote_average'] <= max_score)]

        # AI
        if not filtered_df.empty:
            recommended_movie_row = filtered_df.sample(n=1)
            recommended_movie = recommended_movie_row['title'].values[0]
            release_date = datetime.strptime(recommended_movie_row['release_date'].values[0], '%Y-%m-%d').strftime('%d-%m-%Y')
            vote_average = recommended_movie_row['vote_average'].values[0]
            runtime_minutes = recommended_movie_row['runtime'].values[0]
            runtime_hours = int(runtime_minutes / 60)
            runtime_minutes = int(runtime_minutes % 60)
            runtime = f"{runtime_hours} saat {runtime_minutes} dakika"
            overview = recommended_movie_row['overview'].values[0]
            homepage = recommended_movie_row['homepage'].values[0]
            print("DEBUG - Homepage:", homepage)

            # Sugg with similarity matrix
            def get_recommendations(movie_title):
                idx = movies_df[movies_df['title'] == movie_title].index[0]
                sim_scores = list(enumerate(cosine_sim[idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[1:11]
                movie_indices = [i[0] for i in sim_scores]
                return movies_df['title'].iloc[movie_indices]

            recommendations = get_recommendations(recommended_movie)
            print("DEBUG - Recommendations:", recommendations)

            # YouTube API
            video_id = get_trailer_id(recommended_movie)

            trailer_url = f'https://www.youtube.com/embed/{video_id}' if video_id else None
        else:
            recommended_movie = "Öneri bulunamadı."
            release_date = None
            vote_average = None
            runtime = None
            overview = None
            homepage = None
            recommendations = None
            trailer_url = None

        context = {
            'recommended_movie': recommended_movie,
            'release_date': release_date,
            'vote_average': vote_average,
            'runtime': runtime,
            'overview': overview,
            'homepage': homepage,
            'recommendations': recommendations,
            'trailer_url': trailer_url  
        }

        return render(request, 'movie_recommendation/index.html', context)
    else:
        return render(request, 'movie_recommendation/index.html')


def get_trailer_id(movie_title):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=movie_title + ' trailer',
        part='id',
        maxResults=1
    ).execute()

    video_id = None
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            break

    return video_id
