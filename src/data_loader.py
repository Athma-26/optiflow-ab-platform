import pandas as pd

def load_csv_data(filepath: str) -> pd.DataFrame:
    """
    Loads a CSV file and performs basic validation.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            raise ValueError("File is empty.")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file at {filepath}")