import pandas as pd
import numpy as np

def detect_question_type(column_data, column_name):
    if pd.api.types.is_numeric_dtype(column_data):
        unique_values = column_data.nunique()
        return 'rating_scale' if unique_values <= 10 else 'numeric'
    elif pd.api.types.is_string_dtype(column_data):
        unique_values = column_data.nunique()
        if unique_values <= 3:
            return 'binary'
        elif unique_values < 20:
            return 'categorical'
        else:
            return 'open_text'
    else:
        return 'date'
