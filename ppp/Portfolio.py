import os
import time
import pandas as pd
import numpy as np
import tushare as ts

class Portfolio:

    def __init__(self,df1,df2):

        df = pd.merge(df1, df2, on='code', how='left')
        
        self.df = df
    
    @staticmethod
    def return_market_value(book):
        return (book.hold_vol * book.close).sum()
    @staticmethod
    def return_market_value_pre(book):
        return (book.hold_vol * book.pre_close).sum()
    @staticmethod
    def return_gain_by_pre_close(book):
        return ((book['close'] - book['pre_close']) * book['hold_vol']).sum()
    @staticmethod
    def return_gain_by_diff(book):
        return (book.hold_vol * book.close).sum()-(book.hold_vol * book.pre_close).sum()
    @staticmethod
    def return_gain_by_change(book):
        return (book.hold_vol * book.change).sum()  
    @staticmethod
    def return_ret_pct(book):
        return ((book.hold_vol * book.change).sum())/(book.hold_vol * book.pre_close).sum()*100

    
    












