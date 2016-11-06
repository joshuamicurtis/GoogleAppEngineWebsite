from google.appengine.ext import ndb

class Message(ndb.Model):
    channel = ndb.StringProperty(required=True)
    date_time = ndb.DateTimeProperty(required=True)
    count = ndb.IntegerProperty(required=True)
    
class List(ndb.Model):
    name = ndb.StringProperty(required=True)
    categories = ndb.KeyProperty(repeated=True)
    email = ndb.StringProperty(required=True)
    disEmail = ndb.StringProperty(required=True)
    active = ndb.BooleanProperty(required=True)
    one = ndb.StringProperty(required=True)
    two = ndb.StringProperty(required=True)
    three = ndb.StringProperty(required=True)
    four = ndb.StringProperty(required=True)
    five = ndb.StringProperty(required=True)

class listCategory(ndb.Model):
    name = ndb.StringProperty(required=True)
    active = ndb.BooleanProperty(required=True)
    
class users(ndb.Model):
    email = ndb.StringProperty(required=True)
    disEmail = ndb.StringProperty(required=True)