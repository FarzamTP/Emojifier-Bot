import pandas as pd

data = pd.DataFrame(columns=['Text', 'Predicted', 'Impression', 'Label'])

data.loc[0] = (['Hey', 3, 0, 2])

data = data.append(d)

print(data)