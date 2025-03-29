import sqlite3
import pandas as pd

# Load CSV file
file_path = "updated_listener_data.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Check and rename columns if needed
df.columns = df.columns.str.strip()  # Remove spaces in column names
df.rename(columns={
    "Listener ID": "listener_id",        # Change based on actual CSV column names
    "Listener Name": "listener_name",
    "Listener Type": "listener_type",
    "Status": "status"
}, inplace=True)

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Insert data into the database
for _, row in df.iterrows():
    cursor.execute("INSERT INTO app_team_listeners (listener_id, listener_name, listener_type, listener_status) VALUES (?, ?, ?, ?)",
                   (row["listener_id"], row["listener_name"], row["listener_type"], row["status"]))

conn.commit()
print(f"{len(df)} records inserted into app_team_listeners.")

# Close connection
conn.close()


