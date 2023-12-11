import pandas as pd

# Load the CSV file to inspect its structure
file_path = "./natural_spikes_drawdowns.csv"
data = pd.read_csv(file_path)

# Display the first few rows of the DataFrame to understand its structure
data.head()

# Extracting the first three letters from the "symbol" column
data["symbol"] = data["symbol"].str[:3]

# Extracting date and hour from the "timestamp" column
data["timestamp"] = pd.to_datetime(data["timestamp"])
data["date"] = data["timestamp"].dt.date
data["hour"] = data["timestamp"].dt.strftime("%H:%M")

# Adding the "exchange" column with the value "binance"
data["exchange"] = "binance"

# Selecting the required columns
new_data = data[["symbol", "date", "hour", "exchange"]]

# Saving the new DataFrame to a CSV file
new_file_path = "./transformed.csv"
new_data.to_csv(new_file_path, index=False)
