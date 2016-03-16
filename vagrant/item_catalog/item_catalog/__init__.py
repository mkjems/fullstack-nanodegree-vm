from flask import Flask

app = Flask(__name__)

# Views
import item_catalog.views_restaurant
import item_catalog.views_login
import item_catalog.views_items
