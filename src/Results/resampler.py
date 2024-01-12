import pandas as pd

# Load the Excel file
df = pd.read_excel('Resample.xlsx')

# Combine 'DATUM' and 'ČAS' into a single datetime column
df['datetime'] = pd.to_datetime(df['DATUM'].astype(str) + ' ' + df['ČAS'].astype(str))

# Set the new datetime column as the index
df.set_index('datetime', inplace=True)

# Resample to one-minute intervals and average the 'Vykon L1' values
df_resampled = df['zona 1'].resample('1T').mean()

# Reset the index if you want 'datetime' back as a column
df_resampled = df_resampled.reset_index()

# Save to a new Excel file in the same directory
df_resampled.to_excel('normalized_data.xlsx', index=False)