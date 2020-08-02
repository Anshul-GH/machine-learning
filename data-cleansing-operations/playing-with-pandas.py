import pandas as pd
import numpy as np

# how panels work
# data = {'Red':pd.DataFrame(np.random.radn(4,2)), 'Blue':pd.DataFrame(np.random.radn(4,3))}
data={'Red':pd.DataFrame(np.random.randn(4,2)),
  'Blue':pd.DataFrame(np.random.randn(4,3))}

print(pd.Panel(data))

'''
FutureWarning: The Panel class is removed from pandas. 
Accessing it from the top-level namespace will also be removed in the next version
'''