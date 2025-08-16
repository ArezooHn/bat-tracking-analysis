import pandas as pd

df = pd.read_csv("data/raw/bat_tracking_Germany.csv")
print(df[['event-id', 'timestamp', 'location-lat', 'location-long', 'behavioural-classification', 'individual-local-identifier']].head(10))