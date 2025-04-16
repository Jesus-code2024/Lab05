import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import (
    Director, Actor, Genre, Movie, MovieActor, UserProfile, Rating
)


class Command(BaseCommand):
    """Command to seed the database with sample data"""
    help = 'Seeds the database with sample data for testing and development'
    
    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Rating.objects.all().delete()
        MovieActor.objects.all().delete()
        Movie.objects.all().delete()
        Director.objects.all().delete()
        Actor.objects.all().delete()
        Genre.objects.all().delete()
        
        # Create sample directors
        self.stdout.write('Creating directors...')
        directors_data = [
            {'name': "Christopher Nolan", 'birth_date': date(1970, 7, 30), 'biography': "British-American filmmaker known for his cerebral, often nonlinear, storytelling."},
            {'name': "Steven Spielberg", 'birth_date': date(1946, 12, 18), 'biography': "American filmmaker, considered one of the founding pioneers of the New Hollywood era."},
            {'name': "Greta Gerwig", 'birth_date': date(1983, 8, 4), 'biography': "American actress and filmmaker known for her roles in mumblecore films."},
            {'name': "Denis Villeneuve", 'birth_date': date(1967, 10, 3), 'biography': "Canadian filmmaker known for his atmospheric, visually striking films."},
        ]
        for data in directors_data:
            Director.objects.create(**data)
        
        # Create sample actors
        self.stdout.write('Creating actors...')
        actors_data = [
            {'name': "Leonardo DiCaprio", 'birth_date': date(1974, 11, 11), 'biography': "American actor known for his intense, unconventional roles."},
            {'name': "Meryl Streep", 'birth_date': date(1949, 6, 22), 'biography': "American actress often described as the 'best actress of her generation'."},
            {'name': "Tom Hanks", 'birth_date': date(1956, 7, 9), 'biography': "American actor and filmmaker, known for both comedic and dramatic roles."},
            {'name': "Viola Davis", 'birth_date': date(1965, 8, 11), 'biography': "American actress and producer, known for her powerful performances."},
            {'name': "Timothée Chalamet", 'birth_date': date(1995, 12, 27), 'biography': "American actor known for his roles in independent films."},
            {'name': "Saoirse Ronan", 'birth_date': date(1994, 4, 12), 'biography': "Irish and American actress known for her roles in period dramas."},
        ]
        for data in actors_data:
            Actor.objects.create(**data)
        
        # Create sample genres
        self.stdout.write('Creating genres...')
        genres_data = [
            {"name": "Action", "description": "Action films emphasize spectacular physical action."},
            {"name": "Comedy", "description": "Comedy films are designed to provoke laughter."},
            {"name": "Drama", "description": "Drama films are serious in tone, focusing on personal development."},
            {"name": "Science Fiction", "description": "Science fiction films deal with imaginative and futuristic concepts."},
            {"name": "Horror", "description": "Horror films seek to elicit fear or disgust from the audience."},
            {"name": "Romance", "description": "Romance films focus on love and romantic relationships."},
            {"name": "Thriller", "description": "Thriller films maintain high levels of suspense and excitement."},
        ]

        # Avoid duplicates by checking if the genre already exists
        for genre_data in genres_data:
            Genre.objects.get_or_create(name=genre_data["name"], defaults=genre_data)
        
        # Get all created objects
        directors = list(Director.objects.all())
        actors = list(Actor.objects.all())
        genres = list(Genre.objects.all())
        
        # Create sample movies
        self.stdout.write('Creating movies...')
        movies_data = [
            {'title': "Inception", 'release_date': date(2010, 7, 16), 'plot': "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into someone's mind.", 'runtime': 148, 'director': directors[0]},
            {'title': "Jurassic Park", 'release_date': date(1993, 6, 11), 'plot': "A pragmatic paleontologist visiting a theme park is amazed when its cloned dinosaurs are created, but things soon turn dangerous when they escape.", 'runtime': 127, 'director': directors[1]},
            {'title': "Little Women", 'release_date': date(2019, 12, 25), 'plot': "The lives of the March sisters as they navigate love, loss, and the pressures of growing up in 19th-century Massachusetts.", 'runtime': 135, 'director': directors[2]},
            {'title': "Dune", 'release_date': date(2021, 10, 22), 'plot': "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.", 'runtime': 155, 'director': directors[3]},
            {'title': "Interstellar", 'release_date': date(2014, 11, 7), 'plot': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", 'runtime': 169, 'director': directors[0]},
        ]
        movies = []
        for data in movies_data:
            movie = Movie.objects.create(**{k: v for k, v in data.items() if k != 'genres'})
            movies.append(movie)
        
        # Assign genres to movies
        self.stdout.write('Assigning genres...')
        genre_map = {
            "Inception": [genres[3], genres[6]],  # Sci-Fi, Thriller
            "Jurassic Park": [genres[0], genres[3]],  # Action, Sci-Fi
            "Little Women": [genres[2], genres[5]],  # Drama, Romance
            "Dune": [genres[0], genres[3]],
            "Interstellar": [genres[2], genres[3]],
        }
        for movie in movies:
            movie.genres.set(genre_map.get(movie.title, []))
        
        # Create MovieActor relationships
        self.stdout.write('Creating movie-actor relationships...')
        movie_actors = [
            {'movie': movies[0], 'actor': actors[0], 'character_name': "Dom Cobb", 'is_lead': True},
            {'movie': movies[1], 'actor': actors[2], 'character_name': "Dr. Alan Grant", 'is_lead': True},
            {'movie': movies[2], 'actor': actors[5], 'character_name': "Jo March", 'is_lead': True},
            {'movie': movies[2], 'actor': actors[4], 'character_name': "Laurie", 'is_lead': False},
            {'movie': movies[3], 'actor': actors[4], 'character_name': "Paul Atreides", 'is_lead': True},
            {'movie': movies[4], 'actor': actors[0], 'character_name': "Cooper", 'is_lead': True},
        ]
        for ma in movie_actors:
            MovieActor.objects.create(**ma)
        
        # Create users and profiles
        self.stdout.write('Creating users...')
        users = []
        for i in range(1, 6):
            username = f"user{i}"
            user = User.objects.create_user(username=username, email=f"{username}@example.com", password="password123")
            users.append(user)
            profile = UserProfile.objects.create(user=user, bio=f"Bio for {username}")
            profile.favorite_genres.set(random.sample(genres, 2))
        
        # Create ratings
        self.stdout.write('Creating ratings...')
        for user in users:
            for movie in random.sample(movies, random.randint(2, 4)):
                Rating.objects.create(user=user, movie=movie, value=random.randint(1, 10), comment=f"Rating comment from {user.username} for {movie.title}")
        
        # Update average ratings
        for movie in Movie.objects.all():
            movie.update_avg_rating()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
