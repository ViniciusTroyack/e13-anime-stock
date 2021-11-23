class AnimeAlreadyExistError(Exception):
    def __init__(self, message, code=422):
        self.message = message
        self.code = code


class AnimeNotFoundError(Exception):
    def __init__(self, message, code=404):
        self.message = message
        self.code = code


def animes_wrong_keys_error(avaliable_keys, wrong_keys):
    wrong_keys = [key for key in wrong_keys if not key in avaliable_keys]
    avaliable_keys.remove('id')
    return {"avaliable_keys":avaliable_keys , "wrong_keys_sended": wrong_keys}, 422
