import sys, os, bottle
# Change working directory so relative paths (and template lookup) work again
sys.path = ['/var/www/photo-hack/'] + sys.path
os.chdir(os.path.dirname(__file__))

# This loads the application
import photo_hack

# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi
application = bottle.default_app()
