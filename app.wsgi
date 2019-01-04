import os
import sys

# os.environ['FLASK_APP'] = 'app'

sys.path.insert(0, '/home/vagrant/shared/CatalogApp')

from run import app as application
