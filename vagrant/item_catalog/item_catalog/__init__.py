from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = '/vagrant/item_catalog/item_catalog/uploaded_images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Views
import item_catalog.views_restaurant
import item_catalog.views_login
import item_catalog.views_items
