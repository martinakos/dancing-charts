import numpy as np
import plotly.graph_objects as go

x = np.linspace(0, 2000, 400)

def sigmoid(x, center, steepness):
    """Logistic sigmoid: 0->1 transition centered at 'center' hours."""
    return 1 / (1 + np.exp(-steepness * (x - center)))

# Each dance modeled with: floor + phase1 + phase2 + ... using sigmoids
# Parameters based on research: entry difficulty, plateau timings, ceiling
dances_data = [
    # Bachata: easy start (2), quick basics (50h), body movement phase (200h),
    # musicality (500h), ceiling ~7
    ("Bachata", lambda x:
        1.0
        + 1.5 * sigmoid(x, 25, 0.08)     # basics click fast
        + 2.0 * sigmoid(x, 150, 0.012)    # turn patterns + body movement
        + 2.0 * sigmoid(x, 500, 0.005)    # musicality + styling
        + 1.5 * sigmoid(x, 1200, 0.003)   # sub-style mastery
    ),

    # Salsa LA/NY: moderate start, infamous intermediate plateau ~200h, high ceiling ~9
    ("Salsa (LA/NY)", lambda x:
        1.5
        + 2.0 * sigmoid(x, 40, 0.06)      # basic step + timing
        + 2.0 * sigmoid(x, 200, 0.008)    # patterns (intermediate plateau here)
        + 2.5 * sigmoid(x, 600, 0.004)    # musicality + shines + body
        + 2.0 * sigmoid(x, 1500, 0.002)   # improvisation mastery
    ),

    # Cuban Salsa: easier entry than linear, moderate ceiling ~7.5
    ("Cuban Salsa (Casino)", lambda x:
        1.0
        + 2.0 * sigmoid(x, 30, 0.07)      # rueda basics, forgiving circular motion
        + 2.0 * sigmoid(x, 150, 0.01)     # social partner dancing without calls
        + 2.0 * sigmoid(x, 400, 0.005)    # Afro-Cuban body movement
        + 1.5 * sigmoid(x, 1000, 0.003)   # son montuno, improvisation
    ),

    # Argentine Tango: highest entry barrier, steepest overall, ceiling ~10
    ("Argentine Tango", lambda x:
        3.0
        + 1.5 * sigmoid(x, 60, 0.04)      # walk + embrace (slow to click)
        + 2.0 * sigmoid(x, 250, 0.006)    # ochos, molinetes, basic musicality
        + 2.0 * sigmoid(x, 700, 0.004)    # vals/milonga, floorcraft
        + 2.5 * sigmoid(x, 1500, 0.002)   # nuanced expression, infinite depth
    ),

    # Lindy Hop: high entry (swing-out is hard), high ceiling ~8.5
    ("Lindy Hop", lambda x:
        2.5
        + 2.0 * sigmoid(x, 60, 0.04)      # swing-out basics
        + 2.0 * sigmoid(x, 250, 0.007)    # Charleston, tuck turns
        + 2.0 * sigmoid(x, 600, 0.004)    # solo jazz, musicality
        + 1.5 * sigmoid(x, 1300, 0.002)   # personal style, aerials
    ),

    # Kizomba: very easy entry, moderate ceiling ~6
    ("Kizomba", lambda x:
        0.8
        + 2.0 * sigmoid(x, 20, 0.1)       # basics click very fast
        + 1.5 * sigmoid(x, 120, 0.012)    # turns, timing variations
        + 1.5 * sigmoid(x, 350, 0.005)    # musicality, tarraxinha
        + 1.2 * sigmoid(x, 800, 0.003)    # urban kiz / fusion
    ),

    # Brazilian Zouk: moderate entry, "beginner's hell" ~100h, very high ceiling ~9
    ("Brazilian Zouk", lambda x:
        2.0
        + 1.5 * sigmoid(x, 50, 0.04)      # basic step + connection
        + 2.0 * sigmoid(x, 200, 0.008)    # turns, body movement
        + 2.5 * sigmoid(x, 500, 0.004)    # head movements (big phase)
        + 2.5 * sigmoid(x, 1200, 0.002)   # counter-balance, advanced flow
    ),

    # West Coast Swing: hard entry, very high ceiling ~9.5
    ("West Coast Swing", lambda x:
        2.5
        + 1.5 * sigmoid(x, 70, 0.035)     # basics are hardest of any dance
        + 2.0 * sigmoid(x, 250, 0.007)    # whips, intermediate patterns
        + 2.5 * sigmoid(x, 600, 0.004)    # musical interpretation across genres
        + 2.5 * sigmoid(x, 1400, 0.002)   # champion-level improvisation
    ),

    # Cha-Cha: moderate entry, high ceiling in competition ~8
    ("Cha-Cha (ballroom/Latin)", lambda x:
        1.5
        + 2.0 * sigmoid(x, 35, 0.06)      # basic pattern + timing
        + 2.0 * sigmoid(x, 150, 0.01)     # bronze figures
        + 2.0 * sigmoid(x, 450, 0.005)    # Cuban motion, styling
        + 1.5 * sigmoid(x, 1000, 0.003)   # silver/gold, competition
    ),

    # Modern Jive: easiest entry, lowest ceiling ~4.5
    ("Modern Jive / Ceroc", lambda x:
        0.5
        + 2.0 * sigmoid(x, 5, 0.3)        # dancing within half an hour
        + 1.5 * sigmoid(x, 50, 0.03)      # building repertoire
        + 1.0 * sigmoid(x, 200, 0.008)    # smoothness + styling
        + 0.5 * sigmoid(x, 600, 0.003)    # advanced moves, limited ceiling
    ),

    # Merengue: easiest start, lowest ceiling ~3.5
    ("Merengue", lambda x:
        0.5
        + 1.5 * sigmoid(x, 5, 0.4)        # marching basic, instant
        + 1.0 * sigmoid(x, 30, 0.05)      # turn patterns
        + 1.0 * sigmoid(x, 100, 0.015)    # hip action, body movement
        + 0.5 * sigmoid(x, 300, 0.005)    # limited advanced vocabulary
    ),

    # Cumbia: very easy, low-moderate ceiling ~4.5
    ("Cumbia", lambda x:
        0.8
        + 1.5 * sigmoid(x, 8, 0.2)        # basic step, fast pickup
        + 1.5 * sigmoid(x, 50, 0.03)      # turn patterns
        + 1.0 * sigmoid(x, 200, 0.008)    # regional style variations
        + 0.7 * sigmoid(x, 500, 0.004)    # advanced partner connection
    ),

    # Blues: easy entry, deceptively deep, moderate-high ceiling ~7
    ("Blues", lambda x:
        1.0
        + 1.5 * sigmoid(x, 20, 0.08)      # close embrace, pulse
        + 1.5 * sigmoid(x, 100, 0.015)    # movement vocabulary
        + 2.0 * sigmoid(x, 350, 0.005)    # musical interpretation
        + 1.5 * sigmoid(x, 900, 0.003)    # deep improvisation, micro-leading
    ),

    # Cali Style Salsa: moderate-high entry (fast footwork), high ceiling ~8
    ("Cali Style Salsa", lambda x:
        2.0
        + 2.0 * sigmoid(x, 50, 0.04)      # basic repique patterns
        + 2.0 * sigmoid(x, 200, 0.008)    # speed development
        + 2.0 * sigmoid(x, 600, 0.004)    # pachanga + boogaloo integration
        + 1.5 * sigmoid(x, 1300, 0.002)   # high-speed synchronization
    ),

    # Ballroom Standard: moderate social entry, very high competitive ceiling ~9.5
    # Sinusoidal component represents the multi-dance challenge (waltz/foxtrot/quickstep)
    ("Ballroom (Standard)", lambda x:
        2.0
        + 2.0 * sigmoid(x, 40, 0.05)      # basic waltz/foxtrot
        + 2.0 * sigmoid(x, 200, 0.007)    # bronze syllabus
        + 2.5 * sigmoid(x, 600, 0.004)    # silver/gold, body mechanics
        + 2.5 * sigmoid(x, 1500, 0.002)   # open choreography, championship
        + 0.4 * np.sin(x / 80)            # multi-dance complexity oscillation
    ),
]

colors = [
    "#E6194B", "#3CB44B", "#FFE119", "#4363D8", "#F58231",
    "#911EB4", "#42D4F4", "#F032E6", "#BFEF45", "#FABEBE",
    "#469990", "#E6BEFF", "#9A6324", "#000080", "#800000"
]

fig = go.Figure()

num_dances = len(dances_data)

# Compute max Y across all dances for fixed axis range
max_y = max(np.max(func(x)) for _, func in dances_data)

for i, (name, func) in enumerate(dances_data):
    y = func(x)
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=name,
        line=dict(color=colors[i], width=1.2),
        hoverinfo="x+y+name",
        visible=True
    ))

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            showactive=False,
            x=0.5,
            xanchor="center",
            y=1.18,
            yanchor="top",
            font=dict(size=12),
            buttons=[
                dict(label="Show all",
                     method="restyle",
                     args=[{"visible": [True] * num_dances}]),
                dict(label="Clear all",
                     method="restyle",
                     args=[{"visible": ["legendonly"] * num_dances}]),
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
    yaxis=dict(title="Complexity Level", range=[0, max_y * 1.05], fixedrange=False),
    template="plotly_white",
    hovermode="x unified",
    margin=dict(t=130, r=180)
)

fig.show()
fig.write_html("index.html", include_plotlyjs=True, full_html=True,
               config={"responsive": True})

# Inject viewport meta tag and legend click handler directly into HTML
with open("index.html", "r") as f:
    html = f.read()

html = html.replace("<head>",
    '<head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
    '<style>body { margin: 0; overflow: hidden; }</style>')

fullscreen_script = """
<script>
(function() {
    var gd = document.getElementsByClassName('plotly-graph-div')[0];
    if (gd) {
        gd.style.width = '100vw';
        gd.style.height = '100vh';
        window.addEventListener('resize', function() { Plotly.Plots.resize(gd); });
        Plotly.Plots.resize(gd);
    }
})();
</script>
"""

html = html.replace("</body>", fullscreen_script + "</body>")

with open("index.html", "w") as f:
    f.write(html)