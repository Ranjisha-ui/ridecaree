import pandas as pd
import pickle

# Step 1: Load your CSV (make sure the file name is correct)
csv_path = "Customers_data_info_2025.csv"
data = pd.read_csv(csv_path)

# Step 2: Clean column names
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

# Step 3: Save it as a proper pickle file
with open("untitled8.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ New pickle file created successfully!")
