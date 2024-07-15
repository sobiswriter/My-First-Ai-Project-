from flask import Flask, request, jsonify, send_from_directory
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import random
import time
import re  # For regular expressions

vertexai.init(project="x-avenue-425405-v4", location="us-central1")
model = TextGenerationModel.from_pretrained("text-bison@001")

app = Flask(__name__, static_folder='static')
chat_history = []  # Store conversation history

# Southern Phrases (Expanded and Enhanced)
southern_phrases = {
    "greetings": [
        "Howdy partner! What's on your mind?",
        "Well, howdy there! How can I help you today?",
        "Greetings, y'all! What brings you to my digital doorstep?",
        "Howdy, stranger. You got a name or can I just call you 'Tex'? Hya",
        "Remember, partner, even the toughest trails lead somewhere beautiful."
    ],
    "help_offer": "Is there anything I can do for ya today?",
    "farewells": [
        "Catch you later, space cowboy!",
        "Farewell, my friend! May your circuits stay sparkly!",
        "Y'all come back now, ya hear?",
        "The sun sets but don't worry, we shall meet again!",
        "May your horse always find water and your heart always find peace",
        "See ya later, alligator!"
    ],
    "thanks": [
        "You're most welcome, partner!",
        "Don't mention it, mate!",
        "Happy to help, y'all!",
        "Kindness like yours is rarer than a sober cowboy!",
        "I'd tip my hat to you, but the wind might blow it clean away"
    ],
    "weather": [
        "Well, the weather's lookin' mighty fine today, wouldn't you say?",
        "Looks like a beautiful day for some fishin', ain't it?",
        "The sky's bluer than a bluebird's wing out there!"
    ],
    "general_responses": [
        "That's a mighty fine question!",
        "Well, I'll be hornswoggled!",
        "Ain't that the truth!",
        "You can say that again.",
        "I'm listenin'.",
        "Easy there, partner."
    ]
}


def apply_southern_charm(text):
    # Southern Vocabulary Replacements (Improved with Regex)
    southern_replacements = {
        r"\bhi\b": "Howdy",
        r"\byou\b": "y'all",
        r"\bare\b": "are fixin' to",
        r"\bgoing\b": "goin'",
        r"\bwant\b": "wanna",
        r"\byes\b": "yessir",  # Case-insensitive match for 'yes'
        r"\bno\b": "no sir"  # Case-insensitive match for 'no'
    }

    for pattern, replacement in southern_replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def get_chatbot_response(user_input):
    chat_history.append(f"User: {user_input}")

    response = model.predict(
        prompt=f"{''.join(chat_history)}",  # Include chat history
        temperature=0.8,
        max_output_tokens=150
    )
    chatbot_response = response.text
    chatbot_response = apply_southern_charm(chatbot_response)

    # Enhanced Response Selection based on Keywords
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in ["how are you", "hey"]):
        chatbot_response = random.choice(southern_phrases["greetings"]) + " " + southern_phrases["help_offer"]
    elif "thank you" in user_input_lower or "thanks" in user_input_lower:
        chatbot_response = random.choice(southern_phrases["thanks"])
    elif "weather" in user_input_lower:
        chatbot_response = random.choice(southern_phrases["weather"])
    elif any(keyword in user_input_lower for keyword in ["what is", "how do", "where is"]):
        chatbot_response = random.choice(southern_phrases["general_responses"]) + " " + chatbot_response

    chat_history.append(f"Chatbot: {chatbot_response}")
    return chatbot_response


# Flask Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index2.html')


@app.route('/static2/<path:filename>')
def serve_static(filename):
    return send_from_directory('static2', filename)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if user_message:
        response = get_chatbot_response(user_message)
        return jsonify({'response': response})
    else:
        initial_greeting = random.choice(southern_phrases["greetings"])
        return jsonify({"response": initial_greeting})


if __name__ == '__main__':
    app.run(debug=True)

