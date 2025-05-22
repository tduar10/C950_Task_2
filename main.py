import pandas as pd
import Classes as cls

# Load distance data
distance_df = pd.read_csv('distances.csv', header=None)
name_df = pd.read_csv('dest_names.csv')

# Fill the upper triangle so that i, j == j, i
for i in range(len(distance_df)):
    for j in range(len(distance_df.columns)):
        if pd.isna(distance_df.iloc[i, j]):
            distance_df.iloc[i, j] = distance_df.iloc[j, i]

addresses = name_df['Addr'].tolist()                            # Store addresses
distance_matrix = distance_df.astype(float).values.tolist()     # Convert DataFrame to 2D list
package_df = pd.read_csv('WGUPS Package File.csv')				# Load package data
packages = cls.Hashtable(len(pacakge_df))						# Initialize hashtable

# Load packages into hashtable
for index, row in package_df:
    packages[row[PackageID]] = cls.Package(row[PackageID], row[Address], row[City],	row[Zip], row[DeliveryDeadline], row[Weight], notes=row[SpecialNotes])


        

