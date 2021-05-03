#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)

quotes = {
    0: {
        "author": "Linus Torvalds",
        "quote": "Once you start thinking more about where you want to be than about making the best product, you're screwed."
    },
    1: {
        "author": "Edward Snowden",
        "quote": "Arguing that you don\'t care about privacy because you have nothing to hide is no different than saying you don\'t care about free speech because you have nothing to say."
    },
    2: {
        "author": "Terry A. Davis",
        "quote": "An idiot admires complexity, a genius admires simplicity."
    },
    3: {
        "author": "Peter Drucker",
        "quote": "The best way to predict the future is to create it."
    },
    4: {
        "author": "Linus Torvalds",
        "quote": "Those that can, do. Those that can\'t, complain.",
    },
    5: {
        "author": "Linus Torvalds",
        "quote": "Those that can, do. Those that can\'t, complain.",
    },
    6: {
        "author": "Richard Stallman",
        "quote": "Creativity can be a social contribution, but only in so so far as society is free to use the results.",
    },
    7: {
        "author": "Steve Prefontaine",
        "quote": "To give anything less than your best is to sacrifice the gift.",
    },
    8: {
        "author": "Grant Cardone",
        "quote": "Fear is an indicator of moving in the right direction."
    },
    9: {
        "author": "Casey Neistat",
        "quote": "The Grind is not Glamorous.",
    },
    10: {
        "author": "Alan Lakein",
        "quote": "Failing to plan is planning to fail."
    },
    11: {
        "author": "Chip Heath",
        "quote": "The Curse of Knowledge: when we are given knowledge, it is impossible to imagine what it's like to LACK that knowledge."
    },
    12: {
        "author": "Russian Proverb",
        "quote": "The shark that does not swims, drowns."
    },
    13: {
        "author": "Yoda",
        "quote": "Do, or do not. There is no try."
    },
    14: {
        "author": "Henry Ford",
        "quote": "Whether you think you can or think you can't you're right"
    },
}

class Quote(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(quotes), 200
        quote = quotes.get(id)

        if quote:
            return quote, 200

        return "quote not found", 404

api.add_resource(Quote, "/quotes", "/quotes/", "/quotes/<int:id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
