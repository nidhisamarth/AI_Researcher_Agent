import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_sentiment(review_text):
    if pd.isna(review_text) or len(str(review_text).strip()) == 0:
        return 'Unknown'
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Respond with only: Positive, Negative, or Neutral."},
                {"role": "user", "content": f"Sentiment: {review_text}"}
            ],
            max_tokens=10,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except:
        return 'Error'
