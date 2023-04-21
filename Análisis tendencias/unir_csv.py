import pandas as pd

# Lee los dos archivos CSV
df1 = pd.read_csv('data.csv')
df2 = pd.read_csv('spotify_data.csv')

# Concatena los dos archivos en uno solo
df = pd.concat([df1, df2])

# Guarda el archivo resultante como un nuevo archivo CSV
df.to_csv('data1921-2023.csv', index=False)