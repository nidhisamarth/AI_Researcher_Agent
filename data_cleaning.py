import pandas as pd

def remove_duplicates(data):
    original_count = len(data)
    cleaned_data = data.drop_duplicates()
    removed = original_count - len(cleaned_data)
    print(f"Removed {removed} duplicate reviews")
    return cleaned_data

def handle_missing_ratings(data):
    original_count = len(data)
    cleaned_data = data.dropna(subset=['Rating'])
    removed = original_count - len(cleaned_data)
    print(f"Removed {removed} reviews with missing ratings")
    return cleaned_data

def handle_missing_text(data):
    original_count = len(data)
    cleaned_data = data.dropna(subset=['Review Text'])
    removed = original_count - len(cleaned_data)
    print(f"Removed {removed} reviews with missing text")
    return cleaned_data

def clean_survey_data(data):
    print(f"\nStarting cleaning process...")
    data = remove_duplicates(data)
    data = handle_missing_ratings(data)
    data = handle_missing_text(data)
    print("\nData Cleaning Complete...")
    return data
