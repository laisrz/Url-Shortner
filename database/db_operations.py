from pony import orm
from datetime import datetime
import uuid


def insert_new(db, long_url, expiration_date):
    short_url = str(uuid.uuid4())

    db.URL(
        long_url=long_url,
        short_url=short_url,
        creation_date=datetime.now(),
        expiration_date=expiration_date
    )
    orm.commit()

    return short_url


def update(db, short_url, new_long_url, expiration_date):
    '''Update database of short url provided by the user'''
    
    db_data = db.URL.get(short_url=short_url)

    db_data.long_url = new_long_url

    db_data.expiration_date = expiration_date



def delete(db, short_url):

    db_data = db.URL.get(short_url=short_url)

    db_data.is_deleted = 1
