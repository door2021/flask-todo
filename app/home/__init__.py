
from flask import Blueprint

homeBP = Blueprint('home', __name__)

from . import home_routes