from flask import Blueprint, jsonify
from routes import LIST_ALL_TEAM
from db import get_sorted_teams
from utils import return_json

team_api = Blueprint('team_api', __name__)

@team_api.route(LIST_ALL_TEAM, methods=['GET'])
def list_all_team():
    team_list = get_sorted_teams()
    return return_json(True, "Successfully retrieved all teams.", team_list)
