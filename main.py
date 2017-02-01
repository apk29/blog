
import os
import jinja2
import webapp2

from google.appengine.ext import ndb

#template loading code, locations of the templates
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)


class BlogHandler(webapp2.RequestHandler):
	#code to automatically write on type self.response.out.write
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	#takes template name and dictionary of parameters to substitue into the template       
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	# render calls out wwrite and render_str to print out the template
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

	#keeps line separatated when typing in new blog with spacing  
	def render(self):
		self._render_text = self.content.replace('\n', '<br>')
		return render_str("post.html", p = self)

class MainPage(BlogHandler):
  def get(self):
      self.write('Hello, Udacity!')

###Blog Area

def blog_key(name = 'default'):
	return ndb.Key('blogs', name)


class Post(ndb.Model):
	subject = ndb.StringProperty(required = True)
	content = ndb.TextProperty(required = True)
	created = ndb.DateTimeProperty(auto_now_add = True)
	last_modified = ndb.DateTimeProperty(auto_now = True)
		
class BlogFront(BlogHandler):
	def get(self):
		posts = Post.query().order(-Post.created)
		self.render("front.html", posts = posts)

    

class PostPage(BlogHandler):
	def get(self, post_id):
		key = ndb.Key.from_path('Post', int(post_id), parent=blog_key())
		post = ndb.get(key)

		if not post:
			self.error(404)
			return

		self.render("permalink.html", post = post)

"""class MainPage(Handler):
	#prevents things that were typed into the title and art box from disappearing if there was an error
	def render_front(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art ORDER by created DESC")
		self.render("front.html", title=title, art=art, error=error, arts=arts)

	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Art(title = title, art = art)#grabs the art instead of saying thanks
			a.put()#this stores the art in the database

			self.redirect("/")
		else: #prevents things that were typed into the title and art box from disappearing if there was an error
			error = "we need both title and some artwork!"
			self.render_front(title, art, error)"""

app = webapp2.WSGIApplication([('/', MainPage),('/blog/?',BlogFront)], debug=True)		

