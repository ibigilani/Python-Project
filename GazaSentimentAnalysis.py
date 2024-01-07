import http.client
import json
import emoji
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from datetime import datetime
import DatabaseAccess
import visualization

# Function to retrieve feedback IDs based on a specific hashtag
def get_feedback_ids(api_key):
    feedback_ids = []
    try:
        # Establishing a connection to the API service
        conn = http.client.HTTPSConnection("axesso-facebook-data-service.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': "axesso-facebook-data-service.p.rapidapi.com"
        }

        # Sending a request to get data for a specific hashtag
        conn.request("GET", "/fba/facebook-search-hashtag?hashtag=gaza", headers=headers)
        response = conn.getresponse()
        data = response.read()

        try:
            response_data = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return None

        # Parsing the response to extract feedback IDs
        posts = response_data.get("posts", [])
        for post in posts:
            rendering_strategy = post.get("rendering_strategy")
            explore_view_model = rendering_strategy.get("explore_view_model") if rendering_strategy else None
            story = explore_view_model.get("story") if explore_view_model else None
            feedback = story.get("feedback") if story else None
            id = feedback.get("id") if feedback else None
            if isinstance(id, str):
                feedback_ids.append(id)
        return feedback_ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to retrieve comments for a given feedback ID
def get_comments(feedback_id, api_key):
    comments = []
    try:
        # Establishing a connection to the API service
        conn = http.client.HTTPSConnection("axesso-facebook-data-service.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': "axesso-facebook-data-service.p.rapidapi.com"
        }

        # Sending a request to get comments for a specific feedback ID
        conn.request("GET", f"/fba/facebook-lookup-comments?feedbackId={feedback_id}", headers=headers)
        response = conn.getresponse()
        data = response.read()

        try:
            response_data = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return comments

        # Parsing the response to extract comments
        comments_data = response_data.get("comments", {}).get("data", {}).get("feedback", {}).get("display_comments", {}).get("edges", [])
        for comment_data in comments_data:
            node = comment_data.get("node")
            preferred_body = node.get("preferred_body") if node else None
            text = preferred_body.get("text") if preferred_body else None
            created_time = node.get("created_time") if node else None
            if text is not None and created_time is not None:
                datetime_object = datetime.utcfromtimestamp(created_time)
                formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                comments.append((text, formatted_datetime))
            
        return comments
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return comments

# Converts emojis in the text to their textual representation
def convert_emojis_to_text(text):
    return emoji.demojize(text, delimiters=("", "")) 

# Translates a given text to English
def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

# Analyzes the sentiment of a given text
def get_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

# Setup for NLTK, including downloading the necessary lexicon
def setup_nltk():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon')

# Main function to orchestrate the sentiment analysis process
def main():
    setup_nltk()
    feedback_ids = get_feedback_ids("2c2f7defb1msh9caa0876ba84604p142418jsnf8b0837da372")
    
    for feedback_id in feedback_ids:
        # Check if the feedback ID already exists in the database
        if not DatabaseAccess.get_from_feedbackIds(feedback_id):
            sentiments = []

            DatabaseAccess.insert_into_feedbackIds(feedback_id)
            feedback_id_in_db = DatabaseAccess.get_from_feedbackIds(feedback_id)

            comments = get_comments(feedback_id, "2c2f7defb1msh9caa0876ba84604p142418jsnf8b0837da372")

            for comment, date in comments:
                converted_comment = convert_emojis_to_text(comment)
                translated_comment = translate_to_english(converted_comment)
                sentiment = get_sentiment(translated_comment)
                sentiments.append((translated_comment, date, sentiment.get('compound')))

            for sentiment_data in sentiments:
                DatabaseAccess.insert_into_sentiments(sentiment_data[1], sentiment_data[2], sentiment_data[0], feedback_id_in_db)

    sentiment_list = DatabaseAccess.get_all_sentiments()
    visualization.showReport(sentiment_list)
  
if __name__ == "__main__":
    main()
