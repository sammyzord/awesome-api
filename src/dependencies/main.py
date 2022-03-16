from ..settings import Settings, HashSettings
from hashids import Hashids


def settings():
    return Settings()


def get_hashids():
    salt = HashSettings().salt
    min_length = HashSettings().min_hash_length
    hashids = Hashids(salt=salt, min_length=min_length)
    return hashids
