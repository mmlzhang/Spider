
import random

from flask import Blueprint, render_template, request, redirect, jsonify

from main.settings import MONGO_DB


rrc_blueprint = Blueprint('rrc', __name__)


@rrc_blueprint.route('/', methods=['GET'])
def index():
    """首页"""
    if request.method == 'GET':
        return render_template('renrenche/index.html')


@rrc_blueprint.route('/cars_info/', methods=['GET'])
def cars_info():
    """返回首页车辆数据"""
    if request.method == 'GET':
        collection = MONGO_DB.renrenche.rrc_data
        cars = collection.find({"city_name_en":"cd"}, {'_id': 0}).limit(20)
        cars = [car for car in cars]
        cars = random.sample(cars, 3)
        cars = [dict(car) for car in cars]
        return jsonify(code=200, cars=cars)
