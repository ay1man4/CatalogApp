import os
import sys

# os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_APP'] = 'production'

# sys.path.insert(0, '/home/vagrant/shared/CatalogApp')
sys.path.insert(0, '/home/ayman/projects/CatalogApp')

from run import app as application
