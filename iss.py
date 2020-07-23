#!/usr/bin/env python

__author__ = 'Keith Garcia, Co-Author: Ben McKenzie, teaching Triston Reeves later'

import requests
import turtle
import time


def get_houston_astros():
    res = requests.get('http://api.open-notify.org/astros.json')
    return res.json()


def get_coords():
    res = requests.get('http://api.open-notify.org/iss-now.json')
    return res.json()


def get_pass():
    res = requests.get('http://api.open-notify.org/iss-pass.json',
                       params={'lat': '39.7684', 'lon': '-86.1581'})
    return res.json()


def init_turtle():
    iss = turtle.Turtle()
    next_pass = get_pass()
    rise_time = time.ctime(next_pass["response"][0]["risetime"])

    display = turtle.Screen()
    display.setup(width=800, height=400, startx=0, starty=0)
    display.setworldcoordinates(-180, -90, 180, 90)
    display.bgpic('map.gif')
    display.register_shape('iss.gif')

    iss.shape("iss.gif")
    iss.pu()
    iss.goto(-86.1581, 39.7684)
    iss.dot(4, "yellow")
    iss.color('blue')
    iss.write(rise_time, align='right', font=("Courier", 14))
    return iss


def main():
    data = get_houston_astros()
    coords = get_coords()
    eastern_time = time.ctime()
    print("The {} is currently located at {}: Latitude and {}: Longitude as of {}.".format(
        data['people'][0]['craft'], coords['iss_position']['latitude'], coords['iss_position']['longitude'], eastern_time))
    print("There are {} astronauts on the {} as of today.".format(data['number'],
                                                                  data['people'][0]['craft']))
    for astro in data["people"]:
        print(f"Astronaut {astro['name']}")

    iss = init_turtle()
    while iss:
        coords = get_coords()
        lon = float(coords["iss_position"]["longitude"])
        lat = float(coords["iss_position"]["latitude"])
        heading = iss.towards(lon, lat)
        if heading > 0.0:
            iss.setheading(heading)
        iss.goto(lon, lat)
        time.sleep(16)


if __name__ == '__main__':
    main()
