import pandas as pd

# Load distance data
distance_df = pd.read_csv('distances.csv', header=None)
name_df = pd.read_csv('dest_names.csv')

# Fill the upper triangle so that i, j == j, i
for i in range(len(distance_df)):
    for j in range(len(distance_df.columns)):
        if pd.isna(distance_df.iloc[i, j]):
            distance_df.iloc[i, j] = distance_df.iloc[j, i]

# Store addresses
addresses = name_df['Addr'].tolist()

# Convert DataFrame to 2D list
distance_matrix = distance_df.astype(float).values.tolist()

package_df = pd.read_csv('WGUPS Package File.csv')
