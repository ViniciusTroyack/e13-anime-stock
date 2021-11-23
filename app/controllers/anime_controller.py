from app.models.anime_model import Anime
from app.exceptions.anime_erros import AnimeAlreadyExistError, animes_wrong_keys_error, AnimeNotFoundError
from flask import jsonify, request


def get_all():
    return jsonify(Anime.get_all_animes()), 200


def create():
    data = request.get_json()
    
    try:
        anime = Anime(**data)
        return jsonify(anime.create_anime()), 201
    except TypeError:
        return animes_wrong_keys_error(Anime.anime_keys, data.keys())
    except AnimeAlreadyExistError as e:
        return jsonify({"msg": e.message}), e.code
    

def filter(anime_id):
    try:
        jsonify(Anime.get_by_id(anime_id))
    except AnimeNotFoundError as e:
        return jsonify({"msg": e.message}), e.code


def delete(anime_id):
    try:
        return jsonify(Anime.delete_anime(anime_id)), 204
    except AnimeNotFoundError as e:
        return jsonify({"msg": e.message}), e.code


def update(anime_id):
    data = request.get_json()
    try:
        return jsonify(Anime.update_anime(anime_id, data))
    except AnimeNotFoundError as e:
        return jsonify({"msg": e.message}), e.code
    except:
        return animes_wrong_keys_error(Anime.anime_keys, data.keys())
