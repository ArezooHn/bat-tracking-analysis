import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_wind_turbines():
    """
    تعریف مکان فرضی توربین‌های بادی
    """
    turbine_coords = [
        (13.77, 53.36),
        (13.78, 53.37),
        (13.76, 53.35)
    ]
    gdf = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in turbine_coords],
                           crs="EPSG:4326")
    return gdf

def compare_with_turbines(df_bats, df_turbines, output_path):
    """
    مقایسه موقعیت خفاش‌ها با توربین‌های بادی و ذخیره پلات
    """
    bat_coords = df_bats[['location-long', 'location-lat']].dropna().values
    turbine_coords = np.array([(point.x, point.y) for point in df_turbines.geometry])

    plt.figure(figsize=(8, 6))
    plt.scatter(bat_coords[:, 0], bat_coords[:, 1], s=10, color='blue', alpha=0.5, label='Bat locations')
    plt.scatter(turbine_coords[:, 0], turbine_coords[:, 1], s=50, color='red', marker='^', label='Wind turbines')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Bat Locations vs Wind Turbines')
    plt.legend()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()