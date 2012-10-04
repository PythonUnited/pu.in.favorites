class FakeRequest(object):

   def __init__(self, get=None, post=None, user=None):
       self.get = get
       self.post = post
       self.user = user

       self.FILES = None

   @property
   def GET(self):
       return self.get

   @property
   def POST(self):
       return self.post

   @property
   def method(self):

       return (self.post is not None) and "POST" or "GET"


def initFormView(view, get=None, post=None):

    view.request = FakeRequest(get=get, post=post)
    
    view.form = view.get_form(view.form_class)

    view.form.full_clean()
