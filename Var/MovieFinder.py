import requests

API_KEY = '685f5f76'

def get_movie_info(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data['Response'] == 'True':
        title = data.get('Title', 'N/A')
        year = data.get('Year', 'N/A')
        imdb_rating = data.get('imdbRating', 'N/A')
        genre = data.get('Genre', 'N/A')
        plot = data.get('Plot', 'No plot available')
        director = data.get('Director', 'N/A')
        cast = data.get('Actors', 'N/A')

        print(f"\n🎬 Movie: {title} ({year})")
        print(f"IMDb Rating: {imdb_rating}⭐")
        print(f"🎮 Genre: {genre}")
        print(f"📜 Plot: {plot}")
        print(f"🎥 Director: {director}")
        print(f"🎭 Cast: {cast}")
        input("")
        main()
    else:
        input("\nSorry, the movie was not found. Please check the title and try again.\n")
        main()

def main():
    movie_name = input("Enter a movie name: ")
    get_movie_info(movie_name)

main()