import requests
import datetime
from flask import jsonify
from config import CLIENT_ID, CLIENT_SECRET
from routes import OAUTH_URL

def return_json(isSuccess, returnMessage):
    return jsonify(
        success=isSuccess,
        message=returnMessage
    )

def get_new_access_token(refresh_token):
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    response = requests.post(OAUTH_URL, data=payload, verify=False)
    new_access_token = response.json()['access_token']
    return new_access_token

def convert_from_greenwich_to_singapore_time(timestring, format):
    greenwich_time = datetime.datetime.strptime(timestring, format)
    sg_time_object = greenwich_time + datetime.timedelta(hours=8)

    return sg_time_object