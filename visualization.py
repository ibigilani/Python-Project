import pandas as pd
import matplotlib.pyplot as plt

def showReport(sentimentTuple):
   
    df = pd.DataFrame(sentimentTuple, columns=['Text', 'Datetime', 'Sentiment'])

    # Convert the 'Datetime' column to datetime
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Extract date from 'Datetime'
    df['Date'] = df['Datetime'].dt.date

    # Plotting all data points
    plt.figure(figsize=(15, 7))
    plt.scatter(df['Datetime'], df['Sentiment'], alpha=0.6, color='blue', label='Sentiment Score')

    # Beautify the x-axis to show dates nicely
    plt.gcf().autofmt_xdate()

    plt.title('Sentiment Score Over Time')
    plt.xlabel('Datetime')
    plt.ylabel('Sentiment Score')
    plt.grid(True)
    plt.legend()
    plt.show()

