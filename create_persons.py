from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_database import Address, Base, Person

engine = create_engine("mysql://gpscontrol:qazwsxedc@127.0.0.1/test")
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

person_name=raw_input("Name:")
street_name=raw_input("Street Name:")
street_no=raw_input("Street Number:")
zip=input("ZIP:")
# Insert a Person in the person table
new_person = Person(name=person_name)
session.add(new_person)
session.commit()

# Insert an Address in the address table
new_address = Address(street_name=street_name,street_number=street_no,post_code=zip, person=new_person)
session.add(new_address)
session.commit()