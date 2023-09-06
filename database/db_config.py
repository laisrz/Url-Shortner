from pony import orm
from datetime import date, datetime

# Configurating database
db = orm.Database()

class URL(db.Entity):
    _table_ = 'url'
    id = orm.PrimaryKey(int, auto=True)
    long_url = orm.Required(str)
    short_url = orm.Required(str)
    creation_date = orm.Required(datetime)
    expiration_date = orm.Optional(date)
    number_visits = orm.Optional(int)
    is_deleted = orm.Required(bool, default=0)

db.bind(
    provider='mysql',
    host='localhost',
    user='root',
    passwd='',
    db='urlshortener'
)

# Mapping entities to database tables
db.generate_mapping(create_tables=True)

orm.set_sql_debug(True)