# ---------------- importing modules ----------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyo
import plotly.graph_objs as go
# ---------------- loading dataset ---------------------
df = pd.read_excel('EPL_Set.xlsx', sheet_name='EPL_Set')
### ------------------- preparing dataframes ----------------
all_cols = ['Season', 'HomeTeam', 'AwayTeam', '1HHG', '1HAG', '1HR', '2HHG', '2HAG',
       '2HR', 'FTHG', 'FTAG', 'FTR', '1HSumGoals', '2HSumGoals', 'FTSumGoals',
       '1HScore', '2HScore', 'FTScore', '2.5', 'Winner', 'BothScored',
       '2.5/Winner', '2.5/BothScored', 'Winner/BothScored', 'Result']
goal_cols = ['1HHG', '1HAG', '1HR', '2HHG', '2HAG',
       '2HR', 'FTHG', 'FTAG', 'FTR']
sum_goals_cols = ['1HSumGoals', '2HSumGoals', 'FTSumGoals']
score_cols = ['1HScore', '2HScore', 'FTScore']
spec_cols = ['2.5', 'Winner', 'BothScored',
        '2.5/Winner', '2.5/BothScored', 'Winner/BothScored', 'Result']

df_sum_goals = df[sum_goals_cols]
first_half_goals = df['1HSumGoals'].value_counts()
sec_half_goals = df['2HSumGoals'].value_counts()
ft_goals = df['FTSumGoals'].value_counts()
#print(first_half_goals, sec_half_goals, ft_goals)

### --------------- visualizations -------------------
score1H = pd.DataFrame(data=df['1HR'].value_counts(sort=False)).T
score2H = pd.DataFrame(data=df['2HR'].value_counts(sort=False)).T
scoreFT = pd.DataFrame(data=df['FTR'].value_counts(sort=False)).T
scores = pd.concat([score1H, score2H, scoreFT], axis=0)
scores.index = ['First half', 'Second half','Full time']

# ------------------ percentage of whole column
scores_perc = scores.copy()
scores_perc['1'] = [round(scores_perc['1'][i]/np.sum(scores_perc['1'])*100, 1) for i in scores_perc.index]
scores_perc['X'] = [round(scores_perc['X'][i]/np.sum(scores_perc['X'])*100, 1) for i in scores_perc.index]
scores_perc['2'] = [round(scores_perc['2'][i]/np.sum(scores_perc['2'])*100, 1) for i in scores_perc.index]

# -------------- plotly visualization --------------------
trace0 = go.Bar(x=scores_perc.index, y=scores_perc['1'],
                name='Home team win', marker=dict(color='green'))
trace1 = go.Bar(x=scores_perc.index, y=scores_perc['X'],
                name='Draw', marker=dict(color='slategrey'))
trace2 = go.Bar(x=scores_perc.index, y=scores_perc['2'],
                name='Away team win', marker=dict(color='blue'))

data = [trace0, trace1, trace2]
layout = go.Layout(title='Scores', yaxis=dict(title='%'), barmode=None)
layout1 = go.Layout(title='Scores', yaxis=dict(title='%'), barmode='stack')
fig = go.Figure(data=data, layout=layout)
fig1 = go.Figure(data=data, layout=layout1)
pyo.plot(fig, filename="Scores_nested.html", auto_open=True)
pyo.plot(fig1, filename='Scores_stacked.html', auto_open=True)
# ----------------------- saving dataframes -----------------
df.to_excel('EPL_df.xlsx', sheet_name='Dataframe')
df.to_csv('EPL_df.csv', sep=',')
scores.to_csv('scores.csv', sep=',')
scores_perc.to_csv('scores_perc.csv', sep=',')

d = pd.read_csv('EPL_Set.csv')
d.to_csv('EPL_Set.csv',sep=',')
