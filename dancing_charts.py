import numpy as np
import plotly.graph_objects as go

x = np.linspace(0, 2000, 400)

dances_data = [
    ("Bachata", lambda x: 2 + 0.004*x + 0.000003*x**2),
    ("Salsa (LA/NY)", lambda x: 4 + 0.0035*x + 0.000002*x**2),
    ("Cuban Salsa (Casino)", lambda x: 4 + 0.002*x + 0.0000005*x**2),
    ("Argentine Tango", lambda x: 6 + 0.0015*x + 0.000004*x**2),
    ("Lindy Hop", lambda x: 5 + 0.003*x + 0.000002*x**2),
    ("Kizomba", lambda x: 3 + 0.0025*x + 0.000001*x**2),
    ("Brazilian Zouk", lambda x: 3 + 0.003*x + 0.000003*x**2),
    ("West Coast Swing", lambda x: 4 + 0.003*x + 0.0000025*x**2),
    ("Cha-Cha (ballroom/Latin)", lambda x: 4 + 0.0025*x + 0.000002*x**2),
    ("Modern Jive / Ceroc", lambda x: 3 + 0.0018*x + 0.0000008*x**2),
    ("Merengue", lambda x: 1.5 + 4 * (1 - np.exp(-x/300))),
    ("Cumbia", lambda x: 3 + 0.0022*x + 0.0000006*x**2),
    ("Blues", lambda x: 2 + 0.002*x + 0.000002*x**2),
    ("Cali Style Salsa", lambda x: 5 + 0.004*x + 0.000003*x**2),
    ("Ballroom (Standard)", lambda x: 5.5 + 0.002*x + 0.000004*x**2 + 1.2*np.sin(x/80))
]

colors = [
    "#E6194B", "#3CB44B", "#FFE119", "#4363D8", "#F58231",
    "#911EB4", "#42D4F4", "#F032E6", "#BFEF45", "#FABEBE",
    "#469990", "#E6BEFF", "#9A6324", "#000080", "#800000"
]

fig = go.Figure()

# To fix the interaction while keeping a clean legend, we'll use actual traces 
# for "Show all" and "Clear all" but link them to a custom JS-like behavior 
# through Plotly's updatemenu buttons, but styled as labels.

for i, (name, func) in enumerate(dances_data):
    y = func(x)
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=name,
        line=dict(color=colors[i], width=1.2), # Thinner lines
        hoverinfo="x+y+name",
        visible=True
    ))

# This is the single, working column menu. No redundant buttons.
# Positioned exactly where the legend headers would be.
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            showactive=False,
            x=1.02, 
            xanchor="left",
            y=1.0, 
            yanchor="top",
            pad={"t": 0, "b": 0},
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(size=14, color="black"),
            buttons=[
                dict(label="Show all",
                     method="restyle",
                     args=[{"visible": [True] * len(dances_data)}]),
                dict(label="Clear all",
                     method="restyle",
                     args=[{"visible": ["legendonly"] * len(dances_data)}]),
            ]
        )
    ],
    legend=dict(
        y=0.9,
        yanchor="top",
        itemclick="toggle",
        itemdoubleclick=False
    ),
    title="Dance Complexity Tool",
    xaxis_title="Hours of Practice",
    yaxis_title="Complexity Level",
    template="plotly_white",
    hovermode="x unified",
    margin=dict(t=100, r=180)
)

fig.show()
fig.write_html("index.html", include_plotlyjs=True, full_html=True,
               config={"responsive": True},
               post_script="""
var gd = document.getElementsByClassName('plotly-graph-div')[0];
gd.style.width = '100vw';
gd.style.height = '100vh';
window.addEventListener('resize', function() { Plotly.Plots.resize(gd); });
Plotly.Plots.resize(gd);
""")

# Inject viewport meta tag for mobile
with open("index.html", "r") as f:
    html = f.read()
html = html.replace("<head>",
    '<head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
    '<style>body { margin: 0; overflow: hidden; }</style>')
with open("index.html", "w") as f:
    f.write(html)