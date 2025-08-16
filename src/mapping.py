import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
import os

# رنگ‌بندی رفتارها
BEHAVIOR_COLORS = {
    "rest": "gray",
    "search": "blue",
    "hunt": "red"
}

def plot_bat_paths_colored(df: pd.DataFrame, output_path: str):
    """
    مسیرهای حرکتی خفاش‌ها را روی نقشه ترسیم می‌کند و بر اساس رفتار رنگ‌بندی می‌کند.
    """
    print("ستون‌های df ورودی:", df.columns.tolist())
    print("NaN در location-lat ورودی:", df['location-lat'].isna().sum())
    print("NaN در location-long ورودی:", df['location-long'].isna().sum())
    print("تعداد ردیف‌های df ورودی:", len(df))
    
    # چک کردن مقادیر غیرمعتبر
    df = df.dropna(subset=['location-lat', 'location-long'])
    df = df[~df['location-lat'].isin([np.inf, -np.inf])]
    df = df[~df['location-long'].isin([np.inf, -np.inf])]
    print("تعداد ردیف‌ها بعد از حذف مقادیر نامعتبر:", len(df))
    
    # چک کردن اینکه دیتافریم خالی نباشه
    if len(df) == 0:
        raise ValueError("دیتافریم ورودی خالی است. لطفاً داده‌ها را بررسی کنید.")
    
    # محاسبه میانگین مختصات
    center_lat = df['location-lat'].mean()
    center_lon = df['location-long'].mean()
    print(f"مرکز نقشه: lat={center_lat}, lon={center_lon}")
    
    if pd.isna(center_lat) or pd.isna(center_lon):
        print("نمونه 5 ردیف از location-lat:", df['location-lat'].head().tolist())
        print("نمونه 5 ردیف از location-long:", df['location-long'].head().tolist())
        raise ValueError("مرکز نقشه NaN است. لطفاً داده‌ها را بررسی کنید.")
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    for bat_id, group in df.groupby('individual-local-identifier'):
        print(f"گروه {bat_id} - ستون‌ها:", group.columns.tolist())
        print(f"گروه {bat_id} - تعداد ردیف‌ها:", len(group))
        if len(group) < 2:
            print(f"گروه {bat_id} کمتر از 2 ردیف دارد، رد می‌شود.")
            continue
        coords = list(zip(group['location-lat'], group['location-long'], group['behavioural-classification']))
        for i in range(1, len(coords)):
            lat1, lon1, behavior1 = coords[i-1]
            lat2, lon2, behavior2 = coords[i]
            color = BEHAVIOR_COLORS.get(behavior2, "black")
            folium.PolyLine([(lat1, lon1), (lat2, lon2)], color=color, weight=2, opacity=0.7).add_to(m)

    m.save(output_path)

def plot_bat_heatmap(df: pd.DataFrame, output_path: str):
    """
    نقشه حرارتی حضور خفاش‌ها بر اساس نقاط رهگیری.
    """
    print("تعداد ردیف‌های df ورودی به heatmap:", len(df))
    df = df.dropna(subset=['location-lat', 'location-long'])
    df = df[~df['location-lat'].isin([np.inf, -np.inf])]
    df = df[~df['location-long'].isin([np.inf, -np.inf])]
    center_lat = df['location-lat'].mean()
    center_lon = df['location-long'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    heat_data = df[['location-lat', 'location-long']].values.tolist()
    HeatMap(heat_data, radius=10, blur=15, max_zoom=12).add_to(m)

    m.save(output_path)

def generate_maps(df: pd.DataFrame, figures_dir: str):
    """
    تولید همزمان مسیر رنگی و نقشه حرارتی
    """
    os.makedirs(figures_dir, exist_ok=True)
    
    path_colored = os.path.join(figures_dir, "bat_paths_colored.html")
    path_heatmap = os.path.join(figures_dir, "bat_activity_heatmap.html")
    
    plot_bat_paths_colored(df, path_colored)
    plot_bat_heatmap(df, path_heatmap)
    
    print(f"✅ نقشه‌ها ذخیره شدند:\n- مسیر رنگی: {path_colored}\n- نقشه حرارتی: {path_heatmap}")