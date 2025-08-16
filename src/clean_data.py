import pandas as pd
import numpy as np

def drop_invalid_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    رکوردهای ناقص یا غیرمنطقی را حذف می‌کند.
    """
    print("تعداد ردیف‌های اولیه:", len(df))
    print("NaN در location-lat قبل از حذف:", df['location-lat'].isna().sum())
    print("NaN در location-long قبل از حذف:", df['location-long'].isna().sum())
    
    # تبدیل ستون‌ها به نوع عددی
    df['location-lat'] = pd.to_numeric(df['location-lat'], errors='coerce')
    df['location-long'] = pd.to_numeric(df['location-long'], errors='coerce')
    
    # حذف ردیف‌هایی که هر یک از ستون‌های زیر خالیه
    df = df.dropna(subset=['timestamp', 'location-lat', 'location-long', 'individual-local-identifier'])
    # چک کردن محدوده مختصات
    df = df[(df['location-lat'].between(-90, 90)) & (df['location-long'].between(-180, 180))]
    # حذف مقادیر غیرمعتبر (مثل inf)
    df = df[~df['location-lat'].isin([np.inf, -np.inf])]
    df = df[~df['location-long'].isin([np.inf, -np.inf])]
    
    print("تعداد ردیف‌ها بعد از حذف:", len(df))
    print("NaN در location-lat بعد از حذف:", df['location-lat'].isna().sum())
    print("NaN در location-long بعد از حذف:", df['location-long'].isna().sum())
    return df

def standardize_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """
    زمان‌ها را به فرمت UTC استاندارد می‌کند.
    """
    print("نمونه 5 ردیف از timestamp خام:", df['timestamp'].head().tolist())
    # سعی در تبدیل با فرمت‌های مختلف
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
    print("تعداد ردیف‌ها قبل از حذف NaN در timestamp:", len(df))
    df = df.dropna(subset=['timestamp'])
    print("تعداد ردیف‌ها بعد از حذف NaN در timestamp:", len(df))
    print("NaN در timestamp بعد از تبدیل:", df['timestamp'].isna().sum())
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    کل فرآیند تمیز کردن داده‌ها.
    """
    df = drop_invalid_records(df)
    df = standardize_timestamp(df)
    return df