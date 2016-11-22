import cherrypy
import cherrypy as http
import uuid
import json
import random
import string
from jinja2 import Environment, FileSystemLoader
from create_database import Base,Person, Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("mysql://gpscontrol:qazwsxedc@127.0.0.1/test")
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
env = Environment(loader=FileSystemLoader('templates'))

class Root(object):

    @cherrypy.expose
    def index(self):
        tmpl=env.get_template('basicform.html')
        return(tmpl.render())
    index.exposed = True

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))

class Rest:
    # Read
    exposed = True
    def GET(self, id=None):
        list=[]
        if id is None:
            allpersons=session.query(Person).all()
            for item in allpersons:
                search_results=session.query(Address).filter_by(person_id=item.id).first()
                list.append({'id':item.id,'name':item.name,'street':search_results.street_name,'street_number':search_results.street_number})
        else:
            search_results=session.query(Person).filter_by(id=id).first()
            if search_results is not None:
                list.append({'id':search_results.id,'name':search_results.name})
        return json.dumps(list)

    # Create
    def POST(self, person_name, street_name,street_no,zip):
        # Insert a Person in the person table
        # 127.0.0.1:8080/api/v1/persons?person_name=Jorge&street_name=Manuel Lopez Aguado&street_no=91&zip=54050
        new_person = Person(name=person_name)
        session.add(new_person)
        session.commit()
        # Insert an Address in the address table
        new_address = Address(street_name=street_name,street_number=street_no,post_code=zip, person=new_person)
        session.add(new_address)
        session.commit()
        return ('Person created with  ID: %s' % new_person.id)

    # Update
    def PUT(self, id, street_name,street_no,zip):
        # Update Person in person table
        # 127.0.0.1:8080/api/v1/persons?id=8&street_name=El palomar2&street_no=122&zip=54050
        search_results=session.query(Person).filter_by(id=id).first()
        if search_results is not None:
            address = session.query(Address).filter(Address.person == search_results).one()
            if address is not None:
                address.street_name=street_name
                address.street_number=street_no
                address.post_code=zip
                session.commit()
            return ('Person updated with  ID: %s' % id)

    def DELETE(self, id):
        # Delete Person in table
        # 127.0.0.1:8080/api/v1/persons?id=8
        search_results=session.query(Person).filter_by(id=id).first()
        if search_results is not None:
            address = session.query(Address).filter(Address.person == search_results).one()
            if address is not None:
                session.delete(address)
                session.commit()
            session.delete(search_results)
            session.commit()
            return('Person deleted')

if __name__ == '__main__':
    # http://127.0.0.1:8080/api/v1/persons
    cherrypy.config.update({
    'global': {
        'environment': 'test_suite',
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
    }
    })
    cherrypy.tree.mount(
        Rest(), '/api/v1/persons',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
         }
    )
    cherrypy.tree.mount(Root())
    cherrypy.engine.start()
    cherrypy.engine.block()