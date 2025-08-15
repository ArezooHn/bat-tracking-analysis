import pandas as pd

def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    داده خام خفاش‌ها را بارگذاری می‌کند.
    """
    df = pd.read_csv(filepath)
    return df