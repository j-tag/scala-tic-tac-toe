import pandas as pd
import numpy as np
import pickle


def prediction(params, model):
    df = pd.DataFrame(columns=['open', 'high', 'low', 'close',
                               'P_Level Pivot 1H', 'S_Level_1 Pivot 1H', 'S_Level_2 Pivot 1H',
                               'S_Level_3 Pivot 1H', 'S_Level_4 Pivot 1H', 'R_Level_1 Pivot 1H',
                               'R_Level_2 Pivot 1H', 'R_Level_3 Pivot 1H', 'R_Level_4 Pivot 1H',
                               'P_Level Pivot 1D', 'S_Level_1 Pivot 1D', 'S_Level_2 Pivot 1D',
                               'S_Level_3 Pivot 1D', 'S_Level_4 Pivot 1D', 'R_Level_1 Pivot 1D',
                               'R_Level_2 Pivot 1D', 'R_Level_3 Pivot 1D', 'R_Level_4 Pivot 1D',
                               'P_Level Pivot 4H', 'S_Level_1 Pivot 4H', 'S_Level_2 Pivot 4H',
                               'S_Level_3 Pivot 4H', 'S_Level_4 Pivot 4H', 'R_Level_1 Pivot 4H',
                               'R_Level_2 Pivot 4H', 'R_Level_3 Pivot 4H', 'R_Level_4 Pivot 4H',
                               'p 1d_prev', 's1 1d_prev', 's2 1d_prev', 's3 1d_prev', 's4 1d_prev',
                               'r1 1d_prev', 'r2 1d_prev', 'r3 1d_prev', 'r4 1d_prev', 'p 4h_prev',
                               's1 4h_prev', 's2 4h_prev', 's3 4h_prev', 's4 4h_prev', 'r1 4h_prev',
                               'r2 4h_prev', 'r3 4h_prev', 'r4 4h_prev', 'p 1h_prev', 's1 1h_prev',
                               's2 1h_prev', 's3 1h_prev', 's4 1h_prev', 'r1 1h_prev', 'r2 1h_prev',
                               'r3 1h_prev', 'r4 1h_prev', 'buy', 'sell'])
    df.loc[0] = params
    data = np.asarray(df)
    p = model.predict(data)
    return p


'''
Please Enter the parameters according to the following formats :
['open','high','low','close','P_Level Pivot 1H','S_Level_1 Pivot 1H','S_Level_2 Pivot 1H',
                               'S_Level_3 Pivot 1H','S_Level_4 Pivot 1H','R_Level_1 Pivot 1H',
                               'R_Level_2 Pivot 1H','R_Level_3 Pivot 1H','R_Level_4 Pivot 1H',
                               'P_Level Pivot 1D','S_Level_1 Pivot 1D','S_Level_2 Pivot 1D',
                               'S_Level_3 Pivot 1D','S_Level_4 Pivot 1D','R_Level_1 Pivot 1D',
                               'R_Level_2 Pivot 1D','R_Level_3 Pivot 1D','R_Level_4 Pivot 1D',
                               'P_Level Pivot 4H','S_Level_1 Pivot 4H','S_Level_2 Pivot 4H',
                               'S_Level_3 Pivot 4H','S_Level_4 Pivot 4H','R_Level_1 Pivot 4H',
                               'R_Level_2 Pivot 4H','R_Level_3 Pivot 4H','R_Level_4 Pivot 4H',
                               'p 1d_prev','s1 1d_prev','s2 1d_prev','s3 1d_prev','s4 1d_prev',
                               'r1 1d_prev','r2 1d_prev','r3 1d_prev','r4 1d_prev','p 4h_prev',
                               's1 4h_prev','s2 4h_prev','s3 4h_prev','s4 4h_prev','r1 4h_prev',
                               'r2 4h_prev','r3 4h_prev','r4 4h_prev','p 1h_prev','s1 1h_prev',
                               's2 1h_prev','s3 1h_prev','s4 1h_prev','r1 1h_prev','r2 1h_prev',
                               'r3 1h_prev','r4 1h_prev','buy','sell']
'''

### Example : Sample Data
params = [1791.87, 1792.08, 1791.82, 1792.08, 1790.983333, 1790.246667, 1789.283333, 1787.583333,
          1785.883333, 1791.946667, 1792.683333, 1794.383333, 1796.083333, 1789.37, 1782.95,
          1772.7, 1756.03, 1739.36, 1799.62, 1806.04, 1822.71, 1839.38, 1790.946667, 1788.753333,
          1787.296667, 1783.646667, 1779.996667, 1792.403333, 1794.596667, 1798.246667, 1801.896667,
          1789.37, 1782.95, 1772.7, 1756.03, 1739.36, 1799.62, 1806.04, 1822.71, 1839.38, 1790.946667,
          1788.753333, 1787.296667, 1783.646667, 1779.996667, 1792.403333, 1794.596667, 1798.246667,
          1801.896667, 1790.983333, 1790.246667, 1789.283333, 1787.583333, 1785.883333, 1791.946667,
          1792.683333, 1794.383333, 1796.083333, 0, 1]

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
predicted = prediction(params, loaded_model)
print(predicted)
