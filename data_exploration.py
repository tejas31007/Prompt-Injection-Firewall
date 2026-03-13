import pandas as pd
import os

# 1. Update this path to the exact name of one of your downloaded Parquet files
file_path = "C:\\Users\\tejal\\OneDrive\\Desktop\\Prompt Injection Firewall\\Datasets\\train-prompt-classification.parquet"

def inspect_parquet(path):
    print(f"Loading data from: {path}...\n")
    try:
        # Load the parquet file into a Pandas DataFrame
        df = pd.read_parquet(path)
        
        # Display the anatomy of the dataset
        print("=== Dataset Overview ===")
        print(f"Total Rows: {len(df)}")
        print(f"Columns Found: {df.columns.tolist()}\n")
        
        print("=== First 3 Rows ===")
        print(df.head(3))
        
    except FileNotFoundError:
        print(f"Oops! Couldn't find a file named '{path}'. Double-check the spelling and make sure it's in the same folder as this script.")

if __name__ == "__main__":
    inspect_parquet(file_path)