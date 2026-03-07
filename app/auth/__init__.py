
from flask import Blueprint

authBP = Blueprint('auth', __name__)

from . import auth_routes