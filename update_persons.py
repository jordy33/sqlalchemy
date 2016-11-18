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
person2search=raw_input("Name? ")
search_results=session.query(Person).filter_by(name=person2search).first()
if search_results is not None:
    address = session.query(Address).filter(Address.person == search_results).one()
    if address is not None:
        print("Street: {}".format(address.street_name))
        print("Number: {}".format(address.street_number))
        print("ZIP: {}".format(address.post_code))
        new_street=raw_input("Street:")
        new_number=raw_input("Number:")
        new_zip=raw_input("Zip:")
        address.street_name=new_street
        address.street_number=new_number
        address.post_code=new_zip
        session.commit()




