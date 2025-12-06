import pandas as pd
import os

class DatasetLoader:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self, filename):
        """Loads dataset from CSV."""
        file_path = os.path.join(self.data_path, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} not found in {self.data_path}")
        
        return pd.read_csv(file_path)

    def load_all_data(self):
        """Loads and merges all CSV files in the data directory."""
        all_files = [f for f in os.listdir(self.data_path) if f.endswith('.csv')]
        if not all_files:
            raise FileNotFoundError("No CSV files found in data directory.")
        
        df_list = []
        for f in all_files:
            try:
                df = pd.read_csv(os.path.join(self.data_path, f))
                df_list.append(df)
            except Exception as e:
                print(f"Error loading {f}: {e}")
        
        if not df_list:
            return pd.DataFrame()
            
        return pd.concat(df_list, ignore_index=True)

    def clean_data(self, df):
        """Basic preprocessing."""
        # Remove duplicates
        df = df.drop_duplicates()
        # Handle missing values
        df = df.fillna(0)
        return df
