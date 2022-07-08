import plotly.graph_objects as go

# Create random data with numpy
import numpy as np
np.random.seed(1)

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

# Create traces
fig = go.Figure()

fig.add_trace(go.Scatter(x=random_x, y=random_y0,
                    mode='lines', # Line plot만 그리기
                    line=dict(color='firebrick', width=4),
                    name='lines'))
fig.add_trace(go.Scatter(x=random_x, y=random_y1,
                    mode='lines+markers', # Line Plot에 마커찍기
                    line=dict(color='royalblue', width=2),
                    name='lines+markers'))
fig.add_trace(go.Scatter(x=random_x, y=random_y2,
                    mode='markers', # 마커만 찍기
                    name='markers'))

fig.update_layout(title='Random Data Python Plot',
                   xaxis_title='random x',
                   yaxis_title='random y')

fig.show()