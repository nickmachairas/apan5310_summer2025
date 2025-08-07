
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import relationship, declarative_base



from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


stmt = """
    CREATE TABLE customers (
        customer_id   integer,
        first_name    varchar(50) NOT NULL,
        last_name     varchar(50) NOT NULL,
        email         varchar(50) NOT NULL,
        cell_phone    varchar(20),
        PRIMARY KEY (customer_id)
    );
    
    CREATE TABLE movies (
        movie_id      integer,
        movie_title   varchar(100) NOT NULL,
        PRIMARY KEY (movie_id)
    );
    
    CREATE TABLE genres (
        genre_id      integer,
        genre         varchar(20) NOT NULL,
        PRIMARY KEY (genre_id)
    );
    
    CREATE TABLE movie_genres (
        movie_id      integer,
        genre_id      integer,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
    );
    
    CREATE TABLE orders (
        customer_id   integer,
        movie_id      integer,
        movie_price   numeric(5,2) NOT NULL,
        purchase_datetime  timestamp NOT NULL,
        PRIMARY KEY (customer_id, movie_id),
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
    );
"""


Base = declarative_base()

class Customer(Base):
    """
        CREATE TABLE customers (
        customer_id   integer,
        first_name    varchar(50) NOT NULL,
        last_name     varchar(50) NOT NULL,
        email         varchar(50) NOT NULL,
        cell_phone    varchar(20),
        PRIMARY KEY (customer_id)
    );
    """
    
    __tablename__ = "customer"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    cell_phone: Mapped[str] = mapped_column(String(20), nullable=True)


class Genres(Base):
    """
        CREATE TABLE genres (
        genre_id      integer,
        genre         varchar(20) NOT NULL,
        PRIMARY KEY (genre_id)
    );
    """
    
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(String(20), nullable=False)
    movies: Mapped[List["Movies"]] = relationship(secondary="movie_genres", back_populates="genres")


class Movies(Base):
    """
        CREATE TABLE movies (
        movie_id      integer,
        movie_title   varchar(100) NOT NULL,
        PRIMARY KEY (movie_id)
    );
    """
    
    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    movie_title: Mapped[str] = mapped_column(String(100), nullable=False)
    genres: Mapped[List[Genres]] = relationship(secondary="movie_genres", back_populates="movies")
    
class MovieGenres(Base):
    """
        CREATE TABLE movie_genres (
        movie_id      integer,
        genre_id      integer,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies (movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
    );
    """
    
    __tablename__ = "movie_genres"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(primary_key=True)
    movie: Mapped[Movies] = relationship("Movies", back_populates="genres")
    genre: Mapped[Genres] = relationship("Genres", back_populates="movies")


drama = Genres(genre="Drama")

drama.movies
