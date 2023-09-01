from pony import orm
from database import db_config
from datetime import datetime


def insert_new(long_url, short_url, expiration_date):
    db_config.URL(
        long_url=long_url,
        short_url=short_url,
        creation_date=datetime.now(),
        expiration_date=expiration_date
    )
    orm.commit()