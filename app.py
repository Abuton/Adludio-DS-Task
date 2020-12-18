import sys
import json
import numpy as np

from flask import Flask, request, jsonify, make_response
# from flask import session
from flask import render_template, send_from_directory
from flask_cors import CORS


import lib.recommender_tools as rec_tools
from lib.recommender_data import RECCOMEND_DATA
from lib.tools import json_response, load_input
import lib.look_up_table  as look_up_table

VERBOSE = True

REC_DATA = RECCOMEND_DATA()

app = Flask(__name__, static_url_path='')

CORS(app)
# set this bugger by default.
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/js/<path:path>')
def send_js(path):
    # offer up the js and css files for consumption
    return send_from_directory('templates/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    # offer up the css files for consumption
    return send_from_directory('templates/css', path)


@app.route('/images/<path:path>')
def send_image(path):
    # offer up the images for consumption
    return send_from_directory('templates/images', path)


@app.route('/', methods=['POST', 'GET'])
def page_test():
    """ Sanity check for flask application (used in automated tests)

    """
    # get user-name and access rights from IAM

    html = "<h3>Hello world! 3</h3>"
    return html


@app.route('/demo1', methods=['POST', 'GET'])
def initial_form():
    """ Sanity check for flask application (used in automated tests)
    """
    return render_template('demo_page.html')

@app.route('/example_form_interface', methods=['GET'])
def basic_demo2():
    """
    Displays basic_form_and_results page if route /example_form_interface 
    is specified
    Args:
        no args
    Returns:
        html page
    Raises:
        not handled
    """
    return render_template('basic_form_and_results.html')


@app.route('/list_searchable_parameters', methods=['GET'])
def list_searchable_parameters():
    """ returns a plain text of charset='utf-8'
        with inputs and target as a key:value pair
    """
    # output 'here' with the help of file=sys.stdout
    print('here', file=sys.stdout)
    # saved all searchable parameters into inputs in a key : value format (json)
    inputs = REC_DATA.list_input_keys_values()
    # output 'inputs' with the aid of file=sys.stdout
    print('inputs',inputs, file=sys.stdout)
    # save a portion of the searchable parameter by specifying the key name 'campaign_objective'
    targets = look_up_table.LOOK_UP_TABLE['campaign_objective']
    print('targets', targets, file=sys.stdout)
    # return a text file with inputs as key to searchable parameters and targets key to targets
    return json_response({"inputs": inputs, "targets": targets})


@app.route('/recommend_sort_games', methods=['POST'])
def make_recommendation():
    """Based on the user's objective, this function selects matches and returns scores and meta data
    """
    event_rates = ['click-through-event', 'first_dropped', 'impression']

    # Load the input
    json_dict = load_input(request)
    #json_dict = ast.literal_eval(json_str)
    if VERBOSE:
        print('json_dict', json_dict, file=sys.stdout)

    # beware campaign_objective also sent in
    slice_parameters = json_dict #[{i: json_dict[i]} for i in json_dict if i != 'campaign_objective']


    # set default objects if none given
    objectives = json_dict.get('campaign_objective', look_up_table.LOOK_UP_TABLE['campaign_objective'])

    if isinstance(objectives, list) is False:
        objectives = [objectives]
    print('objectives', objectives, file=sys.stdout)
    # assure the objectives are reasonable
    for obj in objectives:
        assert obj in look_up_table.LOOK_UP_TABLE['campaign_objective']


    # identify rows matching the input query params
    matching_rows = REC_DATA.extract_data_slice(slice_parameters)

    # summ all events for each line_item_id matching above results
    gm_kys_view = REC_DATA.sum_events(
                        matching_rows, ['first_key'], event_rates)

    # get a list of unique game ids
    uniq_games = list(gm_kys_view.keys())
    for game_id in uniq_games:
        # calculate rates, and scores
        gm_kys_view[game_id]['click_through_rate'] = REC_DATA.calculates_rates(gm_kys_view[game_id]['click-through-event'], gm_kys_view[game_id]['impression'])

        gm_kys_view[game_id]['engagement_rate'] = REC_DATA.calculates_rates(gm_kys_view[game_id]['first_dropped'], gm_kys_view[game_id]['impression'])

        # calculate the specific score for this game
        gm_kys_view[game_id]['rec_scores'] = REC_DATA.calculate_score([gm_kys_view[game_id][obj] for obj in objectives])

    # sort the games based on 'decreasing' score
    ind_sort = np.argsort([gm_kys_view[game_id]['rec_scores'] for game_id in uniq_games])[::-1]
    
    # generate a results list of score and games
    rec_score = []
    for i in ind_sort:
        game_id = uniq_games[i]
        # get all the additional feautures for this game
        game_features = REC_DATA.extract_game_features(game_id=game_id)
        rec_score.append({'game_id': game_id,
                         'score': gm_kys_view[game_id]['rec_scores'], 'game_features': game_features
                         })

    if VERBOSE:
        print('rec_score', rec_score, file=sys.stdout)
        pass
    return json_response(rec_score)


@app.route('/get_data_dump', methods=['GET'])
def get_engine_output():
    """Returns a dictionary with all data used in the rec ending and their metadata."""

    res = {"game_data": REC_DATA.data}
    return json_response(res)

@app.route('/get_feature_dump', methods=['GET'])
def get_feature_output():
    """Returns a dictionary with all data used in the rec ending and their metadata."""

    res = {"game_features": REC_DATA.game_features}
    return json_response(res)


def create_app():
    """ Constructor
    Returns
    -------
    app : flask app
    """
    return app

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 80

    # app = create_app(config=None)
    # , use_reloader=False) # remember to set debug to False
    app.run(host='0.0.0.0', port=port, debug=VERBOSE)
