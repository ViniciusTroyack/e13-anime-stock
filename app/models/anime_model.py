from . import conn_cur, commit_and_close
import psycopg2
from psycopg2 import sql
from app.exceptions.anime_erros import AnimeAlreadyExistError, AnimeNotFoundError


class Anime():
    anime_keys = ["id", "anime", "released_date", "seasons"]

    def __init__(self, anime, released_date, seasons) -> None:
        self.anime = anime.title()
        self.released_date = released_date
        self.seasons = seasons


    @staticmethod
    def create_table_if_not_exists():
        
        conn, cur = conn_cur()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS animes(
            id BIGSERIAL PRIMARY KEY,
            anime VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT null,
            seasons INTEGER NOT NULL
            );
            """
        )

        commit_and_close(conn, cur)

        return 'created'


    @staticmethod
    def get_all_animes():
        Anime.create_table_if_not_exists()
        conn, cur = conn_cur()

        cur.execute(
            """
            SELECT * FROM animes;
        """
        )

        animes_list = cur.fetchall()

        commit_and_close(conn, cur)

        all_animes = [dict(zip(Anime.anime_keys, anime)) for anime in animes_list]

        return all_animes


    def create_anime(self):
        Anime.create_table_if_not_exists()

        conn, cur = conn_cur()

        query = """
            INSERT INTO
                animes
            (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """
        query_values = list(self.__dict__.values())

        try:
            cur.execute(query, query_values)
        except:
            raise AnimeAlreadyExistError("Anime already exists")

        new_anime = cur.fetchone()

        commit_and_close(conn, cur)

        return dict(zip(self.anime_keys, new_anime))


    @staticmethod
    def get_by_id(id):

        conn, cur = conn_cur()


        cur.execute(
            """
            SELECT * FROM animes WHERE id=(%s);
        """,
            (id,),
        )

        anime = cur.fetchone()

        if not anime:
            raise AnimeNotFoundError(f"Anime {id} not found")

        anime_found = dict(zip(Anime.anime_keys, anime))

        commit_and_close(conn, cur)

        return anime_found

    
    @staticmethod
    def delete_anime(id):
        conn, cur = conn_cur()

        query = """
            DELETE FROM
                animes
            WHERE
                id=%s
            RETURNING *
        """

        cur.execute(query, (id,))

        deleted_anime = cur.fetchone()

        if not deleted_anime:
            raise AnimeNotFoundError(f"Anime {id} not found")

        commit_and_close(conn, cur)

        return dict(zip(Anime.anime_keys, deleted_anime))


    @staticmethod
    def update_anime(id, data):
        conn, cur = conn_cur()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = row({values})
                WHERE
                    id={id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cur.execute(query)

        updated_anime = cur.fetchone()

        if not updated_anime:
            raise AnimeNotFoundError(f"Anime {id} not found")

        commit_and_close(conn, cur)

        return dict(zip(Anime.anime_keys, updated_anime))
