from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Base(object):
    session = None

    def __init__(self, session=None, **data):
        for key, value in data.iteritems():
            setattr(self, key, value)
