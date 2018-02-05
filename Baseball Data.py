from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
##import seaborn as sns
##%pylab inline

filepath = "C:\Python27\Data\Baseball Data"
batting_file = '\Batting.csv'
pitching_file = '\Pitching.csv'
salary_file = '\Salaries.csv'

batting_df = pd.read_csv(filepath+batting_file)
pitching_df = pd.read_csv(filepath+pitching_file)
salary_df = pd.read_csv(filepath+salary_file)

batting_df.fillna(0)
pitching_df.fillna(0)
salary_df.fillna(0)

salary_dict = {}
salary_list = []
year = 1985

for row in salary_df.iterrows():
    if row[1][0] == year: 
        salary_list.append(row[1][4])
    salary_dict[year] = salary_list
    salary_list = []
    year += 1

print salary_dict
