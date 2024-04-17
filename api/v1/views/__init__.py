#!/usr/bin/python3
"""Initialises views package"""

from api.v1.views.index import *
from .states import *
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
