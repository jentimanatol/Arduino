import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import hashlib
from datetime import datetime, timedelta

# API Key data
api_key_data = {
    "name": "BhccGardenApiKeys",
    "created_date": "April 15, 2025",
    "client_id": "Jr3t1Lgx5LIjDzPKCQ9Y8AUkI27RBjzv",
    "client_secret": "1OgQhAVeFXgwwvPRzJDyY1wE9p6kq3ssnmnXiPRZnd1S1JBnjFloWhqDbQkGkxZd"
}

# IMPORTANT: In a real application, never display or log actual API keys
# Instead, we'll visualize metadata about the keys

# Create hashed versions for visualization
def hash_string(text):
    return hashlib.sha256(text.encode()).hexdigest()[:8]

api_key_data["client_id_hash"] = hash_string(api_key_data["client_id"])
api_key_data["client_secret_hash"] = hash_string(api_key_data["client_secret"])

# Calculate days since creation
created_date = datetime.strptime(api_key_data["created_date"], "%B %d, %Y")
today = datetime.now()
days_active = (today - created_date).days

# Create visualizations
plt.figure(figsize=(12, 8))

# 1. Key Age Visualization
plt.subplot(2, 2, 1)
days = [i for i in range(days_active + 1)]
plt.plot(days, [1] * len(days), marker='o', markersize=10, color='blue')
plt.axvline(x=days_active, color='red', linestyle='--', label='Today')
plt.xlabel('Days Since Creation')
plt.title(f'API Key Age: {days_active} days')
plt.xticks([0, days_active])
plt.yticks([])

# 2. Key Complexity Visualization
plt.subplot(2, 2, 2)
key_lengths = [len(api_key_data["client_id"]), len(api_key_data["client_secret"])]
key_names = ['Client ID', 'Client Secret']
plt.bar(key_names, key_lengths, color=['skyblue', 'lightgreen'])
plt.title('Key Length (Characters)')
plt.ylabel('Length')
for i, v in enumerate(key_lengths):
    plt.text(i, v + 0.5, str(v), ha='center')

# 3. Key Entropy Visualization (simplified)
def estimate_entropy(text):
    # Simple entropy estimation based on unique characters
    unique_chars = len(set(text))
    total_chars = len(text)
    return (unique_chars / total_chars) * 100  # percentage of unique chars

plt.subplot(2, 2, 3)
entropies = [estimate_entropy(api_key_data["client_id"]), 
             estimate_entropy(api_key_data["client_secret"])]
plt.bar(key_names, entropies, color=['coral', 'violet'])
plt.title('Key Character Diversity (%)')
plt.ylabel('Unique Character %')
for i, v in enumerate(entropies):
    plt.text(i, v + 0.5, f'{v:.1f}%', ha='center')

# 4. Key Information Display
plt.subplot(2, 2, 4)
plt.axis('off')
info_text = f"""
API Key: {api_key_data["name"]}
Created: {api_key_data["created_date"]}
Days Active: {days_active}

Client ID: {api_key_data["client_id"][:4]}...{api_key_data["client_id"][-4:]}
(Hash: {api_key_data["client_id_hash"]})

Client Secret: {api_key_data["client_secret"][:4]}...{api_key_data["client_secret"][-4:]}
(Hash: {api_key_data["client_secret_hash"]})
"""
plt.text(0, 0.5, info_text, fontsize=10)

plt.tight_layout()
plt.suptitle("API Key Visualization", fontsize=16)
plt.subplots_adjust(top=0.9)
plt.show()

# If you want to save this data for tracking purposes
# Create a dataframe for historical tracking
historical_data = pd.DataFrame({
    'Key Name': [api_key_data["name"]],
    'Created Date': [api_key_data["created_date"]],
    'Days Active': [days_active],
    'Client ID Hash': [api_key_data["client_id_hash"]],
    'Client Secret Hash': [api_key_data["client_secret_hash"]],
    'Date Checked': [today.strftime("%Y-%m-%d")]
})

print("API Key metadata visualization complete.")
print(f"Key '{api_key_data['name']}' has been active for {days_active} days.")