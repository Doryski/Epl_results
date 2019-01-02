# ---------------- importing modules ----------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyo
import plotly.graph_objs as go
plt.style.use('ggplot')
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
                name='Home team win', marker=dict(color='green'), width=0.25)
trace1 = go.Bar(x=scores_perc.index, y=scores_perc['X'],
                name='Draw', marker=dict(color='grey'), width=0.25)
trace2 = go.Bar(x=scores_perc.index, y=scores_perc['2'],
                name='Away team win', marker=dict(color='blue'), width=0.25)
data = [trace0, trace1, trace2]
layout = go.Layout(title='Scores', yaxis=dict(title='%'), barmode=None)
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="Scores_nested.html", auto_open=True)

# ------------------- heatmap full time goals ------------------
df_heatmap = pd.pivot_table(data=df, index='FTHG',columns='FTAG',values='FTR', aggfunc=lambda x: round(x.count()/len(df)*100, 1), fill_value=0.0)
ax = sns.heatmap(data=df_heatmap, cmap='Blues', linecolor="white", linewidths=.5, annot=True, fmt='.1f')
ax.set_title('Full time goals distribution percentage', pad=35, fontdict=dict(fontsize=14))
ax.set_xlabel('Away team goals')
ax.set_ylabel('Home team goals')
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
plt.tight_layout()
plt.savefig('Goals_distribution_heatmap',bbox_inches='tight')
plt.show()
# ------------------- line plot full time scores ---------------
result = pd.DataFrame(data=df['Result'].value_counts())
result1 = result[result > 0.01*result.sum()].dropna()
result2 = result[result < 0.01*result.sum()].dropna().apply('sum')
result3 = pd.DataFrame(index=['Rest'], data=result2['Result'], columns=['Result'])
result1 = result1.append(result3).apply(lambda x: round(x/result1['Result'].sum()*100, 1))
data = [go.Scatter(x=result1.index, y=result1['Result'], marker=dict(color='blue', size=10),
                    line=dict(color='grey', width=3), name='Percentage of all results', showlegend=True)]
layout = go.Layout(title='Results\' distribution', yaxis=dict(title='%'), legend=dict(x=0.8, y=0.95))
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="Results_dist.html", auto_open=True)
# -------------- violin plot distribution of goals' sums --------------
df_sum_goals = df[sum_goals_cols]
df_sum_goals = df_sum_goals.apply(lambda x: x.value_counts(sort=False)).fillna(0).astype(int)
df_sum_goals = df_sum_goals.apply(lambda x: round(x/len(df)*100, 1))
trace0 = go.Bar(x=df_sum_goals.index, y=df_sum_goals['1HSumGoals'], name='First half goals', marker=dict(color='green'))
trace1 = go.Bar(x=df_sum_goals.index, y=df_sum_goals['2HSumGoals'], name='Second half goals', marker=dict(color='blue'))
trace2 = go.Bar(x=df_sum_goals.index, y=df_sum_goals['FTSumGoals'], name='Full time goals', marker=dict(color='grey'))
data = [trace0, trace1, trace2]
layout = go.Layout(title='Sum of goals distribution', yaxis=dict(title='%'), legend=dict(x=0.8, y=0.95))
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename="Sum_goals_dist.html", auto_open=True)
# ----------------------- bar plot sums of goals -----------------
result_comparison = pd.DataFrame(df['HalfTvsFullT'].value_counts())
result_comparison = result_comparison.apply(lambda x: round(x/len(df)*100,1))
import squarify
x = 0.
y = 0.
width = 100.
height = 100.
values = result_comparison['HalfTvsFullT']
color_brewer = ['blue','blue','blue','green','green','green','green', 'grey', 'grey']
normed = squarify.normalize_sizes(values, width, height)
rects = squarify.squarify(normed, x, y, width, height)
shapes = []
annotations = []
counter = 0

for r in rects:
    shapes.append(
        dict(
            type = 'rect',
            x0 = r['x'],
            y0 = r['y'],
            x1 = r['x']+r['dx'],
            y1 = r['y']+r['dy'],
            line = dict(width=2, color='white'),
            fillcolor = color_brewer[counter]
        )
    )
    annotations.append(
        dict(
            x = r['x']+(r['dx']/2),
            y = r['y']+(r['dy']/2),
            text = values.index[counter] + ': ' + str(values[counter]) + '%',
            showarrow = False,
            font = dict(
                color = "black",
                size = 12
        )
    ))
    counter = counter + 1
    if counter >= len(color_brewer):
        counter = 0
trace0 = go.Scatter(
    x = [ r['x']+(r['dx']/2) for r in rects ],
    y = [ r['y']+(r['dy']/2) for r in rects ]
)

layout = go.Layout(
    height=700,
    width=700,
    xaxis=dict(showgrid=False,zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False,zeroline=False, showticklabels=False),
    shapes=shapes,
    annotations=annotations,
    hovermode='closest', title='Half time result vs Full time result distribution'
)

# With hovertext
fig = dict(data=[trace0], layout=layout)
pyo.plot(fig, filename="Half_goals.html", auto_open=True)
# ----------------------- saving dataframes -----------------
df.to_excel('EPL_df.xlsx', sheet_name='Dataframe')
df.to_csv('EPL_df.csv', index=False)
scores.to_csv('scores.csv')
scores_perc.to_csv('scores_dist.csv')
df_sum_goals.to_csv('sum_goals_dist.csv')
