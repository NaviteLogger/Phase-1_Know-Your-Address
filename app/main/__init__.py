"""
The __init__.py file is required to treat the main directory as a Python package.
This means that the application directory can be treated as a package, and therefore
the modules cam be imported into the __init__.py file in the 'app' folder. This is done 
in the __init__.py file in the 'app' folder by the following line: 'from app.main import routes'.

Also, the '__init__.py' file in each folder will typically be used to create a
Blueprint for that particulare module. This allows us to define the routes specific
to that module in the module's __init__.py file.
"""

from flask import Blueprint

"""
This creates a Blueprint named 'main'. Like the application object, the blueprint 
needs to know where it's defined, so __name__ is passed as the second argument.
"""

main = Blueprint("main", __name__)

# Import the routes module from the 'routes.py' file located in the same directory as this __init__.py file.
from . import routes

# Import the models module from the 'models.py' file located in the same directory as this __init__.py file.
from . import models
