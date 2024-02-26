import os, re
import openai
import datetime
import spacy
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from get_hotel_list import search_hotels
from get_restaurant_list import get_restaurants
from get_weather_forecast import weather_forecast
import gradio as gr
from flask import Flask, render_template, request, jsonify
import openai
import spacy
import datetime
import re

load_dotenv()

# bot = Bot(token="Token")
# dp = Dispatcher(bot)

openai.api_key = 'API_KEY'

chat_history = []

app = Flask(__name__)

def send_to_chatGPT(chat_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    return response


def collect_location(query):
    model_path = r"models/en_core_web_lg-3.4.1"
    nlp = spacy.load(model_path)
    doc = nlp(query)
    locations = [entity.text for entity in doc.ents if entity.label_ == "LOC" or entity.label_ == "GPE"]
    # print(locations)
    return locations


def collect_dates(query):
    date = datetime.datetime.now().date()
    if 'today' in query.lower():
        query = query.replace('today', str(date))
    # print('Query in collect dates function:', query)
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f'Please give the dates mentioned in the text: {query} in "yyyy-mm-dd" format. Or respond with "There are no dates in the query"',
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.9
    )
    # Get the generated response from ChatGPT
    response = response.choices[0].text.strip()
    return response



def chatbot_response(user_input):
    chat_history.append({'role': 'user', 'content': user_input})

    location = collect_location(user_input)

    if 'weather' in user_input.lower() or 'temperature' in user_input.lower():
        if location:
            response = weather_forecast(location[0])
            if response:
                response = response
            else:
                response = 'There are no weather forecasts for the given location'
        else:
            response = 'There are no locations in the query. Please enter a specific location.'

    elif 'hotels' in user_input.lower() or 'book hotel' in user_input.lower() or 'book hotels' in user_input.lower() or 'book a hotel' in user_input.lower():
        date_response = collect_dates(user_input)
        if date_response != 'There are no dates in the query.':
            result = re.findall('\d{4}-\d{1,2}-[0-9]{1,2}', date_response)
            if int(result[0][-2:]) > int(result[-1][-2:]):
                checkIN = result[-1]
                checkOut = result[0]
            else:
                checkIN = result[0]
                checkOut = result[-1]
        else:
            checkIN = str(datetime.datetime.now().date())
            checkOut = str(datetime.datetime.now().date())

        if location:
            data = search_hotels(location[0], checkIN, checkOut)
            if data:
                response = ''
                for i in data[:5]:
                    response += f"Hotel Name:{i['Hotel Name']}\n"
                    response += f"Location:{i['Location']}\n"
                    response += f"Per Night Fare:{i['Per Night Fare']}\n"
                    response += '\n' * 2
            else:
                response = 'Location not found.'
        else:
            response = 'There are no locations in the query. Please enter a specific location.'

    elif 'restaurant' in user_input.lower() or 'restaurants' in user_input.lower():
        if location:
            data = get_restaurants(location[0])
            if data:
                response = ''
                for i in data[:5]:
                    response += f"Restaurant Name: {i['Name']}\n"
                    response += f"Address: {i['Address']}\n"
                    response += f"Cuisines: {i['Cuisines']}\n"
                    response += '\n' * 2
            else:
                response = 'Location not found.'
        else:
            response = 'There are no locations in the query. Please enter a specific location.'
    else:
        result = send_to_chatGPT(chat_history)
        response = result.choices[0].message.content

    chat_history.append({'role': 'assistant', 'content': response})
    return response


@app.route('/')
def chatbot_interface():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    user_input = request.form.get('user_input')
    response = chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()

# if __name__ == "__main__":
#     executor.start_polling(dp)








