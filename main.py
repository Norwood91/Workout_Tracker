import requests
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values('.env')
APP_ID = config['APP_ID']
API_KEY = config['API_KEY']
USER = config['USER']
PASS = config['PASS']

GENDER = 'Male'
WEIGHT_KG = 74.4
HEIGHT_CM = 175.3
AGE = 30


exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
sheet_endpoint = 'https://api.sheety.co/f87960954e6f866405dd1b0ece983f63/workoutTracking/workouts'


exercise_text = input('What exercise(s) did you complete today?: ')

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
    'Content-Type': 'application/json'
}

parameters = {
    'query': exercise_text,
    'gender': GENDER,
    'weight_kg': WEIGHT_KG,
    'height_cm': HEIGHT_CM,
    'age': 30
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
response.raise_for_status()
result = response.json()

todays_date = datetime.now().strftime('%d/%m/%Y')
current_time = datetime.now().strftime('%X')

for exercise in result['exercises']:
    sheet_inputs = {
        'workout': {
            'date': todays_date,
            'time': current_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=(USER, PASS))