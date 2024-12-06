from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import json


engine = create_engine(
    "mysql+mysqldb://root:2706@localhost/hbnb_dev_db", pool_pre_ping=True)

Session = sessionmaker(bind=engine)
session = Session()

place = storage.get(Place, '09b4888f-0e06-4ab1-abbc-05e9865634d0')
print(place.name)
for review in place.reviews:
    print(review.text)
    print()




session.close()
