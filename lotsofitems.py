from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import Base, User, Category, Items

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Rob Baristee",
              email="tinyTim@udaci-tea.com",
              picture='http://loremflickr.com/400/400/dog')
session.add(User1)
session.commit()

# Create a test category
category1 = Category(name="Burgers")

session.add(category1)
session.commit()

time1 = datetime.datetime.now()
Item1 = Items(user_id=1,
              category_id=1,
              name="Double Double AS",
              date=time1,
              description="Juicy grilled double beef patty, specially prepared",
              picture="http://loremflickr.com/200/200/burger?random=1",
              category=category1)

session.add(Item1)
session.commit()

time2 = datetime.datetime.now()
Item2 = Items(user_id=1,
              category_id=1,
              name="Star McWhopper",
              date=time2,
              description="Charbroiled and very tasty. Known to be messy",
              picture="http://loremflickr.com/200/200/burger?random=2",
              category=category1)

session.add(Item2)
session.commit()

category2 = Category(name="Fries")

session.add(category2)
session.commit()

time3 = datetime.datetime.now()
Item3 = Items(user_id=1,
              category_id=2,
              name="Chips",
              date=time3,
              description="A british interpretation of a classic diner item",
              picture="http://loremflickr.com/200/200/fries?random=1",
              category=category2)

session.add(Item3)
session.commit()

time4 = datetime.datetime.now()
Item4 = Items(user_id=1,
              category_id=2,
              name="Waffle",
              date=time4,
              description="Almost better than curly fries",
              picture="http://loremflickr.com/200/200/fries?random=2",
              category=category2)

session.add(Item4)
session.commit()

category3 = Category(name="Milk Shakes")

session.add(category3)
session.commit()