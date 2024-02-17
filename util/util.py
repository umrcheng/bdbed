import hashlib
import time
import os

from config import config


def concatenated_file_name(path, name):
    
    return os.path.join(path, name)


def get_random_md5(filename="") -> str:
    
    t = str(time.time()) + filename
    return hashlib.md5(t.encode()).hexdigest()


def replenishment_date(date: str) -> str:
    
    if len(date) == 1:
        return "0" + date
    else:
        return date


def get_same_day_dir():
    
    t = time.gmtime()
    year = str(t.tm_year.real)
    month = replenishment_date(str(t.tm_mon))
    day = replenishment_date(str(t.tm_mday))
    path = os.path.join(".", "upload", year, month, day)
    return path


def mkdir_same_day_dir():
    
    path = get_same_day_dir()
    if not os.path.exists(path):
        os.makedirs(path)
    return True


def is_login(session):
    
    admin = session.get("admin")
    if admin == config["admin"]:
        return True
    return False


def del_photo_file(p, f):
    os.remove(os.path.join(p, f))
    return True
