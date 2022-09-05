import pandas as pd

df = pd.DataFrame([(1,2,3,4,5), (1,2,3,4,5)]).set_index(0)
df.index.names=['Essi']
cols = pd.MultiIndex.from_tuples([('Noi', 'io'), ('Noi', 'tu'), ('Voi', 'tu'), ('Voi', 'altro')])

df.columns = cols
print(df)