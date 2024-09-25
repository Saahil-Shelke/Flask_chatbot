from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import langdetect  # You need to install the langdetect library: pip install langdetect
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.chat_db
chats_collection = db.chats

ist = pytz.timezone('Asia/Kolkata')

genai.configure(api_key="API_KEY") #saahil.helke@gmail.com

generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
marathi_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="कृपया लक्षात घ्या की या मॉडेलने वापरकर्त्याच्या प्रश्नांची उत्तरे मराठीत देणे अपेक्षित आहे. जर वापरकर्ता कृषीशी संबंधित प्रश्न विचारत असेल, तर त्यास यथाशक्ती उत्तर द्या. जर वापरकर्ता अन्य कोणत्याही प्रकारचे प्रश्न विचारत असेल, तर उत्तर द्या: 'माफ करा, मी फक्त कृषीशी संबंधित प्रश्नांची उत्तरे देऊ शकतो.'"
)
hindi_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="कृपया ध्यान दें कि इस मॉडल को उपयोगकर्ता के प्रश्नों का उत्तर हिंदी में देना है। यदि उपयोगकर्ता कृषि से संबंधित प्रश्न पूछता है, तो जितना संभव हो उतना उत्तर दें। यदि उपयोगकर्ता किसी अन्य प्रकार का प्रश्न पूछता है, तो उत्तर दें: 'मुझे खेद है, मैं केवल कृषि से संबंधित प्रश्नों का उत्तर दे सकता हूं।'"
)
english_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Please answer the user's questions in English. If the user asks about agriculture, weather, or farming, provide a relevant response. If the user asks non-agriculture-related questions, respond with: 'Sorry, I can only answer questions related to agriculture.'"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    try:
        detected_language = langdetect.detect(question)
    except:
        detected_language = 'en'
    
    if detected_language == 'mr':
        response = marathi_model.start_chat().send_message(question)
    elif detected_language == 'hi':
        response = hindi_model.start_chat().send_message(question)
    else:
        response = english_model.start_chat().send_message(question)

        chat_data = {
        "user_input": question,
        "system_response": response.text,
        "language": detected_language,
        "timestamp": datetime.now(ist),
        "userdetails": "123456789",
        "sessionid": "1"
    }
    chats_collection.insert_one(chat_data)

    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
