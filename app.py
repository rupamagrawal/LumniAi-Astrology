import pandas as pd
from flask import Flask, render_template, request
import google.generativeai as genai

# Load the CSV file
astro_data = pd.read_csv('astrology_data.csv')

# Convert DataFrame to dictionary
astro_dict = astro_data.set_index('sign').T.to_dict()

# Initialize the Gemini API client
genai.configure(api_key='AIzaSyA8pZjilnuWl83bLQ5uC6QlDytqIeQXGQc')

# Function to retrieve astrology info
def get_astrological_info(sign):
    return astro_dict.get(sign.capitalize(), {"description": "I'm sorry, I don't have information on that sign."})['description']

# Function to generate AI response
def generate_response(user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"User asked about {user_input}. Provide detailed astrological information."
    response = model.generate_content(prompt)
    return response.text

# Flask app setup
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    response = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        astro_info = get_astrological_info(user_input)
        if "I'm sorry" in astro_info:
            response = generate_response(user_input)
        else:
            response = astro_info
    return render_template('index.html', response=response)

if __name__ == "__main__":
    app.run(debug=True)
