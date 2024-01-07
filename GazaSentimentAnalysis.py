import http.client
import json
import emoji
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from datetime import datetime
import DatabaseAccess
import visualization
import schedule
import time


def getFeedBackId(api_key):
    listOfIds=[]
    try:
        conn = http.client.HTTPSConnection("axesso-facebook-data-service.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': f"{api_key}",
            'X-RapidAPI-Host': "axesso-facebook-data-service.p.rapidapi.com"
        }

        conn.request("GET", "/fba/facebook-search-hashtag?hashtag=gaza", headers=headers)
        res = conn.getresponse()
        data = res.read()

        try:
            new_dict = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return None

        list_of_posts = new_dict.get("posts", [])
        for post in list_of_posts:
            rendering_strategy = post.get("rendering_strategy")
            explore_view_model = rendering_strategy.get("explore_view_model") if rendering_strategy else None
            story = explore_view_model.get("story") if explore_view_model else None
            feedback = story.get("feedback") if story else None
            id = feedback.get("id") if feedback else None
            if isinstance(id, str):
                listOfIds.append(id)
        return listOfIds
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def getComments(feedbackId,api_key):
    list_of_comments = []
    try:
        conn = http.client.HTTPSConnection("axesso-facebook-data-service.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': f"{api_key}",
            'X-RapidAPI-Host': "axesso-facebook-data-service.p.rapidapi.com"
        }

        conn.request("GET", f"/fba/facebook-lookup-comments?feedbackId={feedbackId}", headers=headers)
        res = conn.getresponse()
        data = res.read()

        try:
            new_dict = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return list_of_comments

        comments_data = new_dict.get("comments", {}).get("data", {}).get("feedback", {}).get("display_comments", {}).get("edges", [])
        
        for commentDict in comments_data:
            node = commentDict.get("node")
            preferred_body = node.get("preferred_body") if node else None
            text = preferred_body.get("text") if preferred_body else None
            created_time = node.get("created_time") if node else None
            if text is not None and created_time is not None:
                datetime_object = datetime.utcfromtimestamp(created_time)
                formatted_datetime = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                list_of_comments.append((text, formatted_datetime))
            
        return list_of_comments
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return list_of_comments

def convert_emojis_to_text(text):
    return emoji.demojize(text, delimiters=("", "")) 

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

def get_sentiment(text):
    # VADER sentiment analysis (more suited for social media texts, English only)
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

def setup_nltk():
    # Check if vader_lexicon is already downloaded
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        # Download it if not present
        nltk.download('vader_lexicon')

def main():
    setup_nltk()
    listOf_FIds = getFeedBackId("2c2f7defb1msh9caa0876ba84604p142418jsnf8b0837da372")
    
    for id in listOf_FIds:
        # Check if the feedback ID already exists in the database
        existing_id = DatabaseAccess.get_from_feedbackIds(id)

        if not existing_id:
            lisOfSentiments = []

            DatabaseAccess.insert_into_feedbackIds(id)
            fID = DatabaseAccess.get_from_feedbackIds(id)

            listOfComments = getComments(id, "2c2f7defb1msh9caa0876ba84604p142418jsnf8b0837da372")

            for comment in listOfComments:
                OG_comment = comment[0]
                date = comment[1]
                emojis_converted_comment = convert_emojis_to_text(OG_comment)
                translated_comment = translate_to_english(emojis_converted_comment)
                sentiment = get_sentiment(translated_comment)
                lisOfSentiments.append((translated_comment, date, sentiment.get('compound')))

            for senty in lisOfSentiments:
                DatabaseAccess.insert_into_sentiments(senty[1], senty[2], senty[0], fID)

    s_list= DatabaseAccess.get_all_sentiments()
    visualization.showReport(s_list)
  
if __name__ == "__main__":
    main()
