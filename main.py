import pandas as pd
import Classes as cls

# Load distance data
distance_df = pd.read_csv('distances.csv', header=None)
name_df = pd.read_csv('dest_names.csv')

# Fill the upper triangle so that i, j == j, i
rows, cols = distance_df.shape
for i in range(rows):
    for j in range(cols):
        if pd.isna(distance_df.iloc[i, j]):
            if j < rows and i < cols:
                distance_df.iloc[i, j] = distance_df.iloc[j, i]

addresses = name_df['Addr'].tolist()                            # Store addresses
distance_matrix = distance_df.astype(float).values.tolist()     # Convert DataFrame to 2D list
package_df = pd.read_csv('WGUPS Package File.csv')              # Load package data
packages = cls.Hashtable(len(package_df))                       # Initialize hashtable

# Load packages into hashtable
for index, row in package_df.iterrows():
    packages[row['PackageID']] = cls.Package(
        row['PackageID'], row['Address'], row['City'],
        row['Zip'], row['DeliveryDeadline'], row['Weight'],
        notes=row['SpecialNotes']
    )

packages.display()  # Display all packages in the hashtable

# Create a truck object
# ...existing code...