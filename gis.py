#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, request
import requests
from requests.exceptions import ConnectionError

app = Flask(__name__)


@app.route('/')
def form(longitude=None, latitude=None, server=None):
    address = request.args.get("uaddress")
    print address
    if address:
        result = ask_aigeo(address) or ask_yandex(address) or {'error': u"По вашему запросу ничего не найдено"}
        return render_template("geo.html", **result)
    else:
        return render_template("geo.html")


def ask_aigeo(address):
    payload = {'search': address, 'format': 'json'}
    try:
        r = requests.get('http://api.aigeo.ru/geocoder/service?', params=payload, timeout=1)
    except ConnectionError as e:
        return None
    result_json = r.json()
    if result_json['response']['results']:
        longitude = result_json['response']['results'][0]['geoData']['longitude']
        latitude = result_json['response']['results'][0]['geoData']['latitude']
        return {'latitude': latitude, 'longitude': longitude, 'server': u"Сервер поиска: 24geo"}
    else:
        return None



def ask_yandex(address):
    payload = {'geocode': address, 'format': 'json'}
    try:
        r = requests.get('https://geocode-maps.yandex.ru/1.x/?', params=payload, timeout=1)
    except ConnectionError as e:
        return None
    result_json = r.json()
    if result_json['response']['GeoObjectCollection']['featureMember']:
        lon_lat = result_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        longitude = lon_lat.split()[0]
        latitude = lon_lat.split()[1]
        return {'latitude': latitude, 'longitude': longitude, 'server': u"Сервер поиска: yandex"}
    else:
        return None

