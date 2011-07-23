from pymongo import Connection

from pms.config import config

def get_connection():
    return Connection(config['mongodb']['host'])
