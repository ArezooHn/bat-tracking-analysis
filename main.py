import os
import pandas as pd
import numpy as np
from src.load_data import load_raw_data
from src.clean_data import clean_data
from src.analysis import calculate_movement_metrics, classify_behavior
from src.mapping import plot_bat_paths_colored, generate_maps
from src.kde_analysis import run_kde_analysis
from src.wind_turbine import load_wind_turbines, compare_with_turbines

# مسیر فایل‌ها
RAW_FILE = "data/raw/bat_tracking_Germany.csv"
CLEAN_FILE = "data/processed/cleaned_data.csv"
METRICS_FILE = "data/processed/movement_metrics.csv"
MAP_FILE = "outputs/figures/bat_paths_map.html"
FIGURES_DIR = "outputs/figures"
KDE_FIG = "outputs/figures/kde_map.png"
COMPARISON_FIG = "outputs/figures/comparison.png"

# ---------- ۱. بارگذاری و تمیز کردن ----------
df = load_raw_data(RAW_FILE)
print("ستون‌های داده خام:", df.columns.tolist())
print("NaN در location-lat خام:", df['location-lat'].isna().sum())
print("NaN در location-long خام:", df['location-long'].isna().sum())
print("NaN در behavioural-classification خام:", df['behavioural-classification'].isna().sum())
print("نمونه 5 ردیف از location-lat خام:", df['location-lat'].head().tolist())
print("نمونه 5 ردیف از location-long خام:", df['location-long'].head().tolist())
df_clean = clean_data(df)
print("ستون‌های df_clean:", df_clean.columns.tolist())
df_clean.to_csv(CLEAN_FILE, index=False)

# ---------- ۲. محاسبه متریک‌ها ----------
df_metrics = calculate_movement_metrics(df_clean)
df_metrics = classify_behavior(df_metrics)
print("ستون‌های df_metrics:", df_metrics.columns.tolist())
df_metrics.to_csv(METRICS_FILE, index=False)

# ---------- 🎯 فیلترها (اختیاری) ----------
df_filtered = df_clean.copy()
print("NaN در location-lat فیلترشده:", df_filtered['location-lat'].isna().sum())
print("NaN در location-long فیلترشده:", df_filtered['location-long'].isna().sum())
print("تعداد ردیف‌های df_filtered:", len(df_filtered))

# ---------- ۳. رسم نقشه‌ها ----------
os.makedirs(os.path.dirname(MAP_FILE), exist_ok=True)
plot_bat_paths_colored(df_filtered, MAP_FILE)
generate_maps(df_metrics, FIGURES_DIR)
print("✅ پردازش مسیر و نقشه‌ها کامل شد!")

# ---------- ۴. KDE و مقایسه با توربین‌ها ----------
df_turbines = load_wind_turbines()
os.makedirs(os.path.dirname(KDE_FIG), exist_ok=True)
run_kde_analysis(df_clean, bandwidth=0.01, output_path=KDE_FIG)
os.makedirs(os.path.dirname(COMPARISON_FIG), exist_ok=True)
compare_with_turbines(df_clean, df_turbines, COMPARISON_FIG)
print("✅ KDE و مقایسه با توربین‌ها هم انجام شد!")