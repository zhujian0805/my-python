import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(
    np.random.randn(10, 4),
    index=pd.date_range('1/1/2000', periods=10),
    columns=['Col1', 'Col2', 'Col3', 'Col4'])

df.plot()

plt.show()
