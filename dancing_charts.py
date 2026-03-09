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
    # Bachata: easy start, quick basics (25h), body movement (150h),
    # musicality across derecho/majao/mambo sections (500h),
    # multi-style fusion mastery — Dominican footwork + Sensual body waves +
    # Moderna turns, switching within a single song (1200h). Ceiling ~9
    ("Bachata", lambda x:
        1.0
        + 1.5 * sigmoid(x, 25, 0.08)     # basics click fast
        + 2.0 * sigmoid(x, 150, 0.012)    # turn patterns + body movement
        + 2.5 * sigmoid(x, 500, 0.005)    # musicality + styling (derecho/majao/mambo)
        + 2.0 * sigmoid(x, 1200, 0.003)   # multi-style fusion (Dominican/Sensual/Moderna)
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
    # Multi-dance learning (waltz/foxtrot/quickstep/VW/tango) slows progression but
    # complexity never decreases — removed sinusoidal oscillation (unsupported by sources)
    ("Ballroom (Standard)", lambda x:
        2.0
        + 2.0 * sigmoid(x, 40, 0.05)      # basic waltz/foxtrot
        + 2.0 * sigmoid(x, 200, 0.007)    # bronze syllabus
        + 2.5 * sigmoid(x, 600, 0.004)    # silver/gold, body mechanics
        + 2.5 * sigmoid(x, 1500, 0.002)   # open choreography, championship
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
    title=dict(text="Dance Complexity: Learning Curves", font=dict(size=28)),
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
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">~9</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">20&ndash;30h</td>
    <td style="padding: 10px; border-bottom: 1px solid #eee;">Simple side-to-side basic clicks within a few classes. By ~50h, comfortable at socials with basic turns. ~150h: body movement and isolations become the focus (especially sensual bachata). ~500h: musicality across song sections (derecho, majao, mambo) each demanding different movement. ~1200h: multi-style fusion mastery &mdash; modern social dancing requires switching between Dominican (fast footwork), Sensual (body waves), and Moderna (complex turn patterns) within a single song.</td>
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

<h2 style="border-bottom: 2px solid #ddd; padding-bottom: 8px; margin-top: 40px;">References</h2>
<p>The following sources were consulted to determine learning phases, milestone timings, entry difficulty, and complexity ceilings for each dance. Where a source informed multiple dances, it is listed under the primary dance it was used for.</p>

<h3>General &amp; Cross-Dance</h3>
<ul>
    <li><a href="https://blog.arthurmurraylive.com/arthur-murray-curve-of-learning" target="_blank">Arthur Murray &mdash; Dance Progress Explained: The Curve of Learning</a> &mdash; four stages of dance learning; plateau descriptions; general ballroom progression timelines.</li>
    <li><a href="https://dancelouisville.com/how-many-lessons-to-learn-to-dance/" target="_blank">Dance Louisville &mdash; Learning to Ballroom Dance: How Long Does It Take?</a> &mdash; 10-hour breakthrough, 20-hour functional dancing milestone.</li>
    <li><a href="https://ask.metafilter.com/123017/What-is-the-most-difficult-social-dance" target="_blank">Ask MetaFilter &mdash; What Is the Most Difficult Social Dance?</a> &mdash; community ranking of partner dance difficulty; relative difficulty changes with proficiency level.</li>
    <li><a href="https://www.watchmojo.com/articles/top-10-hardest-partner-dances-to-pull-off" target="_blank">WatchMojo &mdash; Top 10 Hardest Partner Dances to Pull Off</a> &mdash; cross-dance difficulty ranking with Argentine Tango at the top.</li>
</ul>

<h3>Bachata</h3>
<ul>
    <li><a href="https://bachataonlinecourse.com/how-long-does-it-take-to-learn-bachata-a-timeline-for-beginners/" target="_blank">Bachata Online &mdash; How Long Does It Take to Learn Bachata?</a> &mdash; beginner timeline, basics in a few weeks, body movement phase, first-year milestones.</li>
    <li><a href="https://sensualmovementusa.com/how-to-dance-bachata/" target="_blank">Sensual Movement USA &mdash; How to Dance Bachata: A Beginner&rsquo;s Guide</a> &mdash; sensual bachata body movement progression.</li>
    <li><a href="https://www.classpop.com/magazine/how-to-dance-bachata" target="_blank">Classpop &mdash; How to Dance Bachata (2025 Guide)</a> &mdash; structured learning timeline and sub-style descriptions.</li>
    <li><a href="https://www.jettence.com/blog/bachata-styles-and-why-you-should-learn-them-all/" target="_blank">Jettence &mdash; Different Bachata Styles and Why You Should Learn Them All</a> &mdash; multi-style switching expected at socials; &ldquo;inappropriate to dance sensual when Dominican music is playing&rdquo;; Urbana/Moderna described as &ldquo;very demanding.&rdquo;</li>
    <li><a href="https://www.djvampbachata.com/open-level-listening-comprehension" target="_blank">DJ Vamp &mdash; Principles of Bachata Music</a> &mdash; derecho/majao/mambo song sections; each polyrhythm requires different dance approach.</li>
    <li><a href="https://www.fortheloveofbachata.com/blog-1/bachatastyles" target="_blank">For the Love of Bachata &mdash; Bachata Styles Breakdown</a> &mdash; Dominican, Moderna, Sensual style definitions and fusion complexity.</li>
</ul>

<h3>Salsa (LA/NY)</h3>
<ul>
    <li><a href="https://www.salsaforums.com/threads/how-long-have-you-considered-yourself-beginner-intermediate-advanced-other-milestones.19249/" target="_blank">SalsaForums &mdash; How Long Have You Considered Yourself Beginner/Intermediate/Advanced?</a> &mdash; dancer self-reports on progression timelines; intermediate plateau experiences.</li>
    <li><a href="https://rfdance.com/blog/how-long-does-it-take-to-learn-salsa-timelines-tips/" target="_blank">RF Dance &mdash; How Long Does It Take to Learn Salsa? Timelines &amp; Tips</a> &mdash; beginner to intermediate timeline (1&ndash;2 years with regular practice).</li>
    <li><a href="https://www.dance-forums.com/threads/how-long-did-it-take-you-to-learn-salsa.5757/" target="_blank">Dance-Forums.com &mdash; How Long Did It Take You to Learn Salsa?</a> &mdash; community timelines; plateau at 6&ndash;7 months; breakthrough after social dancing.</li>
    <li><a href="https://www.moversandshakersdance.com/how-long-does-it-take-to-get-good-at-salsa" target="_blank">Movers &amp; Shakers &mdash; How Long Does It Take to Get Good at Salsa?</a> &mdash; stage-by-stage progression.</li>
</ul>

<h3>Cuban Salsa (Casino)</h3>
<ul>
    <li><a href="https://www.dancelifemap.com/cuban-salsa-how-it-differs-from-linear-salsa-styles/" target="_blank">DanceLifeMap &mdash; Cuban Salsa: How It Differs from Linear Salsa Styles</a> &mdash; easier entry than linear salsa; circular movement more forgiving; simpler footwork.</li>
    <li><a href="https://thedancedojo.com/salsa-dance-terms/cuban-salsa-cubana/" target="_blank">The Dance Dojo &mdash; Cuban Salsa (Salsa Cubana): Casino &amp; Rueda de Casino</a> &mdash; rueda format, Afro-Cuban influences.</li>
    <li><a href="https://www.salsaforums.com/threads/learning-rueda-casino-cuban-salsa-trouble-leading-though-when-social-dancing.42781/" target="_blank">SalsaForums &mdash; Learning Rueda Casino / Cuban Salsa</a> &mdash; transition from rueda to social partner dancing challenges.</li>
</ul>

<h3>Argentine Tango</h3>
<ul>
    <li><a href="https://www.ultimatetango.com/blog/beyond-steps-the-true-journey-of-learning-argentine-tango" target="_blank">Ultimate Tango &mdash; Beyond Steps: The True Journey of Learning Argentine Tango</a> &mdash; 18&ndash;24 month minimum for meaningful mastery; &ldquo;competence crisis&rdquo; at ~6 months; embrace difficulty.</li>
    <li><a href="https://tangocanada.ca/how-long-does-it-take-to-learn-argentine-tango/" target="_blank">Tango Canada Academy &mdash; How Long Does It Take to Learn Argentine Tango?</a> &mdash; 8&ndash;12 weeks for fundamentals; 6&ndash;12 months for ochos/molinetes; 18+ months for advanced expression.</li>
    <li><a href="http://learn-to-tango.com/blog/5-levels-of-learning-tango-how-hard-is-learning-tango/" target="_blank">Learn to Tango &mdash; 5 Levels: How Hard Is It to Learn Tango?</a> &mdash; five stages of competence; 10,000+ hours for mastery; reflective competence stage.</li>
    <li><a href="https://www.dance-forums.com/threads/is-it-possible-for-a-woman-to-become-proficient-in-dancing-argentine-tango-in-1-2-years.49389/" target="_blank">Dance-Forums.com &mdash; Proficiency in Argentine Tango in 1&ndash;2 Years?</a> &mdash; community consensus on high entry barrier and long timeline.</li>
    <li><a href="https://www.quora.com/Why-is-Argentine-Tango-so-difficult" target="_blank">Quora &mdash; Why Is Argentine Tango So Difficult?</a> &mdash; weight placement, frame, lead-follow precision demands from day one.</li>
</ul>

<h3>Lindy Hop</h3>
<ul>
    <li><a href="https://bostonlindyhop.com/faq/" target="_blank">Boston Lindy Hop &mdash; FAQ</a> &mdash; swing-out as fundamental 8-count move; 6-week series structure; rotation accelerates learning.</li>
    <li><a href="https://www.dance-forums.com/threads/lindy-hop-improving-the-swingout.30967/" target="_blank">Dance-Forums.com &mdash; Lindy Hop: Improving the Swing-Out</a> &mdash; &ldquo;5 minutes to learn, 3 years to do it reasonably well&rdquo;; technique refinement is lifelong.</li>
    <li><a href="https://www.quora.com/What-are-some-of-the-hardest-moves-in-swing-dancing-to-learn" target="_blank">Quora &mdash; What Are the Hardest Moves in Swing Dancing?</a> &mdash; swing-out simultaneously the basic and hardest move.</li>
</ul>

<h3>Kizomba</h3>
<ul>
    <li><a href="https://www.salsadancela.com/post/the-sensual-world-of-kizomba-dance-a-comprehensive-beginner-s-guide" target="_blank">Salsa Dance LA &mdash; The Sensual World of Kizomba Dance: Beginner&rsquo;s Guide</a> &mdash; accessible first partner dance; slow tempo aids beginners.</li>
    <li><a href="https://www.goandance.com/en/blog/post/114/9-differences-between-kizomba-and-urban-kizz" target="_blank">Go&amp;Dance &mdash; 9 Differences Between Kizomba and Urban Kiz</a> &mdash; Urban Kiz adds stops, direction changes, acrobatics; significantly higher ceiling.</li>
    <li><a href="https://www.chocolatekizomba.com/kizomba-top-tips/kizomba-vs-urban-kiz-how-to-spot-the-difference-and-find-kizomba-classes" target="_blank">Chocolate Kizomba &mdash; Kizomba vs. Urban Kiz</a> &mdash; traditional vs. contemporary complexity comparison.</li>
</ul>

<h3>Brazilian Zouk</h3>
<ul>
    <li><a href="https://zouksidedown.wordpress.com/2015/07/10/letter-to-a-beginner/" target="_blank">ZoukSide Down &mdash; Letter to a Beginner</a> &mdash; &ldquo;beginner&rsquo;s hell&rdquo; phase; frustration and fumbling in early stages; immediate social dancing recommended.</li>
    <li><a href="https://zouksidedown.wordpress.com/2014/05/04/the-journey-of-a-dancer-series-week-two-the-key-to-becoming-a-great-zouk-leader/" target="_blank">ZoukSide Down &mdash; The Journey of a Dancer: Key to Becoming a Great Zouk Leader</a> &mdash; leader development stages; long-term growth trajectory.</li>
    <li><a href="https://zoukology.com/brazilian-zouk-a-demanding-physical-art-casi/" target="_blank">Zoukology &mdash; Brazilian Zouk: A Demanding Physical Art</a> &mdash; physical demands; head movements as defining advanced feature.</li>
    <li><a href="https://twoleftfeetpodcast.medium.com/dealing-with-stress-frustration-in-brazilian-zouk-class-a328d2d73c28" target="_blank">Two Left Feet Podcast &mdash; Dealing with Stress/Frustration in Brazilian Zouk Class</a> &mdash; beginner&rsquo;s hell lasting longer than in other styles.</li>
</ul>

<h3>West Coast Swing</h3>
<ul>
    <li><a href="https://www.swingliteracy.com/category/about-dancing/the-learning-curve/" target="_blank">SwingLiteracy &mdash; The Learning Curve (article series)</a> &mdash; WCS learning progression; steep initial curve; musical interpretation depth.</li>
    <li><a href="https://www.westcoastswingonline.com/10-biggest-struggles-of-west-coast-swing-dancers/" target="_blank">WCS Online &mdash; 10 Biggest Struggles of WCS Dancers</a> &mdash; &ldquo;WCS is a VERY difficult dance to be really good at&rdquo;; timing, musicality, and confidence challenges.</li>
    <li><a href="https://www.westcoastswingonline.com/the-challenge-of-west-coast-swing/" target="_blank">WCS Online &mdash; 7 Challenges of West Coast Swing</a> &mdash; six-beat pattern complexity; open position demands; follower skill requirements.</li>
    <li><a href="https://www.swingliteracy.com/tough-love-read-at-your-own-risk/" target="_blank">SwingLiteracy &mdash; Tough Love: Read at Your Own Risk</a> &mdash; education and practice requirements for WCS progression.</li>
</ul>

<h3>Cha-Cha (Ballroom/Latin)</h3>
<ul>
    <li><a href="https://studioaccessballroom.com/latin-and-ballroom-dance-levels/" target="_blank">Access Ballroom &mdash; Latin and Ballroom Dance Levels</a> &mdash; Bronze/Silver/Gold syllabus structure; Cuban motion introduced at Bronze 2&ndash;3.</li>
    <li><a href="https://www.centralhome.com/ballroomcountry/cha-cha-syll.htm" target="_blank">CentralHome &mdash; Cha Cha Syllabus (International Latin)</a> &mdash; complete syllabus breakdown by level.</li>
    <li><a href="https://delta.dance/2020/06/video-intermediate-chacha/" target="_blank">Delta.Dance &mdash; Intermediate Cha Cha Video Program</a> &mdash; intermediate technique focus and progression.</li>
</ul>

<h3>Modern Jive / Ceroc</h3>
<ul>
    <li><a href="https://en.wikipedia.org/wiki/Modern_Jive" target="_blank">Wikipedia &mdash; Modern Jive</a> &mdash; overview; &ldquo;simplest of all partner dances&rdquo;; no specific footwork.</li>
    <li><a href="https://whataboutdance.com/how-easy-is-modern-jive-dance/" target="_blank">What About Dance &mdash; How Easy Is Modern Jive Dance?</a> &mdash; dancing within half an hour; limited ceiling for advanced development.</li>
    <li><a href="https://www.ceroc.com/24/3441/learn-to-jive-dance-dance-classes-lessons" target="_blank">Ceroc UK &mdash; Learn to Jive Dance</a> &mdash; first-night experience; move-per-week progression.</li>
</ul>

<h3>Merengue</h3>
<ul>
    <li><a href="https://www.classpop.com/magazine/how-to-dance-cumbia" target="_blank">Classpop &mdash; How to Dance Cumbia (2025 Guide)</a> &mdash; merengue as gateway dance; simplest Latin rhythm.</li>
    <li><a href="https://www.salsavida.com/articles/latin-dances/" target="_blank">Salsa Vida &mdash; Latin Dances List: 40 Popular Styles</a> &mdash; merengue described as the easiest Latin dance; marching basic.</li>
</ul>

<h3>Cumbia</h3>
<ul>
    <li><a href="https://www.classpop.com/magazine/how-to-dance-cumbia" target="_blank">Classpop &mdash; How to Dance Cumbia (2025 Guide)</a> &mdash; beginner-friendly; regional variations (Colombian, Mexican, Argentine).</li>
    <li><a href="https://somoloco.com/colombian-salsa-whats-it-all-about/" target="_blank">Somoloco &mdash; Colombian Salsa: What&rsquo;s It All About</a> &mdash; cumbia influence on Cali-style salsa.</li>
    <li><a href="https://dancemagazine.com/cumbia-the-new-old-latin-dance/" target="_blank">Dance Magazine &mdash; Cumbia: The New/Old Latin Dance</a> &mdash; cultural history and regional spread.</li>
</ul>

<h3>Blues</h3>
<ul>
    <li><a href="https://thebluesroom.com/mastering-the-basics-why-essential-skills-are-the-foundation-of-your-blues-dance-journey/" target="_blank">The Blues Room &mdash; Mastering the Basics: Foundation of Blues Dance</a> &mdash; foundational technique; close embrace importance.</li>
    <li><a href="https://dirtcheapblues.com/blues-dance-styles/" target="_blank">Dirt Cheap Blues &mdash; Blues Dance Styles</a> &mdash; slow drag, struttin&rsquo;, and other idioms; improvisation-based nature.</li>
    <li><a href="https://www.bluescentral.org/blues-dancing-technique/" target="_blank">bluesCENTRAL &mdash; Blues Dancing Technique</a> &mdash; pulse-based movement; musical interpretation depth.</li>
</ul>

<h3>Cali Style Salsa</h3>
<ul>
    <li><a href="https://thedancedojo.com/salsa-dance-terms/colombian-style-salsa-calena/" target="_blank">The Dance Dojo &mdash; Colombian Style Salsa (Salsa Cale&ntilde;a)</a> &mdash; repique footwork; pachanga and boogaloo influences; speed challenge.</li>
    <li><a href="https://www.salsaforums.com/threads/cali-style-salsa-is-much-harder-for-follows.36771/" target="_blank">SalsaForums &mdash; Cali Style Salsa Is Much Harder for Follows</a> &mdash; follower difficulty; fast footwork demands.</li>
    <li><a href="https://thedancedojo.com/salsa-styles/" target="_blank">The Dance Dojo &mdash; Salsa Styles Comparison</a> &mdash; Cali style vs. LA/NY/Cuban; speed as defining characteristic.</li>
    <li><a href="https://folklife.si.edu/magazine/la-vieja-guardia-salsa-dancing-cali-colombia" target="_blank">Smithsonian Folklife &mdash; Salsa Dancing in Cali, Colombia</a> &mdash; cultural context; &ldquo;La capital mundial de la salsa.&rdquo;</li>
</ul>

<h3>Ballroom (Standard)</h3>
<ul>
    <li><a href="https://www.justdanzehouston.com/post/levels-of-ballroom-dancing" target="_blank">Just Danze Houston &mdash; Levels of Ballroom Dancing: From Bronze to Gold Mastery</a> &mdash; syllabus progression timelines; 100&ndash;500 hours for Bronze depending on scope.</li>
    <li><a href="https://byyoursidedancestudio.com/what-is-the-ballroom-dancing-medal-system-and-how-does-it-work/" target="_blank">By Your Side Dance Studio &mdash; The Ballroom Dancing Medal System</a> &mdash; medal/syllabus system explanation.</li>
    <li><a href="https://delta.dance/2015/01/slow-foxtrot-a-stroll-in-the-moonlight/" target="_blank">Delta.Dance &mdash; Slow Foxtrot: A Stroll in the Moonlight</a> &mdash; &ldquo;most challenging of the Standard dances&rdquo;; control and seamless movement required.</li>
    <li><a href="https://www.dance-forums.com/threads/order-of-learning-dances.51390/" target="_blank">Dance-Forums.com &mdash; Order of Learning Dances?</a> &mdash; multi-dance learning; waltz recommended first; cross-dance skills transfer.</li>
    <li><a href="https://www.dance-forums.com/threads/what-is-the-most-difficult-ballroom-dance.2544/" target="_blank">Dance-Forums.com &mdash; What Is the Most Difficult Ballroom Dance?</a> &mdash; community debate on ballroom dance difficulty ranking.</li>
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