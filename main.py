import webapp2

config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
    ('list/add', 'edit_list.EditList'),
    ('/edit_list', 'admin.EditList'),
    ('/edit', 'admin.Edit'),
    ('/category/add', 'add_category.AddCategory'),
    ('/admin', 'admin.Admin'),
    ('/view', 'admin.View')
], debug=True, config=config)