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
input=raw_input("Delete all Records or the First (A/F): ")
if input=="F":
    # Return the first Person from all Persons in the database
    person = session.query(Person).first()
    if person is not None:
        print("The person {} was deleted".format(person.name))
        address = session.query(Address).filter(Address.person == person).one()
        if address is not None:
            session.delete(address)
            session.commit()
        session.delete(person)
        session.commit()
else:
    allpersons=session.query(Person).all()
    if allpersons is not None:
        for item in allpersons:
            print("The person {} was deleted".format(item.name))
            address = session.query(Address).filter(Address.person == item).one()
            if address is not None:
                session.delete(address)
                session.commit()
            if item is not None:
                session.delete(item)
                session.commit()
