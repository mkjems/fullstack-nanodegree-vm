import random
import string

from flask import Flask
from flask import session as login_session


app = Flask(__name__)

UPLOAD_FOLDER = '/vagrant/item_catalog/item_catalog/uploaded_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Function to generate the secret token
def generate_csrf_token():
    if '_csrf_token' not in login_session:
        login_session['_csrf_token'] = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for x in xrange(16)
        )
    return login_session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


# Views
import item_catalog.views_restaurant
import item_catalog.views_login
import item_catalog.views_items
