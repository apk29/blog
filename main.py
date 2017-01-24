#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import re
from string import letters
import jinja2
import webapp2

from google.appengine.ext import db
#template loading code, locations of the templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class BaseHandler(webapp2.RequestHandler):
    #code to automatically write on type self.response.out.write
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    #takes template name and dictionary of parameters to substitue into the template       
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    # render calls out wwrite and render_str to print out the template
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

########### blog area
#data store in google, assigns a key to BlogPost
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

#list of blog entry properties
class Post(db.Model):
    subject = db.StringProperty(required = True)#less than 500 character
    content = db.TextProperty(required = True)#greater than 500 character and have new lines
    created = db.DateTimeProperty(auto_now_add = True)#makes the current time when an object is created
    last_modified = db.DateTimeProperty(auto_now = True)#every the blog is updated time is set to the current time 
    author = ndb.StructuredProperty(User)
    likes = ndb.IntegerProperty(default = 0)

    #keeps line separatated when typing in new blog with spacing  
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

#limits blog to 10 entries
class BlogFront(BlogHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('front.html', posts = posts)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post = post)

class NewPost(BlogHandler):
    def get(self):
        self.render("newp_ost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/unit2/rot13', Rot13),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ],
                              debug=True)

