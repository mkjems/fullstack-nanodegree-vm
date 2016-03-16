from sqlalchemy import create_engine
from database_model import Base

if __name__ == '__main__':
    engine = create_engine('sqlite:////vagrant/item_catalog/item_catalog/db/restaurantmenuwithusers.db')
    Base.metadata.create_all(engine)
