from urllib import response

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json


def get_ai_response(chat_history):

    url = "https://defend-academy-parameters-region.trycloudflare.com/webhook/3be5f2b8-7f95-4964-b9c1-88c0798a75b8"

    latest_question = chat_history[-1]["content"]

    payload = {
        "question": latest_question
    }

    response = requests.post(
        url,
        json=payload,
        headers={
            "X-SustainIQ-Key": st.secrets["N8N_WEBHOOK_SECRET"]
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["answer"]



# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SustainIQ — Germany Student Guide",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* sidebar styling */
section[data-testid="stSidebar"] { background-color: #0d1117; }
section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

/* metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    margin-bottom: 4px;
}
.metric-value { font-size: 1.8rem; font-weight: 600; color: #58a6ff; }
.metric-label { font-size: 0.78rem; color: #8b949e; margin-top: 4px; }

/* section headers */
.section-header {
    font-size: 1rem; font-weight: 600;
    color: #e6edf3; margin: 1.2rem 0 0.5rem;
    border-left: 3px solid #58a6ff;
    padding-left: 10px;
}

/* cause boxes */
.cause-box {
    background: #161b22;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 5px 0;
    border: 1px solid #30363d;
    font-size: 0.85rem;
    color: #c9d1d9;
    line-height: 1.6;
}
.cause-box b { color: #a5a9ff; }

/* chat bubbles */
.chat-container {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px;
    min-height: 200px;
    max-height: 380px;
    overflow-y: auto;
    margin-bottom: 10px;
}
.bubble-user {
    background: #1f6feb;
    color: #ffffff;
    padding: 10px 14px;
    border-radius: 12px 12px 2px 12px;
    margin: 6px 0 6px auto;
    max-width: 80%;
    width: fit-content;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-left: auto;
}
.bubble-bot {
    background: #161b22;
    border: 1px solid #30363d;
    color: #e6edf3;
    padding: 10px 14px;
    border-radius: 12px 12px 12px 2px;
    margin: 6px 0;
    max-width: 85%;
    font-size: 0.9rem;
    line-height: 1.5;
}
.tag-chip {
    display: inline-block;
    background: #1c2128;
    border: 1px solid #30363d;
    color: #8b949e;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px;
    cursor: pointer;
}

/* info cards for jobs/parttime */
.info-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.info-card h4 { color: #58a6ff; font-size: 0.95rem; margin: 0 0 6px; }
.info-card p  { color: #8b949e; font-size: 0.85rem; margin: 0; line-height: 1.6; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 4px;
}
.badge-green  { background: #0d4429; color: #3fb950; }
.badge-blue   { background: #0c2d6b; color: #58a6ff; }
.badge-orange { background: #3d1f00; color: #d29922; }
.badge-purple { background: #271052; color: #bc8cff; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SHARED DATA — DISASTERS
# ─────────────────────────────────────────────────────────────
DISASTER_COLORS = {
    "Floods":       "#378ADD",
    "Earthquakes":  "#E24B4A",
    "Storms":       "#EF9F27",
    "Heatwaves":    "#BA7517",
    "Wildfires":    "#639922",
    "Landslides":   "#7F77DD",
    "Droughts":     "#1D9E75",
    "Extreme Cold": "#D4537E",
}

CAUSES = {
    "Floods":       "Heavy prolonged rainfall, snowmelt, river overflow. Intensified by climate change — warmer air holds ~7% more moisture per 1°C (Clausius-Clapeyron effect). Key events: Rhine 1993/1995, Elbe 2002, Ahr Valley 2021 (220 deaths).",
    "Earthquakes":  "African-Eurasian plate boundary collision. Apennine extensional faults (Italy); North Anatolian fault (Turkey). Frequency unchanged by climate. Key events: Friuli 1976 (976 deaths), Amatrice 2016 (299 deaths), Turkey-Syria 2023 (50,000+ deaths).",
    "Storms":       "Atlantic extratropical cyclones and Medicanes (Mediterranean hurricanes). Key events: Great Storm 1987, Daria/Vivian/Wiebke 1990 (200+ deaths), Lothar/Martin 1999 (140 deaths), Kyrill 2007, Ciaran 2023.",
    "Heatwaves":    "Persistent blocking anticyclones + rising baseline temperatures. Urban heat islands amplify by 2–5°C. Key events: 2003 (~70,000 excess deaths), 2019 (45.9°C France record), 2022 (40°C+ UK first time).",
    "Wildfires":    "Longer/hotter/drier summers, rural land abandonment, fuel accumulation. Key events: Southern France/Iberia 1989-90, Portugal 2017 (Pedrógão, 66 deaths), Greece 2021, EU record 800,000 ha burned in 2022.",
    "Landslides":   "Intense rainfall on steep terrain, deforestation, permafrost thaw in Alps. Key events: Sarno Italy 1998 (160 deaths), Messina 2009 (37 deaths), increasing Alpine debris flows from 2010s.",
    "Droughts":     "Blocking anticyclones diverting Atlantic rainfall; Mediterranean drying trend. Key events: Iberian 1991-92, UK 1995-96, Europe-wide 2003, 2018, 2022 (worst in 500 years, 63% EU territory affected).",
    "Extreme Cold": "Siberian anticyclone intrusions; polar vortex disruptions. Key events: winters 1985 & 1987, Beast from the East 2018 (-20°C in Western Europe), various Balkan cold waves.",
}

years_all = list(range(1975, 2026))
raw_disasters = {
    "Floods":       [4,5,3,6,4,5,4,5,3,4,5,4,6,5,5,7,6,5,8,7,9,6,7,8,9,8,
                     9,12,7,8,8,9,10,9,10,11,10,11,12,10,11,11,10,12,11,12,14,13,15,14,13],
    "Earthquakes":  [3,6,4,2,3,2,3,2,2,2,3,2,3,3,2,4,3,3,2,3,3,2,4,3,3,4,
                     4,3,3,3,4,3,4,4,5,4,5,5,3,4,4,5,4,4,4,3,4,4,5,4,4],
    "Storms":       [3,2,3,3,4,3,3,4,3,3,4,3,5,3,3,6,4,3,4,4,5,4,4,4,5,5,
                     5,5,5,5,5,5,6,5,5,6,5,5,6,6,5,6,5,6,6,6,6,7,7,7,6],
    "Heatwaves":    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                     1,1,5,2,2,2,2,2,2,2,2,2,2,2,3,2,2,3,4,3,4,5,5,5,4],
    "Wildfires":    [2,2,2,2,2,2,2,2,2,2,2,2,3,2,5,4,3,3,3,3,3,3,3,3,3,3,
                     3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,6,7,6,5,5],
    "Landslides":   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,2,2,2,1,2,3,2,2,
                     2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,3],
    "Droughts":     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,3,3,1,1,2,2,1,1,1,2,
                     2,1,4,1,1,2,2,1,1,2,2,3,1,2,2,2,2,4,3,2,3,5,3,4,3],
    "Extreme Cold": [2,2,2,2,3,2,2,2,3,2,4,2,4,2,2,2,2,2,2,2,2,3,2,2,2,2,
                     2,2,1,2,2,2,2,2,2,3,2,3,2,2,2,2,2,3,2,2,2,2,2,2,2],
}

NOTABLE_EVENTS = {
    1976:"Friuli EQ", 1980:"S.Italy EQ", 1987:"Great Storm",
    1988:"Spitak EQ", 1990:"Triple Storms", 1993:"Rhine Floods",
    1999:"Lothar/Martin", 2002:"Elbe Floods", 2003:"Heatwave",
    2009:"L'Aquila EQ", 2016:"Amatrice EQ", 2021:"Ahr Floods",
    2022:"Record Drought", 2023:"Turkey EQ",
}

df_disasters = pd.DataFrame(raw_disasters, index=years_all)
df_disasters.index.name = "Year"
df_disasters["Total"] = df_disasters.sum(axis=1)

BG = "#0d1117"

# ─────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌱 SustainIQ")
    st.markdown("*Germany University Student Guide*")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=[
            "🏠 Home & AI Chat",
            "🌍 European Disasters",
            "💼 Sustainability Jobs",
            "⏰ Part-time Work Guide",
            "🌡️ Climate Data",
            "⚡ Green Energy",
            "🪪 Visa & Stay",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("Data: EM-DAT · EEA · IPCC AR6\nDeveloped with Streamlit + Plotly")

# ─────────────────────────────────────────────────────────────
# PAGE 1 — HOME & AI CHAT
# ─────────────────────────────────────────────────────────────
if page == "🏠 Home & AI Chat":
    st.title("🌱 SustainIQ — Germany Student Guide")
    st.markdown("*Your AI-powered guide for sustainability students in Germany*")
    st.markdown("---")

    col_chat, col_info = st.columns([3, 2])

    with col_chat:
        st.markdown('<div class="section-header">💬 Ask your AI assistant</div>', unsafe_allow_html=True)

        # Chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "👋 Hi! I'm your Germany sustainability student guide. Ask me anything about:\n\n• 🎓 Sustainability courses & universities\n• 💼 Job opportunities in green sector\n• ⏰ Part-time work rules for students\n• 🌍 Climate & disaster research\n• 🪪 Visa & staying in Germany\n\nWhat would you like to know?"}
            ]

        # Render chat
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_html += f'<div class="bubble-user">{msg["content"]}</div>'
            else:
                content = msg["content"].replace("\n", "<br>")
                chat_html += f'<div class="bubble-bot">{content}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Quick topic chips
        st.markdown("**Quick questions:**")
        chips = [
            "What part-time jobs can I do as a student?",
            "Best sustainability universities in Germany?",
            "How does student visa work in Germany?",
            "What green energy jobs are growing in Germany?",
            "How does climate change affect Europe?",
            "What scholarships exist for sustainability?",
        ]
        
        cols_chip = st.columns(3)

        for i, chip in enumerate(chips):
            if cols_chip[i % 3].button(
                chip[:35] + "…",
                key=f"chip_{i}",
                use_container_width=True
            ):
                st.session_state.messages.append({
                    "role": "user",
                    "content": chip
                })

                with st.spinner("AI is thinking…"):
                    try:
                        reply = get_ai_response(st.session_state.messages)
                    except Exception as e:
                        reply = f"Sorry, I couldn't connect to the AI right now. Error: {str(e)}"

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

                st.rerun()


        # Text input
        user_input = st.chat_input("Ask about jobs, visa, sustainability, campus life…")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("AI is thinking…"):
                
                try:
                    reply = get_ai_response(st.session_state.messages)

                except Exception as e:
                    reply = f"Sorry, I couldn't connect right now. Error: {str(e)}"

              
                st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

    with col_info:
        st.markdown('<div class="section-header">📊 Quick Stats</div>', unsafe_allow_html=True)
        stats = [
            ("€12.41/hr", "Minimum wage Germany (2024)"),
            ("120 days", "Max part-time work/year for students"),
            ("3,400+", "Open sustainability jobs in Germany"),
            ("47", "Universities offering sustainability degrees"),
            ("€850–1,200", "Average student cost of living/month"),
            ("18 months", "Job-seeker visa after graduation"),
        ]
        for val, label in stats:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value">{val}</div>'
                f'<div class="metric-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────────────────────
# PAGE 2 — EUROPEAN DISASTERS (full app from before)
# ─────────────────────────────────────────────────────────────
elif page == "🌍 European Disasters":
    st.title("🌍 Natural Disasters in Europe  1975–2025")
    st.markdown("*Annual events by type — causes, trends, and historical context*")

    # Controls
    ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2, 2, 1, 1])
    with ctrl1:
        year_range = st.slider("Year range", 1975, 2025, (1975, 2025), step=1)
    with ctrl2:
        selected_types = st.multiselect(
            "Disaster types",
            options=list(DISASTER_COLORS.keys()),
            default=list(DISASTER_COLORS.keys())
        )
    with ctrl3:
        chart_style = st.selectbox("Chart style", ["Stacked Bar", "Line", "Area", "Heatmap"])
    with ctrl4:
        show_notable = st.checkbox("Major events", value=True)
        show_causes  = st.checkbox("Causes panel", value=True)

    if not selected_types:
        st.warning("Please select at least one disaster type.")
        st.stop()

    mask = (df_disasters.index >= year_range[0]) & (df_disasters.index <= year_range[1])
    dff  = df_disasters.loc[mask, selected_types].copy()
    dff["Total"] = dff.sum(axis=1)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    for col, val, lbl in [
        (k1, int(dff["Total"].sum()),           "Total events"),
        (k2, int(dff["Total"].idxmax()),        "Busiest year"),
        (k3, round(dff["Total"].mean(), 1),     "Avg events/year"),
        (k4, dff[selected_types].sum().idxmax(),"Most frequent type"),
    ]:
        col.markdown(
            f'<div class="metric-card"><div class="metric-value">{val}</div>'
            f'<div class="metric-label">{lbl}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-header">Annual disaster events</div>', unsafe_allow_html=True)

    # Main chart
    if chart_style == "Stacked Bar":
        melted = dff[selected_types].reset_index().melt(id_vars="Year", var_name="Type", value_name="Events")
        fig = px.bar(melted, x="Year", y="Events", color="Type",
                     color_discrete_map=DISASTER_COLORS, template="plotly_dark")
        fig.update_layout(barmode="stack")
    elif chart_style == "Line":
        fig = go.Figure()
        for d in selected_types:
            fig.add_trace(go.Scatter(x=dff.index, y=dff[d], name=d,
                          line=dict(color=DISASTER_COLORS[d], width=2),
                          mode="lines+markers", marker_size=4))
    elif chart_style == "Area":
        melted = dff[selected_types].reset_index().melt(id_vars="Year", var_name="Type", value_name="Events")
        fig = px.area(melted, x="Year", y="Events", color="Type",
                      color_discrete_map=DISASTER_COLORS, template="plotly_dark")
    else:
        fig = px.imshow(dff[selected_types].T, aspect="auto",
                        color_continuous_scale="Blues",
                        labels=dict(x="Year", y="Type", color="Events"),
                        template="plotly_dark")

    fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
                      height=420, margin=dict(l=10,r=10,t=20,b=30))

    if show_notable and chart_style != "Heatmap":
        for yr, lbl in NOTABLE_EVENTS.items():
            if year_range[0] <= yr <= year_range[1] and yr in dff.index:
                fig.add_vline(x=yr, line_dash="dot",
                              line_color="rgba(255,255,255,0.2)", line_width=1)
                fig.add_annotation(x=yr, y=dff.loc[yr,"Total"],
                                   text=lbl, showarrow=True,
                                   arrowhead=2, arrowcolor="#7c83ff",
                                   font=dict(size=9, color="#a5a9ff"),
                                   bgcolor="#1a1d2e", bordercolor="#30363d",
                                   ax=20, ay=-32)
    st.plotly_chart(fig, use_container_width=True)

    # Two column row
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-header">Total by type</div>', unsafe_allow_html=True)
        totals = dff[selected_types].sum().reset_index()
        totals.columns = ["Type","Events"]
        totals = totals.sort_values("Events", ascending=True)
        fig2 = px.bar(totals, x="Events", y="Type", orientation="h",
                      color="Type", color_discrete_map=DISASTER_COLORS,
                      template="plotly_dark")
        fig2.update_layout(paper_bgcolor=BG, plot_bgcolor=BG,
                           showlegend=False, height=300,
                           margin=dict(l=0,r=10,t=10,b=20))
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.markdown('<div class="section-header">Decade comparison</div>', unsafe_allow_html=True)
        periods = {"1975–84":(1975,1984),"1985–94":(1985,1994),
                   "1995–04":(1995,2004),"2005–14":(2005,2014),"2015–25":(2015,2025)}
        decade_rows = {}
        for lbl,(s,e) in periods.items():
            pm = (df_disasters.index >= max(s,year_range[0])) & (df_disasters.index <= min(e,year_range[1]))
            if pm.any():
                decade_rows[lbl] = df_disasters.loc[pm, selected_types].sum()
        if decade_rows:
            dec_df  = pd.DataFrame(decade_rows).T
            melted3 = dec_df.reset_index().melt(id_vars="index", var_name="Type", value_name="Events")
            fig3    = px.bar(melted3, x="index", y="Events", color="Type",
                             color_discrete_map=DISASTER_COLORS, template="plotly_dark")
            fig3.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, barmode="stack",
                               xaxis_title="", showlegend=False, height=300,
                               margin=dict(l=0,r=10,t=10,b=20))
            st.plotly_chart(fig3, use_container_width=True)

    # Trend
    st.markdown('<div class="section-header">Trend — rolling 5-year average</div>', unsafe_allow_html=True)
    roll = dff["Total"].rolling(5, center=True).mean()
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=dff.index, y=dff["Total"], name="Annual total",
                          marker_color="rgba(88,166,255,0.25)"))
    fig4.add_trace(go.Scatter(x=roll.index, y=roll, name="5-yr average",
                              line=dict(color="#58a6ff", width=2.5)))
    if len(dff) > 2:
        xv = np.array(dff.index)
        yv = dff["Total"].values
        z  = np.polyfit(xv, yv, 1)
        p  = np.poly1d(z)
        fig4.add_trace(go.Scatter(x=dff.index, y=p(xv),
                                  name=f"Trend (+{z[0]:.2f} events/yr)",
                                  line=dict(color="#E24B4A", width=1.5, dash="dash")))
    fig4.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=BG,
                       height=260, margin=dict(l=10,r=10,t=10,b=30))
    st.plotly_chart(fig4, use_container_width=True)

    # Raw data
    with st.expander("📊 Raw data table"):
        show_cols = selected_types + ["Total"]
        st.dataframe(dff[show_cols].style.background_gradient(cmap="Blues", subset=["Total"]),
                     use_container_width=True)
        st.download_button("⬇ Download CSV", data=dff[show_cols].to_csv(),
                           file_name="europe_disasters.csv", mime="text/csv")

    # Causes
    if show_causes:
        st.markdown('<div class="section-header">Causes & context</div>', unsafe_allow_html=True)
        cols_c = st.columns(2)
        for i, dtype in enumerate(selected_types):
            color = DISASTER_COLORS.get(dtype, "#888")
            cols_c[i % 2].markdown(
                f'<div class="cause-box">'
                f'<b style="color:{color}">🔍 {dtype}</b><br>'
                f'{CAUSES.get(dtype,"—")}'
                f'</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────────────────────
# PAGE 3 — SUSTAINABILITY JOBS
# ─────────────────────────────────────────────────────────────
elif page == "💼 Sustainability Jobs":
    st.title("💼 Sustainability Jobs in Germany")
    st.markdown("*Career paths, salaries, and skills for international sustainability students*")

    j1, j2, j3, j4 = st.columns(4)
    for col, val, lbl in [
        (j1, "3,400+", "Open green jobs"),
        (j2, "€45,000", "Avg entry salary"),
        (j3, "12%", "Sector growth/year"),
        (j4, "18 months", "Job-seeker visa"),
    ]:
        col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div>'
                     f'<div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Top job categories</div>', unsafe_allow_html=True)

    jobs = [
        ("🌞 Renewable Energy Engineer", "€42,000–65,000/yr",
         "Design and manage solar, wind, and hydro energy systems. Germany leads in Energiewende (energy transition). Strong demand in Bavaria, Schleswig-Holstein.",
         ["Engineering degree", "AutoCAD/MATLAB", "German B2"]),
        ("♻️ Sustainability Consultant", "€38,000–58,000/yr",
         "Help companies reduce carbon footprint and meet ESG goals. Growing rapidly with EU Green Deal requirements. Big 4 consulting firms actively hire.",
         ["Business/Environment degree", "Data analysis", "English + German"]),
        ("🌱 Environmental Policy Analyst", "€36,000–52,000/yr",
         "Work with government agencies, NGOs, or EU institutions. Berlin and Brussels are key hubs. Research-focused with strong writing requirements.",
         ["Policy/Law/Environment", "Research skills", "German C1"]),
        ("📊 ESG Data Analyst", "€40,000–60,000/yr",
         "Analyse environmental, social, governance data for finance sector. Fastest-growing sustainability role in 2023–2024. Remote-friendly.",
         ["Data science", "Python/SQL", "Bloomberg ESG"]),
        ("🏗️ Green Building Architect", "€44,000–68,000/yr",
         "Design energy-efficient buildings under Germany's GEG (Building Energy Act). DGNB certification a plus. Strong in Munich, Hamburg, Berlin.",
         ["Architecture degree", "BIM software", "DGNB knowledge"]),
        ("🚗 E-Mobility Engineer", "€46,000–72,000/yr",
         "Electric vehicle and charging infrastructure development. Germany's auto sector is transforming — BMW, VW, Mercedes all hiring sustainability engineers.",
         ["Mechanical/Electrical Eng", "Battery tech", "Automotive knowledge"]),
    ]

    for title, salary, desc, skills in jobs:
        st.markdown(
            f'<div class="info-card">'
            f'<h4>{title} <span style="float:right;font-size:0.8rem;color:#3fb950;">{salary}</span></h4>'
            f'<p>{desc}</p>'
            f'<div style="margin-top:8px;">'
            + "".join(f'<span class="badge badge-blue">✓ {s}</span>' for s in skills)
            + f'</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-header">Salary comparison by role</div>', unsafe_allow_html=True)
    salary_df = pd.DataFrame({
        "Role": ["E-Mobility Engineer","Green Building Architect","ESG Data Analyst",
                 "Sustainability Consultant","Environmental Policy","Renewable Energy Eng"],
        "Min (€)": [46000, 44000, 40000, 38000, 36000, 42000],
        "Max (€)": [72000, 68000, 60000, 58000, 52000, 65000],
    })
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(name="Min salary", x=salary_df["Role"], y=salary_df["Min (€)"],
                           marker_color="#1f6feb"))
    fig_s.add_trace(go.Bar(name="Max salary", x=salary_df["Role"], y=salary_df["Max (€)"],
                           marker_color="#58a6ff"))
    fig_s.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=BG,
                        barmode="group", height=350, xaxis_tickangle=-20,
                        margin=dict(l=10,r=10,t=20,b=80))
    st.plotly_chart(fig_s, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# PAGE 4 — PART-TIME WORK GUIDE
# ─────────────────────────────────────────────────────────────
elif page == "⏰ Part-time Work Guide":
    st.title("⏰ Part-time Work Guide for Students")
    st.markdown("*Rules, rights, and best jobs for international students in Germany*")

    p1, p2, p3, p4 = st.columns(4)
    for col, val, lbl in [
        (p1, "120 days", "Full days/year allowed"),
        (p2, "240 days", "Half days/year allowed"),
        (p3, "€12.41/hr", "Minimum wage (2024)"),
        (p4, "€520/mo", "Mini-job limit (tax-free)"),
    ]:
        col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div>'
                     f'<div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 Key rules you must know</div>', unsafe_allow_html=True)
    rules = [
        ("⏱️ Work hour limit", "badge-blue",
         "120 full days OR 240 half days per year. A 'half day' = max 4 hours. Exceeding this requires special permit from Ausländerbehörde."),
        ("💰 Mini-job (Minijob)", "badge-green",
         "Earn up to €520/month tax-free. No income tax, no health insurance contribution from you. Great for first job — just register with employer."),
        ("📋 Tax registration", "badge-orange",
         "Get your Steuer-ID (tax ID) — arrives by post within 2-3 weeks of Anmeldung. You need this for every job. Keep it safe!"),
        ("🏥 Health insurance", "badge-purple",
         "You must have health insurance. If working >20hrs/week, you may lose student health insurance rate (€120/mo). Check with your Krankenkasse."),
        ("🎓 HiWi jobs", "badge-blue",
         "Wissenschaftliche Hilfskraft (HiWi) — university research assistant. Up to 80hrs/month, €13-17/hr, often flexible. Best option for sustainability students."),
        ("📅 Semester vs vacation", "badge-green",
         "During lecture period: max 20 hrs/week. During semester break (vacation): can work full-time. Plan bigger work periods in summer/winter breaks."),
    ]
    for title, badge_class, desc in rules:
        st.markdown(
            f'<div class="info-card">'
            f'<h4><span class="badge {badge_class}">{title}</span></h4>'
            f'<p style="margin-top:8px;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-header">🌱 Best part-time jobs for sustainability students</div>',
                unsafe_allow_html=True)

    pt_jobs = [
        ("🔬 HiWi — Research Assistant", "€13–17/hr", "University",
         "Best fit: work directly on sustainability research. Flexible hours, good pay, CV booster."),
        ("☕ Café / Restaurant", "€12.41–14/hr", "Service",
         "Flexible shifts, easy to find, cash tips. Many eco/organic cafes in German university cities."),
        ("📦 Delivery / Logistics", "€13–15/hr", "Logistics",
         "DHL, Amazon, Gorillas. Physical work but very flexible. No German required."),
        ("🌳 Environmental NGO", "€12–14/hr", "NGO",
         "NABU, WWF Germany, Greenpeace Deutschland. Part-time office/field roles for sustainability students."),
        ("📚 Tutor / Teaching", "€15–25/hr", "Education",
         "Teach maths, science, languages. Set your own schedule. Platforms: Nachhilfe, Superprof."),
        ("💻 Student jobs online", "€12–20/hr", "Remote",
         "Freelance translation, data entry, social media. Platforms: Upwork, Fiverr, Studitemps."),
    ]

    c1, c2 = st.columns(2)
    for i, (title, rate, sector, desc) in enumerate(pt_jobs):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(
                f'<div class="info-card">'
                f'<h4>{title} <span style="float:right;font-size:0.8rem;color:#3fb950;">{rate}</span></h4>'
                f'<span class="badge badge-blue">{sector}</span>'
                f'<p style="margin-top:8px;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-header">📅 Monthly earnings calculator</div>',
                unsafe_allow_html=True)
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        hrs_per_week = st.slider("Hours per week", 1, 20, 10)
        hourly_rate  = st.slider("Hourly rate (€)", 12, 25, 13)
    with col_calc2:
        monthly = hrs_per_week * 4.33 * hourly_rate
        annual  = monthly * 12
        is_minijob = monthly <= 520
        st.metric("Monthly earnings", f"€{monthly:,.0f}")
        st.metric("Annual earnings", f"€{annual:,.0f}")
        if is_minijob:
            st.success("✅ Within Minijob limit (€520) — tax-free!")
        else:
            st.warning(f"⚠️ Above Minijob limit — income tax applies on €{monthly-520:,.0f}/month")

# ─────────────────────────────────────────────────────────────
# PAGE 5 — CLIMATE DATA
# ─────────────────────────────────────────────────────────────
elif page == "🌡️ Climate Data":
    st.title("🌡️ Climate Trends — Europe")
    st.markdown("*Temperature anomalies, CO₂ levels, and warming trends*")

    years_c = list(range(1975, 2026))
    np.random.seed(42)
    temp_anomaly = [-0.1,-0.05,0,-0.1,0.1,0.2,0.1,0.15,0.2,0.15,
                     0.25,0.2,0.3,0.25,0.35,0.4,0.3,0.45,0.5,0.55,
                     0.6,0.55,0.65,0.7,0.65,0.7,0.75,0.8,1.2,0.9,
                     0.95,1.0,1.05,1.1,1.0,1.15,1.2,1.25,1.1,1.3,
                     1.2,1.35,1.4,1.3,1.5,1.45,1.6,1.55,1.7,1.65,1.8]
    co2 = [331+i*1.9+np.random.uniform(-0.3,0.3) for i in range(51)]

    fig_c1 = go.Figure()
    colors_bar = ["#E24B4A" if t > 0.8 else "#EF9F27" if t > 0.4 else "#378ADD" for t in temp_anomaly]
    fig_c1.add_trace(go.Bar(x=years_c, y=temp_anomaly, marker_color=colors_bar, name="Temp anomaly (°C)"))
    fig_c1.add_hline(y=0, line_dash="dash", line_color="white", line_width=1)
    fig_c1.add_hline(y=1.5, line_dash="dot", line_color="#E24B4A", line_width=1,
                     annotation_text="1.5°C Paris target", annotation_position="right")
    fig_c1.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=BG,
                         title="European temperature anomaly vs 1950–1980 baseline (°C)",
                         height=350, margin=dict(l=10,r=10,t=40,b=30))
    st.plotly_chart(fig_c1, use_container_width=True)

    fig_c2 = go.Figure()
    fig_c2.add_trace(go.Scatter(x=years_c, y=co2, mode="lines",
                                line=dict(color="#EF9F27", width=2.5),
                                fill="tozeroy", fillcolor="rgba(239,159,39,0.1)"))
    fig_c2.add_hline(y=350, line_dash="dot", line_color="#3fb950", line_width=1,
                     annotation_text="Safe limit (Hansen, 350ppm)", annotation_position="right")
    fig_c2.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=BG,
                         title="Atmospheric CO₂ concentration (ppm) — Europe",
                         height=300, margin=dict(l=10,r=10,t=40,b=30))
    st.plotly_chart(fig_c2, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# PAGE 6 — GREEN ENERGY
# ─────────────────────────────────────────────────────────────
elif page == "⚡ Green Energy":
    st.title("⚡ Green Energy in Germany")
    st.markdown("*Renewable energy growth, Germany's Energiewende, and what it means for your career*")

    energy_years = list(range(2000, 2026))
    solar   = [0.1,0.2,0.3,0.4,0.6,1.0,1.8,3.5,5.8,9.8,17,24,32,36,38,40,41,43,46,48,52,59,62,65,70,75]
    wind    = [7,8,9,10,11,13,16,19,23,26,30,33,35,38,40,44,48,53,59,64,70,73,76,78,80,82]
    coal    = [55,54,52,50,48,46,45,44,43,43,41,40,39,38,36,34,32,30,26,24,20,18,15,12,10,8]
    nuclear = [30,29,29,28,27,27,27,26,26,26,24,17,16,16,15,14,14,13,13,12,11,6,6,6,0,0]

    
    fig_e = go.Figure()

    for name, data, color, fill_color in [
        ("Solar", solar, "#EF9F27", "rgba(239,159,39,0.13)"),
        ("Wind", wind, "#378ADD", "rgba(55,138,221,0.13)"),
        ("Coal", coal, "#888780", None),
        ("Nuclear", nuclear, "#E24B4A", None),
    ]:
        fig_e.add_trace(go.Scatter(
            x=energy_years,
            y=data,
            name=name,
            line=dict(color=color, width=2.5),
            mode="lines",
            fill="tozeroy" if fill_color else None,
            fillcolor=fill_color
        ))

    fig_e.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        title="Germany electricity generation share (%) 2000–2025",
        height=400,
        margin=dict(l=10, r=10, t=40, b=30)
    )

    st.plotly_chart(fig_e, use_container_width=True)


    st.markdown('<div class="section-header">Key milestones — Energiewende</div>', unsafe_allow_html=True)
    milestones = [
        ("2000", "Renewable Energy Act (EEG) passed — feed-in tariffs introduced"),
        ("2011", "Nuclear phase-out decided after Fukushima — 8 reactors shut immediately"),
        ("2017", "Renewables exceed 35% of electricity for first time"),
        ("2021", "Coal phase-out law — all coal plants to close by 2038"),
        ("2022", "Energy crisis (Russia-Ukraine) — accelerated renewable expansion"),
        ("2023", "Last 3 nuclear plants shut down — Germany fully nuclear-free"),
        ("2024", "Renewables hit 65%+ of electricity generation"),
        ("2030 target", "80% renewable electricity — 215 GW solar + 115 GW wind"),
    ]
    for year, event in milestones:
        st.markdown(
            f'<div class="info-card" style="display:flex;gap:12px;align-items:start;">'
            f'<span class="badge badge-orange" style="white-space:nowrap;margin-top:2px;">{year}</span>'
            f'<p style="margin:0;">{event}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────────────────────
# PAGE 7 — VISA & STAY
# ─────────────────────────────────────────────────────────────
elif page == "🪪 Visa & Stay":
    st.title("🪪 Visa & Staying in Germany")
    st.markdown("*Student visa, residence permit, and post-graduation options*")

    v1, v2, v3, v4 = st.columns(4)
    for col, val, lbl in [
        (v1, "90 days", "Visa-free entry (most countries)"),
        (v2, "18 months", "Job-seeker visa after graduation"),
        (v3, "21 months", "EU Blue Card fast-track"),
        (v4, "5 years", "Permanent residence eligibility"),
    ]:
        col.markdown(f'<div class="metric-card"><div class="metric-value">{val}</div>'
                     f'<div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 Step-by-step — arriving as a student</div>',
                unsafe_allow_html=True)

    steps = [
        ("1️⃣ Before you arrive", "badge-blue",
         "Get student visa (§16b AufenthG) at German embassy in your country. Need: university admission letter, financial proof (€10,332/year blocked account), health insurance, accommodation proof."),
        ("2️⃣ Anmeldung (registration)", "badge-green",
         "Register your address at local Einwohnermeldeamt within 2 weeks of arrival. You get Meldebescheinigung — essential for bank account, Steuer-ID, SIM card."),
        ("3️⃣ Residence permit", "badge-orange",
         "Apply for Aufenthaltserlaubnis at Ausländerbehörde before visa expires. Bring: passport, Anmeldung, enrollment certificate, insurance, biometric photo, €100 fee."),
        ("4️⃣ During studies", "badge-purple",
         "Renew residence permit each year or per semester. Maintain 120-day work limit. If extending studies, inform Ausländerbehörde early — don't let permit expire!"),
        ("5️⃣ After graduation", "badge-blue",
         "Apply for 18-month job-seeker visa (§20 AufenthG). Work any job while searching. Once you find sustainability job (€45,800+ salary), switch to EU Blue Card."),
        ("6️⃣ Permanent residence", "badge-green",
         "After 5 years (or 21 months with EU Blue Card + B1 German), apply for Niederlassungserlaubnis. Need: stable income, language skills, pension contributions, no criminal record."),
    ]

    for title, badge_class, desc in steps:
        st.markdown(
            f'<div class="info-card">'
            f'<h4><span class="badge {badge_class}">{title}</span></h4>'
            f'<p style="margin-top:8px;">{desc}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🌱 SustainIQ | Data: EM-DAT · EEA · IPCC AR6 · BMAS · BAMF | Built with Streamlit + Plotly + Claude AI")
