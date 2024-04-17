#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns a JSON string"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats_class_count():
    """Retrieves the number of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    dic = {}
    for i in range(len(classes)):
        dic[names[i]] = storage.count(classes[i])
    return jsonify(dic)
