from create_database import Person, Base, Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
def getdb():
    engine = create_engine("mysql://gpscontrol:qazwsxedc@127.0.0.1/test")
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session
    # Make a query to find all Persons in the database
session=getdb()

# Return the first Person from all Persons in the database
print("First Record:")
person = session.query(Person).first()
if person is not None:
    print(person.name)
    address = session.query(Address).filter(Address.person == person).one()
    if address is not None:
        print(address.street_name)
        print(address.street_number)
        print(address.post_code)

# Return all persons
print("All Persons:")
allpersons=session.query(Person).all()
if allpersons is not None:
    for item in allpersons:
        print(item.name)
        address = session.query(Address).filter(Address.person == item).one()
        if address is not None:
            print(address.street_name)
            print(address.street_number)
            print(address.post_code)

