# Facebook Sentiment Analysis App

## Author

Ibrahim Gilani

## Overview

The Facebook Sentiment Analysis App is a Python application designed to retrieve and analyze comments on Facebook posts containing the hashtag #Gaza. The primary objective of the app is to gauge public sentiment regarding the ongoing events in Palestine, particularly the Gaza region. By analyzing the comments associated with these posts, the app aims to provide insights into the emotions and opinions expressed by Facebook users.

## Technologies Used

The app utilizes various technologies and libraries to achieve its objectives:

1. **Python**: The core programming language used for developing the application.

2. **HTTP Client**: The `http.client` module is employed to establish connections to the Facebook data service API for retrieving posts and comments.

3. **JSON**: The app leverages JSON for parsing and handling data received from the API.

4. **Emoji**: The `emoji` library is used to convert emojis in comments to their textual representations.

5. **Natural Language Toolkit (NLTK)**: NLTK, and more specifically the Sentiment Intensity Analyzer, is utilized for sentiment analysis of comments.

6. **Google Translate API**: The `googletrans` library is used for translating comments to English, ensuring a common language for sentiment analysis.

7. **Database Access**: The app interacts with a SQL Server database to store and retrieve data related to feedback IDs, comments, and sentiment analysis results.

8. **Data Visualization**: The `pandas` and `matplotlib` libraries are employed for data manipulation and visualization, respectively.

## How It Works

The Facebook Sentiment Analysis App follows these key steps:

1. **Data Retrieval**: The app connects to the Facebook data service API using an API key and retrieves posts containing the hashtag #Gaza.

2. **Feedback IDs Extraction**: The app extracts feedback IDs from the retrieved posts to identify unique comments for sentiment analysis.

3. **Comment Retrieval**: For each feedback ID, the app fetches the associated comments from the API.

4. **Data Processing**: The comments are processed, including emoji conversion and translation to English.

5. **Sentiment Analysis**: The NLTK Sentiment Intensity Analyzer is used to analyze the sentiment of each comment.

6. **Database Interaction**: Data related to feedback IDs, comments, and sentiment analysis results are stored and retrieved from a SQL Server database.

7. **Data Visualization**: The sentiment analysis results are visualized over time, allowing viewers to understand sentiment trends.

## Usage

To use the Facebook Sentiment Analysis App:

1. Ensure you have the required dependencies and libraries installed (specified in the code and environment).

2. Set up your API key for access to the Facebook data service API.

3. Run the `main()` function in the Python script to initiate the sentiment analysis process.

4. The app will retrieve data, perform sentiment analysis, and store the results in the database.

5. You can visualize the sentiment trends using the provided visualization functions.

Please note that you need to configure the database connection by providing the appropriate database connection string in the `config.json` file.

## Disclaimer

The sentiment analysis results are based on text analysis and may not represent the complete sentiments of users. Use the app's insights responsibly and consider the context and limitations of sentiment analysis.




