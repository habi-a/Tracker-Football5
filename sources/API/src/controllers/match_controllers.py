import os
import random
import string
import subprocess
import time
import threading

from flask import request, json, Response, Blueprint
from flasgger import swag_from

from ..specs import specs_match
from ..models.match import Match
from ..models.team import TeamHasMatchPlayed
from ..auth.authentication import Auth
from ..helper import custom_response, video_url_for
from ..models import db

from subprocess import check_output, CalledProcessError, STDOUT

match_api = Blueprint('match', __name__)


def lunch(match_id, filepath, id_blue, id_red):
    result = subprocess.run(
        ["python", "/tensorflow/models/research/object_detection/tracker/tracker.py", str(match_id), str(id_red),
         str(id_blue), filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result


def generate_random_number(number_of_digits: int) -> str:
    return ''.join([random.choice(string.digits) for _ in range(number_of_digits)])


@match_api.route('', methods=['POST'])
# @swag_from(specs_match.all_match)
def post_match():
    video_storage = request.files.get('video')
    if not video_storage or video_storage.content_type != 'video/mp4':
        return custom_response({'error': 'Is not a mp4 file.'}, 400)
    req_data = request.form.to_dict()

    path_file = './src/files/'
    name_file = generate_random_number(6) + '_' + video_storage.name + '.mp4'

    video_storage.save(path_file + name_file)

    m_match = Match(name=name_file, duration="10:00", ground=1, path=path_file + name_file)
    m_match.save()
    m_team_has_match_played = TeamHasMatchPlayed(team_id=req_data['team_one'],
                                                 match_id=m_match.id,
                                                 goals=3,
                                                 possesion=70,
                                                 color=0,
                                                 ended=1)
    m_team_has_match_played.save()

    m_team_has_match_played = TeamHasMatchPlayed(team_id=req_data['team_two'],
                                                 match_id=m_match.id,
                                                 goals=2,
                                                 possesion=30,
                                                 color=1,
                                                 ended=1)
    m_team_has_match_played.save()

    t = threading.Thread(target=lunch,
                         args=(m_match.id, path_file + name_file, req_data['team_one'], req_data['team_two'],))
    t.start()

    return custom_response({'error': False, 'message': 'Sauvegarde du match.', 'data': None}, 200)


@match_api.route('/result', methods=['POST'])
# @swag_from(specs_match.all_match)
def result():
    req_data = request.get_json()
    match_id = req_data['result']['id']
    m_match = Match.query.filter_by(id=match_id).first()
    m_li_team_has_match_played = TeamHasMatchPlayed.query.filter_by(match_id=match_id).all()

    result_team = req_data['result']['red']
    for m_team_has_match_played in m_li_team_has_match_played:
        m_team_has_match_played.goals = result_team['score']
        m_team_has_match_played.possesion = result_team['possession']
        db.session.commit()
        result_team = req_data['result']['blue']

    return custom_response({'error': False, 'message': 'Update match result.', 'data': None}, 200)


@match_api.route('/all_match', methods=['GET'])
@swag_from(specs_match.all_match)
def all_match():
    matchs_in_db = Match.query.all()
    matchs = []
    for match in matchs_in_db:
        matchs.append(match.to_json())
    return custom_response({'error': False, 'message': 'Listes des matchs.', 'data': matchs}, 200)


@match_api.route('/stat_match_by_id/<int:id>', methods=['GET'])
@swag_from(specs_match.stat_match_by_id)
def stat_match_by_id(id):
    match_in_db = Match.query.filter_by(id=id).first()
    if not match_in_db:
        message = {'error': True, 'message': 'Le match existe pas.', 'data': None}
        return custom_response(message, 404)
    stats = []
    for stat in match_in_db.team_match_played:
        stats.append(stat.to_json())

    match_data = match_in_db.to_json()
    match_data['path'] = video_url_for('video', path=match_in_db.name)
    data = {**match_data, **{'stats': stats}}
    return custom_response({'error': False, 'message': 'Match stats by id.', 'data': data}, 200)
