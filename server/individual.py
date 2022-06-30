import requests
from time import time
from flask import Blueprint, request, jsonify
from routes import LIST_ALL_INDIVIDUAL, GET_HALL_OF_FAME, UPDATE_INDIVIDUAL_TOTAL_MILEAGE,ACTIVITIES_URL
from config import EVENT_END_TIME_OBJECT, EVENT_START_TIME_OBJECT
from db import get_data, update_data, get_sorted_names
from utils import return_json
from utils import get_new_access_token, convert_from_greenwich_to_singapore_time

individual_api = Blueprint('individual_api', __name__)

@individual_api.route(LIST_ALL_INDIVIDUAL, methods=['GET'])
def list_all_individual():
    name_list = get_sorted_names()
    return return_json(True, "Successfully retrieved all individuals.", name_list)

@individual_api.route(GET_HALL_OF_FAME, methods=['GET'])
def get_hall_of_fame():
    # get top 5 individuals for longest run, furthest run, highest accmulated mileage
    # each a different function from DBs
    return

@individual_api.route(UPDATE_INDIVIDUAL_TOTAL_MILEAGE, methods=['POST'])
def update_individual_total_mileage():
    name = request.form.get('name')
    if name == None:
        return return_json(False, f"Missing name field in request.")

    new_mileage = update_individual_total_mileage_from_strava(name)
    person_mileage_object = {
        "name": name,
        "mileage": new_mileage
    }
    return return_json(True, f"Successfully updated {name}'s total mileage to {new_mileage} km.", person_mileage_object)

def update_individual_total_mileage_from_strava(name):
    person = get_data(name)

    access_token_expiry = person.get("access_token_expired_at")
    if access_token_expiry <= time():
        access_token = get_new_access_token(person.get("refresh_token"))
    else:
        access_token = person.get("access_token")

    headers = {
            "Authorization": "Bearer " + access_token
    }
    activityRequest = requests.get(ACTIVITIES_URL, headers=headers)
    if activityRequest.status_code != 200:
        return return_json(
            False, 
            f"Failed to retrieve activities from Strava.\n Error code: {activityRequest.status_code}"
        )
    activityList = activityRequest.json()

    totalDistance = 0
    for activity in activityList:
        greenwich_time_string = activity.get('start_date')
        sg_time_object = convert_from_greenwich_to_singapore_time(greenwich_time_string, "%Y-%m-%dT%H:%M:%SZ")
        if sg_time_object < EVENT_START_TIME_OBJECT or sg_time_object > EVENT_END_TIME_OBJECT:
            continue

        if activity.get('type') != 'Run':
            continue

        totalDistance = totalDistance + activity.get('distance')

    totalDistance = int(totalDistance / 1000)
    update_data(name, "mileage", totalDistance)

    return totalDistance