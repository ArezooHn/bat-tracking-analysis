import pandas as pd
from geopy.distance import geodesic

def calculate_movement_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    محاسبه فاصله (متر) و سرعت (متر بر ثانیه) بین نقاط.
    """
    df = df.sort_values(by=['individual-local-identifier', 'timestamp'])
    
    distances = []
    speeds = []
    
    for bat_id, group in df.groupby('individual-local-identifier'):
        prev_point = None
        prev_time = None
        
        for _, row in group.iterrows():
            if prev_point is None:
                distances.append(0)
                speeds.append(0)
            else:
                dist = geodesic(prev_point, (row['location-lat'], row['location-long'])).meters
                time_diff = (row['timestamp'] - prev_time).total_seconds()
                speed = dist / time_diff if time_diff > 0 else 0
                distances.append(dist)
                speeds.append(speed)
            
            prev_point = (row['location-lat'], row['location-long'])
            prev_time = row['timestamp']
    
    df['distance_m'] = distances
    df['speed_mps'] = speeds
    return df

def classify_behavior(df: pd.DataFrame) -> pd.DataFrame:
    """
    بر اساس سرعت یا داده‌های رفتاری، برچسب رفتار را تعیین می‌کند.
    """
    def behavior_from_speed(speed):
        if speed < 1:
            return "rest"
        elif speed < 5:
            return "search"
        else:
            return "hunt"
    
    df['behavior_estimated'] = df['speed_mps'].apply(behavior_from_speed)
    return df