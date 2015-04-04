from __future__ import print_function
from flask import Flask, render_template, request
import locale
import pickle
import test

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())

app = Flask(__name__)


def make_link_profile_map_dict(profile_pickle):
    with open(profile_pickle, 'rb') as file:
        profiles = pickle.load(file)
    return test.make_link_profile_map_dict(profiles)


link_profile_map = make_link_profile_map_dict('profiles.pkl')


@app.route('/')
def search():
    return render_template('search.jinja')


@app.route('/results')
def results():
    link = request.args['profile_url']
    query = request.args['query']
    search.find_match_bfs(start_link=link,
                          query=query,
                          link_profile_map=link_profile_map)
    return render_template('results.jinja')


if __name__ == '__main__':
    app.run(debug=True)
