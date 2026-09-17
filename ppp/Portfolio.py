import os
import time
import pandas as pd
import numpy as np
import tushare as ts

class Portfolio:

    def __init__(self,df1,df2):

        df = pd.merge(df1, df2, on='code', how='left')
        
        self.df = df

    












