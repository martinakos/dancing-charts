import numpy as np
import plotly.graph_objects as go
import webbrowser
import os

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
        itemdoubleclick=False,
        title=dict(text="<i>Click on dance label to show/hide</i>", font=dict(size=11, color="#888"))
    ),
    title="Dance Complexity: Learning Curves",
    xaxis_title="Hours of Practice",
    yaxis=dict(title="Complexity Level", range=[0, max_y * 1.05], fixedrange=False),
    template="plotly_white",
    hovermode="x unified",
    margin=dict(t=130, r=180, b=40)
)

# Generate preview image for social media sharing
fig.write_image("preview.png", width=1200, height=630, scale=2)

# Get just the chart div (no full HTML wrapper) so we control the page structure
chart_html = fig.to_html(include_plotlyjs=True, full_html=False,
                         config={"responsive": True})

# Build the full page ourselves with chart in a fixed-height container
# This avoids Plotly's height:100% chain that prevents scrolling

index_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="Dance Complexity: Learning Curves">
<meta property="og:description" content="Interactive comparison of learning curves for 15 partner dances — from Merengue to Argentine Tango.">
<meta property="og:image" content="https://martinakos.github.io/dancing-charts/preview.png">
<meta property="og:url" content="https://martinakos.github.io/dancing-charts/">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<title>Dance Complexity: Learning Curves</title>
<style>
html, body { margin: 0; padding: 0; height: auto !important; overflow: auto !important; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #333; line-height: 1.6; }
#chart-container { width: 100%; height: calc(100vh - 80px); margin-bottom: 0; }
#chart-container .plotly-graph-div { height: 100% !important; width: 100% !important; }
#chart-container .js-plotly-plot, #chart-container .plot-container { height: 100% !important; }
</style>
<script data-goatcounter="https://dancing-charts.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<div id="chart-container">
""" + chart_html + """
</div>
<script>
// Resize Plotly chart to fill the container after render
(function() {
    function resizeChart() {
        var container = document.getElementById('chart-container');
        var gd = container.querySelector('.plotly-graph-div');
        if (gd && window.Plotly) {
            Plotly.relayout(gd, { height: container.clientHeight });
        }
    }
    // Run after Plotly renders and on window resize
    setTimeout(resizeChart, 100);
    window.addEventListener('resize', resizeChart);
})();
</script>

<div style="padding: 0 40px 40px 40px;">

<h2 style="border-bottom: 2px solid #ddd; padding-bottom: 8px;">Learning Difficulty Summary</h2>

<div style="overflow-x: auto;">
<table style="width: 100%; border-collapse: collapse; font-size: 14px;">
<thead>
<tr style="background: #f5f5f5;">
    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd; white-space: nowrap;">Dance</th>
    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd; white-space: nowrap;">Entry</th>
    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd; white-space: nowrap;">Shape</th>
    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd; white-space: nowrap;">Ceiling</th>
    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd; white-space: nowrap;">Hours to<br>Social Dance</th>
    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Progression Details</th>
</tr>
</thead>
<tbody>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Merengue</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Easiest</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Fast plateau ~100h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~4.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">5&ndash;10h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Step on every beat &mdash; no complicated footwork. A beginner course takes about an hour. Turn patterns ~30h. Hip movement and styling ~100h. Often used as a &ldquo;gateway dance&rdquo; to salsa and bachata. Advanced merengue involves body rolls and complex turns but the ceiling remains limited.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Modern Jive / Ceroc</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Very easy</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Quick initial, low ceiling</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~5.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">2&ndash;5h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">&ldquo;The simplest of all partner dances.&rdquo; Within half an hour you can be dancing to chart hits. Very little specific footwork; basic 1,2,3,4 count. Build ~1 move per week, solid repertoire by ~50h. Smoothness and styling ~200h. Designed for social enjoyment rather than technical mastery.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Cumbia</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Very easy</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Gentle climb, low ceiling</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~5.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">5&ndash;10h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Basic steps mastered in a couple of hours. Turn patterns ~50h. Depth comes from regional style variations (Colombian vs. Mexican vs. Argentine cumbia) ~200h. Overall technical ceiling is lower than salsa or tango. Often learned alongside salsa in Latin dance communities.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Kizomba</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Easy</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Gentle climb</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~7</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">15&ndash;25h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">One of the most accessible social dances. Slow tempo gives beginners time to think. Basics click within ~20h. Turns and timing variations ~120h. Traditional kizomba has a moderate ceiling; Urban Kiz and Fusion styles significantly raise it with stops, direction changes, and acrobatics (~800h).</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Bachata</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Easy</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Accelerates at body movement phase</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~8</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">20&ndash;30h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Simple side-to-side basic clicks within a few classes. By ~50h, comfortable at socials with basic turns. ~150h: body movement and isolations become the focus (especially sensual bachata). ~500h: musicality and musical interpretation. Ceiling depends on sub-style &mdash; Dominican (fast footwork), Sensual (body waves), or Moderna (complex turn patterns).</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Blues</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Easy start</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Deceptively deep improvisation</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~7.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">15&ndash;25h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">&ldquo;Easy to learn, hard to master.&rdquo; No set patterns &mdash; beginners connect with their partner first (~20h). Movement vocabulary (slow drag, struttin&rsquo;) ~100h. Deceptive depth emerges in musical interpretation across different blues idioms ~350h. Advanced improvisation and micro-leading ~900h.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Cuban Salsa (Casino)</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Easy-moderate</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Rueda phase, then body work</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~8.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">30&ndash;50h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Easier entry than linear salsa &mdash; circular movement is more forgiving. Rueda de Casino (group format) accelerates early learning (~30h). Independent partner dancing ~100&ndash;150h. Deeper phases involve Afro-Cuban body movement, rumba styling, and son elements (~400h). Adds unique group coordination and cultural depth.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Cha-Cha (ballroom/Latin)</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Moderate</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Syllabus progression</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~9</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">20&ndash;30h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">The half-beat &ldquo;cha-cha&rdquo; steps are faster than beginners expect, but the basic pattern is accessible (~35h). Bronze syllabus figures ~150h. The real challenge begins with proper Cuban motion and hip action ~450h. Competitive syllabus (Bronze/Silver/Gold/Open) demands extreme precision.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Salsa (LA/NY)</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Moderate</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Famous intermediate plateau ~200h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~10</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">50&ndash;80h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Basic step and timing (On1 easier than On2) within ~40h. The infamous &ldquo;intermediate plateau&rdquo; hits around 150&ndash;300h &mdash; dancers know patterns but can&rsquo;t connect them fluidly. Breaking through requires musicality, shines, and body movement (~600h). Enormous depth in partner tricks, clave awareness, and improvisation.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Ballroom (Standard)</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Moderate</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Multi-dance, syllabus depth</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~11.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">20&ndash;30h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Social waltz box step is easy, but International slow foxtrot is &ldquo;perhaps the most difficult of all ballroom dances.&rdquo; Basic waltz/foxtrot ~40h. Bronze syllabus ~200h. Silver/Gold requires years of body training ~600h. Structured syllabus (Bronze/Silver/Gold/Open) provides the clearest progression milestones. Posture, body flight, sway, and rise-and-fall refined for decades.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Cali Style Salsa</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Moderate-high</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Fast footwork challenge</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~9.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">50&ndash;80h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Famous for extreme fast footwork using the syncopated &ldquo;repique&rdquo; step. &ldquo;More approachable than it looks&rdquo; but the speed is challenging from the start (~50h). Speed development and basic partner work ~200h. Integration of pachanga, boogaloo, and cumbia influences ~600h. Speed itself creates a persistent challenge at every level.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Brazilian Zouk</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Moderate</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Head movement phase ~500h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~10.5</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">40&ndash;60h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">&ldquo;Beginner&rsquo;s Hell&rdquo; phase involves frustration and fumbling (~50&ndash;100h). Turns and body movement ~200h. The defining feature &mdash; head movements led out of axis &mdash; begins around ~400h and takes years to master safely. Counter-balance techniques and advanced flow at 1200h+. OGs with 10+ years are still developing.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Lindy Hop</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Hard entry</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Swing-out takes years to refine</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~10</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">50&ndash;80h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">The swing-out &mdash; simultaneously the basic and the hardest move. &ldquo;About 5 minutes to learn, about 3 years to do it reasonably well.&rdquo; Charleston variations and tuck turns ~200h. Solo jazz vocabulary and musicality ~600h. Often danced to very fast music. Aerials and personal style development at 1000h+.</td>
</tr>
<tr style="background: #fafafa;">
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">WCS</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Hard entry</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Multi-genre musicality depth</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~11</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">60&ndash;100h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">&ldquo;Arguably the most difficult partner dance to master.&rdquo; Triple steps require strong rhythm sense (~70h). Whips and intermediate patterns ~250h. Uniquely danced to all genres (blues, hip-hop, pop), requiring broad musicality (~600h). Six competitive levels (Newcomer through Champion). Champions are typically full-time professionals.</td>
</tr>
<tr>
    <td style="padding: 10px; border-bottom: 1px solid #eee; font-weight: bold; white-space: nowrap;">Argentine Tango</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">Hardest entry</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">&ldquo;Goes on forever&rdquo;</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~11</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">100&ndash;200h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Steepest entry barrier. &ldquo;It takes 3 months to 1 year before you can be of any use to anybody on the dance floor.&rdquo; Walk, embrace, and lead-follow demanding from day one (~60h). Ochos and molinetes ~250h. Vals/milonga rhythms and floorcraft ~700h. Described as &ldquo;chess compared to a party board game&rdquo; &mdash; essentially infinite refinement.</td>
</tr>
</tbody>
</table>
</div>

<h2 style="border-bottom: 2px solid #ddd; padding-bottom: 8px; margin-top: 40px;">Methodology</h2>

<h3>What is &ldquo;Complexity Level&rdquo;?</h3>
<p>The Complexity Level axis is an <strong>arbitrary synthetic scale</strong> &mdash; it does not correspond to any standardized measurement. It is a constructed score designed to allow <em>relative comparison</em> between dances. The absolute numbers are meaningless; only the relative positions and shapes of the curves matter.</p>

<h3>Data Sources</h3>
<p>The curve parameters were derived from a survey of online resources including:</p>
<ul>
    <li><strong>Dance forums:</strong> Dance-Forums.com, SalsaForums.com, Ask MetaFilter</li>
    <li><strong>Instructor resources:</strong> Arthur Murray (dance progress curve of learning), dance school curriculum descriptions</li>
    <li><strong>Community discussions:</strong> Reddit communities (r/salsa, r/swingdancing, r/ballroom), blog posts from experienced dancers</li>
    <li><strong>Style-specific sources:</strong> ZoukSide Down, SwingLiteracy, Ultimate Tango, Boston Lindy Hop, and others</li>
</ul>
<p>For each dance, information was collected on: how easy/hard it is to start, early learning curve steepness, when plateaus occur, the ultimate complexity ceiling, distinct learning phases and milestones, and consensus opinions from experienced dancers and instructors.</p>

<h3>How the Curves Were Built</h3>
<p>Each curve is modeled as a sum of <strong>logistic sigmoid functions</strong>, one per learning phase:</p>
<p style="font-family: monospace; background: #f5f5f5; padding: 12px; border-radius: 4px;">complexity(h) = floor + &sum; amplitude<sub>i</sub> &times; sigmoid(h, center<sub>i</sub>, steepness<sub>i</sub>)</p>
<p>Where:</p>
<ul>
    <li><strong>Floor value</strong> (entry difficulty): How hard the dance is to <em>start</em>. Based on consistent consensus rankings &mdash; e.g., Argentine Tango and WCS are hardest to begin (floor ~2.5&ndash;3.0), while Merengue and Modern Jive are near-instant (floor ~0.5).</li>
    <li><strong>Sigmoid centers</strong> (phase transitions): Placed at reported milestone timings. For example, &ldquo;Bachata basics click in ~25 hours&rdquo; places a sigmoid at 25h; &ldquo;Salsa intermediate plateau hits around 200 hours&rdquo; places one at 200h.</li>
    <li><strong>Sigmoid amplitudes</strong> (phase magnitudes): How much complexity each phase adds. Larger jumps for phases that unlock significant new skill dimensions (e.g., Brazilian Zouk head movements = 2.5 units); smaller for dances with limited advanced vocabulary (e.g., Merengue&rsquo;s later phases = 0.5 units).</li>
    <li><strong>Ceiling</strong> (sum of floor + all amplitudes): Matched to consensus difficulty rankings from multiple sources.</li>
</ul>

<h3>Caveats</h3>
<ul>
    <li>The absolute numbers are meaningless &mdash; only the <em>relative</em> positions and curve shapes matter for comparison.</li>
    <li>The phase timings are rough averages from anecdotal reports, not controlled studies. No scientific research exists that systematically measures &ldquo;dance complexity&rdquo; over practice hours.</li>
    <li>Different sub-styles within a dance can have very different curves (e.g., Dominican vs. Sensual Bachata; social vs. competitive Ballroom).</li>
    <li>Leader vs. follower progression differs significantly and is not modeled separately.</li>
    <li>Individual learning rates vary enormously based on prior dance experience, natural aptitude, quality of instruction, practice frequency, and other factors.</li>
    <li>The curves model <em>available complexity</em> (what the dance offers to learn), not individual skill level (which depends on the dancer).</li>
</ul>

<p style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; color: #888; font-size: 13px;">Built with Plotly. Curve data compiled from dance community forums, instructor resources, and online discussions (March 2026).</p>

</div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(index_html)

# Open the final index.html in the browser
webbrowser.open("file://" + os.path.realpath("index.html"))