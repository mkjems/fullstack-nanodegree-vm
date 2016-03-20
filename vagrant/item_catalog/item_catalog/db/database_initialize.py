from sqlalchemy import create_engine
from item_catalog.db.database_model import Base

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurantmenuwithusers.db')
    Base.metadata.create_all(engine)
