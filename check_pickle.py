import pickle

try:
    with open("untitled8.pkl", "rb") as f:
        obj = pickle.load(f)
    print("✅ Pickle file loaded successfully!")
    print("🔹 Object type:", type(obj))
    print("🔹 Preview of object content:")
    preview = str(obj)
    print(preview[:1000])  # show first 1000 characters
except Exception as e:
    print("❌ Error while loading pickle file:", e)
