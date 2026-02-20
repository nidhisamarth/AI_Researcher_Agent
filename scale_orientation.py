import pandas as pd
import numpy as np

def detect_scale_orientation(column_data, column_name):
    min_rating = column_data.min()
    max_rating = column_data.max()
    return f"Ascending ({min_rating}=worst, {max_rating}=best)"
