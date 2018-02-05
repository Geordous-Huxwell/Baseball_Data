
# coding: utf-8

# Baseball Data
# 
# Data Points to use
# - playerID
# - yearID
# - salary
# - RBI
# - ERA
# - CityID
# 
# Questions to answer
# - median salary over year (line plot)
# - standard deviation of salaries over years (scatterplot)
# - Compare RBI to Salary
# - Compare ERA to salary
# - All time best ERA/RBI combo
# - Mean ERA for Colorado pitchers relative to league average

# In[7]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
get_ipython().magic('pylab inline')

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


# In[8]:


salary_dict = {}
salary_list = []
year = 1985

for row in salary_df.iterrows():
    if row[1][0] == year:
        salary_list.append(row[1][4])        
        salary_dict.update({year:salary_list})
    else:
        salary_list = []
        year += 1
        salary_list.append(row[1][4])        
        salary_dict.update({year:salary_list})
    



# In[9]:


mean_salary_dict = {}
for year in salary_dict:
    mean_salary_dict[year] = mean(salary_dict[year])



# In[89]:


year_salary_df = pd.DataFrame.from_dict(mean_salary_dict, orient='index')
year_salary_df.columns = ["Mean Salaries"]
year_salary_df.plot()


# In[68]:


from easymoney.money import EasyPeasy
ep = EasyPeasy()

normalized_salary_dict = {}

for row in year_salary_df.iterrows():
    year = int(row[0])
    salary = int(row[1])
    normalized_salary = ep.normalize(amount=salary, region="US", from_year=year, to_year="latest", base_currency="USD")
    normalized_salary_dict[year] = normalized_salary
    


# In[88]:



normalized_salary_df = pd.DataFrame.from_dict(normalized_salary_dict, orient='index')
normalized_salary_df.columns = ["Normalized Salaries"]
normalized_salary_df.plot(title="MLB Salaries Normalized to 2016 USD")


# In[90]:


ax = year_salary_df.plot()

normalized_salary_df.plot(ax=ax)


# In[157]:


batter_salary_df = batting_df.merge(salary_df, on=["playerID","yearID","teamID", "lgID"], how="inner")
batter_salary_df = batter_salary_df.drop_duplicates(subset=["playerID"], keep="last")
batter_salary_df = batter_salary_df.dropna(subset=["RBI","salary"], how="any")
batter_salary_df = batter_salary_df[batter_salary_df.RBI!=0]
batter_salary_df = batter_salary_df[batter_salary_df.yearID==2016]
batter_salary_df.plot(kind="scatter", x="RBI", y="salary", title="RBI to Salary Comparison", figsize=(20,20))


# In[155]:


batter_salary_df[batter_salary_df.RBI>=120]


# In[156]:


batter_salary_df[batter_salary_df.salary>=30000000]


# In[159]:


pitcher_salary_df = pitching_df.merge(salary_df, on=["playerID","yearID","teamID", "lgID"], how="inner")
pitcher_salary_df = pitcher_salary_df.drop_duplicates(subset=["playerID"], keep="last")
pitcher_salary_df = pitcher_salary_df.dropna(subset=["ERA","salary"], how="any")
pitcher_salary_df = pitcher_salary_df[pitcher_salary_df.ERA!=0]
pitcher_salary_df = pitcher_salary_df[pitcher_salary_df.yearID==2016]
pitcher_salary_df.plot(kind="scatter", x="ERA", y="salary", title="ERA to Salary Comparison", figsize=(20,20))


# In[161]:


pitcher_salary_df[pitcher_salary_df.ERA>=15]


# In[162]:


pitcher_salary_df[pitcher_salary_df.salary>=30000000]


# In[173]:


ERA_RBI_df = pitching_df.merge(batting_df, on=["playerID","yearID","teamID", "lgID"], how="inner")
ERA_RBI_df = ERA_RBI_df.drop_duplicates(subset=["playerID"], keep="last")
ERA_RBI_df = ERA_RBI_df.dropna(subset=["ERA","RBI"], how="any")
ERA_RBI_df = ERA_RBI_df[ERA_RBI_df.ERA!=0]
ERA_RBI_df.plot(kind="scatter", x="ERA", y="RBI", title="ERA/RBI Combo", figsize=(20,20))


# In[174]:


ERA_RBI_df[ERA_RBI_df.RBI>=110]


# In[175]:


ERA_RBI_df[ERA_RBI_df.ERA>=175]


# In[171]:


max(ERA_RBI_df["ERA"])


# In[180]:


mean_league_ERA = pitching_df["ERA"].mean()
mean_league_ERA


# In[184]:


COL_pitching_df = pitching_df[pitching_df.teamID=="COL"]
mean_COL_ERA = COL_pitching_df["ERA"].mean()
mean_COL_ERA


# In[194]:


ERA_by_team = pitching_df["ERA"].groupby(pitching_df["teamID"])
list(ERA_by_team)


# In[195]:


ERA_by_team.mean()


# In[204]:


team_ERA_normalized = ((ERA_by_team.mean())-(mean_league_ERA))/ERA_by_team.std(ddof=1)
team_ERA_normalized


# In[208]:


COL_ERA_normalized = team_ERA_normalized["COL"]
COL_ERA_normalized


# In[223]:


ordered_normalized_team_ERA = team_ERA_normalized.sort_values()
list(ordered_normalized_team_ERA).index(0.18612622975928425)


# In[224]:


len(ordered_normalized_team_ERA)

