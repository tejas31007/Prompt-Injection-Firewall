import pandas as pd
import numpy as np

# Using the exact path you just found
file_path = r"C:\Users\tejal\OneDrive\Desktop\Prompt Injection Firewall\Datasets\train-prompt-classification.parquet"

print("Loading dataset...")
df = pd.read_parquet(file_path)
print(f"Original size: {len(df)} rows")

# 1. Clean the Data
print("\nCleaning data...")
df = df.dropna(subset=['prompt', 'label']) # Remove empty rows
df = df.drop_duplicates(subset=['prompt']) # Remove duplicate prompts
print(f"Size after cleaning: {len(df)} rows")

# 2. Map Binary Labels to your Custom 1-10 Scale
print("\nMapping to 1-10 intent scale...")
np.random.seed(42) # Keeps the random numbers consistent every time you run this

def map_intent_score(label):
    if label == 0:
        return np.random.randint(1, 4)   # Safe gets a 1, 2, or 3
    else:
        return np.random.randint(8, 11)  # Malicious gets an 8, 9, or 10

df['intent_score'] = df['label'].apply(map_intent_score)

# 3. Save the prepared dataset
output_path = "prepared_firewall_data.parquet"
df[['prompt', 'intent_score']].to_parquet(output_path, index=False)

print(f"\nSuccess! Cleaned and scaled data saved as '{output_path}'")
print("\n=== Your New Training Data ===")
print(df[['prompt', 'intent_score']].head())