from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


from .employee import Employee  # noqa: E402, F401
