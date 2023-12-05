import pandas as pd

data = {'date': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02'],
        'country': ['USA', 'USA', 'USA', 'Canada'],
        'cases': [100, 200, 150, 250]}

df = pd.DataFrame(data)

pivot_df = df.pivot_table(index='date', columns='country', values='cases', aggfunc='sum')
print(pivot_df)