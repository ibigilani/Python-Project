import http.client
import json
import emoji
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import nltk

def getFeedBackId(api_key):
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
                return id
        return None
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
            if text is not None:
                list_of_comments.append(text)
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
    # TextBlob sentiment analysis (it works for basic English text)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1 where 1 means positive sentiment

    # VADER sentiment analysis (more suited for social media texts, English only)
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    
    return polarity, sentiment_score

def setup_nltk():
    # Check if vader_lexicon is already downloaded
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        # Download it if not present
        nltk.download('vader_lexicon')

setup_nltk()
fId = getFeedBackId("8b08ebd98emsh5da1790990b14d7p11566bjsnc7b22e897d4d")
listOfComments = getComments(fId,"8b08ebd98emsh5da1790990b14d7p11566bjsnc7b22e897d4d")
lisOfSentiments = []

for comment in listOfComments:
    comment = convert_emojis_to_text(comment)
    comment = translate_to_english(comment)
    sentiment = get_sentiment(comment)
    lisOfSentiments.append(sentiment)

for x in lisOfSentiments:
    print(x)

