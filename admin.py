import webapp2
import base_page
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
import db_defs

class Admin(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}
        
    def render(self, page):
        self.template_values['categories'] = [{'name':x.name, 'key':x.key.urlsafe()} for x in db_defs.listCategory.query(ancestor=ndb.Key(db_defs.listCategory, self.app.config.get('default-group'))).fetch()]
        self.template_values['lists'] = [{'name':x.name, 'key':x.key.urlsafe()} for x in db_defs.List.query(ancestor=ndb.Key(db_defs.List, self.app.config.get('default-group'))).fetch()]
        base_page.BaseHandler.render(self, page, self.template_values)
        
    def get(self):
        self.render('top5.html')
    
    def post(self):
        action = self.request.get('action')
        if action == 'new_category':
            k = ndb.Key(db_defs.listCategory, self.app.config.get('default-group'))
            cat = db_defs.listCategory(parent=k)
            cat.name = self.request.get('category-name')
            cat.active = True
            cat.put()
            self.template_values['message'] = 'Added category ' + cat.name + ' to the database.'
        elif action == 'new_list':
            k = ndb.Key(db_defs.List, self.app.config.get('default-group'))
            lis = db_defs.List(parent=k)
            lis.name = self.request.get('list-name')
            lis.categories = [ndb.Key(urlsafe=x) for x in self.request.get_all('categories[]')]
            lis.email = self.request.get('email')
            lis.disEmail = self.request.get('disEmail')
            lis.one = self.request.get('one')
            lis.two = self.request.get('two')
            lis.three = self.request.get('three')
            lis.four = self.request.get('four')
            lis.five = self.request.get('five')
            lis.active = True
            lis.put()
            self.template_values['message'] = lis.email + ' added list ' + lis.name + ' to the database. '
            if lis.disEmail == 'yes':
                self.template_values['message2'] = lis.email + ' will be displayed with list ' + lis.name + ' on view page.'
        else:
            self.render('top5.html', {'message':'Action ' + action + ' is unknown.'})
        self.render('top5.html')

class View(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}
    
    def render(self, page):
        self.template_values['lists'] = [{'name':x.name, 'one':x.one, 'two':x.two, 'three':x.three, 'four':x.four, 'five':x.five, 'email':x.email,
        'disEmail':x.disEmail, 'key':x.key.urlsafe()} for x in db_defs.List.query(ancestor=ndb.Key(db_defs.List, self.app.config.get('default-group'))).fetch()]
        base_page.BaseHandler.render(self, page, self.template_values)
        
    def get(self):
        self.render('viewTop5.html')
        
class Edit(base_page.BaseHandler):
    list_key = ndb.Key
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_values = {}
    
    def get(self):
        if self.request.get('type') == 'lists':
            list_key = ndb.Key(urlsafe=self.request.get('key'))
            list = list_key.get()
            self.template_values['list'] = list
            categories = db_defs.listCategory.query(ancestor=ndb.Key(db_defs.listCategory, self.app.config.get('default-group')))
            class_boxes = []
            for c in categories:
                if c.key in list.categories:
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
                else:
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
            self.template_values['categories'] = class_boxes
            self.template_values['edit_url'] = '/edit?key=' +  list_key.urlsafe() + '&type=edLists'
            if list.disEmail == "yes":
                self.template_values['yes'] = 'checked'
            else:
                self.template_values['no'] = 'checked'
        if self.request.get('type') == 'edLists':
            list_key = ndb.Key(urlsafe=self.request.get('key'))
            list = list_key.get()
            self.template_values['list'] = list
            categories = db_defs.listCategory.query(ancestor=ndb.Key(db_defs.listCategory, self.app.config.get('default-group')))
            class_boxes = []
            for c in categories:
                if c.key in list.categories:
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
                else:
                    class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
            self.template_values['categories'] = class_boxes
            if list.disEmail == "yes":
                self.template_values['yes'] = 'checked'
            else:
                self.template_values['no'] = 'checked'
            self.template_values['message'] = list.name + ' updated. '
        self.render('editList.html',self.template_values)
     
    def post(self):
        list_key = ndb.Key(urlsafe=self.request.get('key'))
        list = list_key.get()
        #action = self.request.get('action')
        #if action == 'edit_list':
        #k = ndb.Key(db_defs.List, self.app.config.get('default-group'))
        #list = db_defs.List(parent=k)
        list.name = self.request.get('list-name')
        list.categories = [ndb.Key(urlsafe=x) for x in self.request.get_all('categories[]')]
        list.email = self.request.get('email')
        list.disEmail = self.request.get('disEmail')
        list.one = self.request.get('one')
        list.two = self.request.get('two')
        list.three = self.request.get('three')
        list.four = self.request.get('four')
        list.five = self.request.get('five')
        list.active = True
        list.put()
        #self.template_values['message'] = list.email + ' edited ' + list.name
        self.redirect('/edit?key=' + list.key.urlsafe() + '&type=edLists')
            