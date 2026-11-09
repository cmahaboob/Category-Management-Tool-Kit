import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import re
import time
import requests

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Category Management ToolKit Engine",
    page_icon="🏭",
    layout="wide"
)

# ---------------------------------------------------------
# TAXONOMY REPOSITORY (Jubail Petrochemical Complex)
# ---------------------------------------------------------
CATEGORY_TAXONOMY = {
    "Industrial O&M Services": [
        "Mechanical Maintenance (Piping, Static, Valves)", "Rotating Equipment Overhaul (Turbines/Compressors)",
        "Electrical Maintenance (Motors, VFDs, Switchgear)", "Instrumentation & Control (Analyzers, DCS)",
        "Inspection & Testing (NDT, RBI, Lifting)", "Industrial Cleaning (Hydrojetting 10k-40k PSI)",
        "Catalyst Handling under Inert Atmosphere", "Building & Civil Maintenance",
        "Material Handling Equipment Maintenance", "Safety & Fire Protection Systems Maintenance"
    ],
    "Logistics Services": [
        "Ocean Freight", "Export Freight Forwarding", "KSA Inland Transportation",
        "Cross-Border Inland (GCC)", "Air Freight & Courier", "Warehousing & Open Yard",
        "Terminal, Port & Hub (KFIP/Dammam)", "Container / ISO Tank", "Bagging & Packing",
        "Container Operations", "Loading & Unloading", "Product Shuttling (Plant to Port)",
        "Import Freight Forwarding", "Customs Clearance"
    ],
    "Soft / Facility Management": [
        "Workplace Operations (Cleaning & Janitorial)", "Industrial & Camp Catering Services",
        "Property & Worker Accommodations Lease (RCJY)", "Pest Control & Vector Management",
        "Potable Water & Bulk Fluid Supply", "Corporate Security & Guard Force",
        "Office Renovation & Workplace Support", "Waste Management & Hazardous Fluid Handling"
    ],
    "IT & Digital Services": [
        "Enterprise Subscription & Renewal (ERP/Core)", "Strategic Platform Partnership (Cloud/Hyperscalers)",
        "Managed Services Framework (AMS/Infra)", "Network & Telecom Framework (Plant Connectivity)",
        "Cybersecurity & OT Risk Model (HCIS/NCA CSCC)", "End-User Computing & Hardware Catalog"
    ],
    "Project & Construction": [
        "Brownfield EPC / EPCM Plant Debottlenecking", "Civil Works & Deep Foundations",
        "Mechanical Piping Tie-ins & Structural Revamp", "Electrical & Instrumentation Installation",
        "Scaffolding & Insulation (SIP Packages)", "Plant Modification Management of Change (MOC)"
    ],
    "Rental Services": [
        "Heavy Mobile Cranes (100T to 1200T Telescopic/Crawler)", "Oil-Free Industrial Air Compressors",
        "Explosion-Proof / ATEX Power Generators", "Earthmoving & Site Civil Fleet",
        "Modular Blast-Resistant Site Cabins & Offices", "Boom Trucks & Manlifts"
    ],
    "Professional & Consultancy": [
        "Engineering Design & Licensor TSA (GES/GES+)", "Process Safety & HAZOP / SIL Studies",
        "Legal & Regulatory Advisory (Trade, REACH/KKDIK)", "Financial Audit & Tax Advisory (ZATCA)",
        "Corporate Strategy & Operating Model Optimization", "Petrochemical Feasibility & Market Forecasting"
    ],
    "Manpower Supply": [
        "Plant & Technical Maintenance Manpower", "Process Control & DCS Operations Technicians",
        "Supplementary Support Manpower", "Professional Manpower & IT/Cyber Secondment",
        "HCIS Certified Industrial Security Staffing", "Certified Shutdown / TAM Surge Craft Labor"
    ],
    "HSE and Compliance": [
        "HCIS Physical Security Compliance Infrastructure", "Environmental Emissions Testing (RCER 2020)",
        "Hazardous Petrochemical Waste Incineration", "Fixed Fire Suppression & Deluge Maintenance",
        "Personal Protective Equipment (PPE) Contracts"
    ]
}

ANALYSIS_TYPES = [
    "Should-Cost & Cost Breakdown Structure (CBS)",
    "Total Cost of Ownership (TCO) Lifecycle Model",
    "Kraljic Matrix Positioning & Strategic Portfolio",
    "Risk Assessment Scorecard, Heatmap & Mitigation Plan",
    "Porter's 5 Forces & Market Intelligence",
    "Kearney Purchasing Chessboard & Sourcing Strategy"
]

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🏭 Category Management ToolKit Engine")
st.sidebar.caption("Jubail Industrial City | Services & Projects")

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

api_key_input = st.sidebar.text_input(
    "Google AI Studio API Key",
    type="password",
    value=st.session_state["api_key"],
    help="Enter your Gemini key from aistudio.google.com"
)
if api_key_input:
    st.session_state["api_key"] = api_key_input

st.sidebar.markdown("---")

selected_parent = st.sidebar.selectbox("1. Parent Category", list(CATEGORY_TAXONOMY.keys()))
sub_options = CATEGORY_TAXONOMY[selected_parent]
selected_sub = st.sidebar.selectbox("2. Subcategory", sub_options)
selected_analysis = st.sidebar.selectbox("3. Analysis Tool", ANALYSIS_TYPES)

default_context = f"Scope in Jubail Industrial City petrochemical complex for {selected_sub}."
if selected_sub == "Ocean Freight":
    default_context = "Route: Jubail (King Fahd Industrial Port) to India (Mundra Port), 40ft High Cube Container, Petrochemical Polymer Pellets."
elif "Rotating Equipment" in selected_sub:
    default_context = "Turnaround (TAM) Rotating Equipment Overhaul: High-pressure multistage feed pumps, turbine rotor inspection, dynamic balancing inside Jubail 1 complex."
elif "Mechanical Maintenance" in selected_sub:
    default_context = "Turnaround (TAM) Mechanical Overhaul: Heat exchangers, valve overhaul, piping spool fabrication inside Jubail 1 complex."

scope_context = st.sidebar.text_area("4. Scope / Route / Project Details", value=default_context, height=85)
run_btn = st.sidebar.button("🚀 Run Strategic Analysis", use_container_width=True)

# ---------------------------------------------------------
# DEFAULT BENCHMARKS PER ANALYSIS TYPE
# ---------------------------------------------------------
DEFAULT_DATABASE = {
    "Should-Cost & Cost Breakdown Structure (CBS)": {
        "analysis_title": "Should-Cost & Cost Breakdown Structure (CBS)",
        "currency_or_unit": "SAR",
        "total_metric_value": 485000,
        "total_metric_label": "Total Should-Cost",
        "metric_card_2_label": "Direct Operating Cost",
        "metric_card_2_value": "SAR 436,500 (90%)",
        "metric_card_3_label": "Supplier Profit Margin",
        "metric_card_3_value": "SAR 48,500 (10%)",
        "metric_card_4_label": "Fair Target Counter",
        "metric_card_4_value": "8.0% (CIPS Benchmark)",
        "chart_title": "Cost Factor Breakdown",
        "chart_items": [
            {"name": "Direct Skilled Craft Labor", "value": 194000, "details": "Certified Pipefitters, 6G Alloy Welders, Millwrights, Riggers."},
            {"name": "KSA Statutory & Fringe Burden", "value": 97000, "details": "GOSI contributions, Iqama/Maktab Amal fees, CCHI Medical, End of Service."},
            {"name": "Field Overheads & Accommodation", "value": 63050, "details": "RCJY-approved camp housing in Jubail, daily shuttle bus, catering, badging."},
            {"name": "Tooling & Consumables", "value": 38800, "details": "Torque wrenches, hydro-testing pumps, blind flanges, welding rods, gaskets."},
            {"name": "Corporate SG&A Overhead (9%)", "value": 43650, "details": "Head-office QA/QC, Aramco/RCJY safety compliance administration."},
            {"name": "Contractor Profit Margin (10%)", "value": 48500, "details": "Fair contractor net margin for plant shutdown mechanical scopes."}
        ],
        "secondary_chart_title": "Direct Operating Cost vs. Supplier Profit Margin",
        "secondary_chart_labels": ["Direct Operating Cost", "Supplier Profit Margin"],
        "secondary_chart_values": [436500, 48500],
        "strategic_insights": {
            "summary": "Should-Cost clean-sheet model reflecting Eastern Province labor economics and RCJY industrial standards.",
            "market_benchmark_range": "SAR 470,000 - SAR 540,000",
            "key_drivers_or_forces": [
                "Scarcity of certified alloy welders and millwrights during peak winter turnaround windows.",
                "RCJY industrial housing and gate pass lead times inflate contractor standby costs.",
                "Subcontractor margin stacking on valve testing and third-party inspection."
            ],
            "buyer_actionable_levers": [
                "Unbundle statutory visa/Iqama fees: require transparent pass-through billing.",
                "Convert T&M call-outs to unit-rate milestone deliverables (per weld-inch, per valve).",
                "Enforce LCGPA local content credits for utilizing Jubail-based fabrication workshops."
            ]
        }
    }
}

# ---------------------------------------------------------
# GEMINI 3.8 FLASH OPTIMIZED CALL (FAST RESPONSE & 90S TIMEOUT)
# ---------------------------------------------------------
def fetch_analysis_via_direct_api(parent, sub, context, analysis_type, user_key):
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    prompt = (
        "You are the Principal Strategic Sourcing & Cost Engineer in Jubail Industrial City, Saudi Arabia for a world-scale Petrochemical Complex.\n"
        f"Perform an in-depth professional analysis for:\n"
        f"- Parent Category: {parent}\n"
        f"- Subcategory: {sub}\n"
        f"- Analysis Tool: {analysis_type}\n"
        f"- Scope Context: {context}\n\n"
        "ADAPT YOUR OUTPUT SPECIFICALLY TO THE REQUESTED ANALYSIS TOOL:\n"
        "1. Should-Cost (CBS): Detailed cost breakdown (Direct Labor, KSA Statutory Burden, Overheads, Consumables, Profit) in SAR or USD.\n"
        "2. TCO Lifecycle Model: Cost breakdown across lifecycle stages (Acquisition, Mobilization, O&M, Risk/Downtime Buffer, Demobilization) in SAR or USD.\n"
        "3. Kraljic Matrix: Position in 2x2 matrix (Strategic, Leverage, Bottleneck, Routine). Provide profit_impact (1-10), supply_risk (1-10), and strategic governance.\n"
        "4. Risk Assessment & Heatmap: 5 specific risks with probability (1-5), impact (1-5), score (prob x impact), severity (Critical/High/Medium/Low), concrete mitigation action, and named owner.\n"
        "5. Porter's 5 Forces: Score each force from 0 to 100 with unit 'Index (0-100)'.\n"
        "6. Kearney Chessboard: Quantify value potential across strategic levers in SAR or USD.\n\n"
        "RETURN ONLY A VALID JSON OBJECT MATCHING THIS EXACT SCHEMA (no markdown fences, no raw text):\n"
        """{
  "analysis_title": "string",
  "currency_or_unit": "SAR or USD or Score (1-10) or Score (1-25) or Index (0-100)",
  "total_metric_value": 450000,
  "total_metric_label": "string",
  "metric_card_2_label": "string",
  "metric_card_2_value": "string",
  "metric_card_3_label": "string",
  "metric_card_3_value": "string",
  "metric_card_4_label": "string",
  "metric_card_4_value": "string",
  "chart_title": "string",
  "chart_items": [
    {"name": "Item Name", "value": 150000, "details": "Detailed explanation"}
  ],
  "kraljic_data": {
    "quadrant": "Strategic or Leverage or Bottleneck or Routine",
    "profit_impact": 8.5,
    "supply_risk": 7.5,
    "contract_horizon": "string",
    "supplier_relationship": "string"
  },
  "risk_items": [
    {"risk_name": "Specific Risk Name", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "Concrete action", "owner": "Role Name"}
  ],
  "secondary_chart_title": "string",
  "secondary_chart_labels": ["Part A", "Part B"],
  "secondary_chart_values": [80, 20],
  "strategic_insights": {
    "summary": "Executive summary",
    "market_benchmark_range": "Benchmark description",
    "key_drivers_or_forces": ["Point 1", "Point 2", "Point 3"],
    "buyer_actionable_levers": ["Lever 1", "Lever 2", "Lever 3"]
  }
}"""
    )

    def parse_json_from_text(raw_text):
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return None

    def extract_text(data):
        if isinstance(data, dict):
            if "text" in data and isinstance(data["text"], str) and data["text"].strip():
                return data["text"]
            for v in data.values():
                t = extract_text(v)
                if t:
                    return t
        elif isinstance(data, list):
            for item in reversed(data):
                t = extract_text(item)
                if t:
                    return t
        return ""

    error_log = []

    # 1. Primary: Google Interactions API with gemini-3.8-flash & low thinking level for fast response
    try:
        interactions_url = f"https://generativelanguage.googleapis.com/v1beta/interactions?key={user_key}"
        headers = {"Content-Type": "application/json", "x-goog-api-key": user_key}
        payload = {
            "model": "gemini-3.8-flash",
            "input": prompt,
            "generation_config": {"thinking_level": "low"}
        }
        r1 = requests.post(interactions_url, headers=headers, json=payload, timeout=90, verify=False)
        if r1.status_code == 200:
            txt = extract_text(r1.json())
            parsed = parse_json_from_text(txt)
            if parsed:
                return parsed
        else:
            error_log.append(f"Interactions API: HTTP {r1.status_code}")
    except Exception as e:
        error_log.append(f"Interactions API: {str(e)}")

    # 2. Secondary: Direct generateContent endpoint with gemini-3.8-flash & gemini-3.5-flash
    modern_models = ["gemini-3.8-flash", "gemini-3.5-flash"]
    gen_payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json", "temperature": 0.2}
    }
    for m in modern_models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={user_key}"
            r2 = requests.post(url, headers={"Content-Type": "application/json"}, json=gen_payload, timeout=90, verify=False)
            if r2.status_code == 200:
                rj = r2.json()
                txt = rj["candidates"][0]["content"]["parts"][0]["text"]
                parsed = parse_json_from_text(txt)
                if parsed:
                    return parsed
            else:
                error_log.append(f"{m}: HTTP {r2.status_code}")
        except Exception as e:
            error_log.append(f"{m}: {str(e)}")

    raise Exception(" | ".join(error_log))
# ---------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------
default_model = DEFAULT_DATABASE.get(selected_analysis, DEFAULT_DATABASE["Should-Cost & Cost Breakdown Structure (CBS)"])

if "active_data" not in st.session_state or st.session_state.get("active_tool") != selected_analysis:
    st.session_state["active_data"] = default_model
    st.session_state["active_tool"] = selected_analysis

if run_btn:
    active_key = st.session_state.get("api_key", "").strip()
    if active_key:
        with st.spinner(f"Engineering live {selected_analysis} for {selected_sub}..."):
            try:
                st.session_state["active_data"] = fetch_analysis_via_direct_api(
                    selected_parent, selected_sub, scope_context, selected_analysis, active_key
                )
                st.session_state["active_tool"] = selected_analysis
                st.success(f"✅ Live {selected_analysis} generated successfully via Gemini!")
            except Exception as e:
                st.error(f"Error fetching data from Gemini: {str(e)}")
    else:
        st.warning("⚠️ Enter your Google AI Studio API Key in the left sidebar to generate custom models for new routes and scopes.")

data = st.session_state["active_data"]

# ---------------------------------------------------------
# DASHBOARD RENDERING ENGINE
# ---------------------------------------------------------
st.title("🏭 Category Management ToolKit Engine")
st.subheader(f"📌 {data.get('analysis_title', selected_analysis)}")
st.markdown(f"**Operating Hub:** Jubail Industrial City (KSA) | **Active Category:** `{selected_parent}` → `{selected_sub}`")
st.markdown("---")

unit = data.get("currency_or_unit", "SAR")
total_val = data.get("total_metric_value", 0)

# Process chart items
df_chart = pd.DataFrame(data.get("chart_items", []))
if not df_chart.empty and "value" in df_chart.columns:
    df_chart = df_chart.sort_values(by="value", ascending=False)
    if total_val > 0 and unit in ["SAR", "USD"]:
        df_chart["Percentage"] = (df_chart["value"] / total_val) * 100
    else:
        df_chart["Percentage"] = (df_chart["value"] / df_chart["value"].sum()) * 100

# ROW 1: 4 EXECUTIVE METRICS
col1, col2, col3, col4 = st.columns(4)
with col1:
    val_disp = f"{unit} {total_val:,.2f}" if unit in ["SAR", "USD"] else f"{total_val}"
    st.metric(label=data.get("total_metric_label", "Overall Metric"), value=val_disp)
with col2:
    st.metric(label=data.get("metric_card_2_label", "Primary Factor"), value=data.get("metric_card_2_value", "-"))
with col3:
    st.metric(label=data.get("metric_card_3_label", "Secondary Factor"), value=data.get("metric_card_3_value", "-"), delta_color="inverse")
with col4:
    st.metric(label=data.get("metric_card_4_label", "Benchmark Target"), value=data.get("metric_card_4_value", "-"), delta_color="off")

st.markdown("---")

# ---------------------------------------------------------
# SPECIALIZED VIEW A: KRALJIC MATRIX 2x2 QUADRANT MAP
# ---------------------------------------------------------
if "Kraljic" in selected_analysis:
    col_kraljic, col_table = st.columns([1.2, 0.8])
    k_data = data.get("kraljic_data", {"quadrant": "Strategic", "profit_impact": 8.5, "supply_risk": 7.5})
    
    with col_kraljic:
        st.subheader("🎯 Kraljic Portfolio Matrix (2x2)")
        fig_k = go.Figure()
        
        fig_k.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="#ECEFF1", opacity=0.4, line_width=0)
        fig_k.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="#FFF3E0", opacity=0.4, line_width=0)
        fig_k.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="#E0F2F1", opacity=0.4, line_width=0)
        fig_k.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="#FFEBEE", opacity=0.5, line_width=0)
        
        fig_k.add_annotation(x=2.5, y=2.5, text="<b>ROUTINE / NON-CRITICAL</b><br>(Simplify & Automate)", showarrow=False, font=dict(color="#546E7A", size=11))
        fig_k.add_annotation(x=7.5, y=2.5, text="<b>BOTTLENECK</b><br>(Secure Volume / Buffer)", showarrow=False, font=dict(color="#E65100", size=11))
        fig_k.add_annotation(x=2.5, y=7.5, text="<b>LEVERAGE</b><br>(Competitive Bidding)", showarrow=False, font=dict(color="#00695C", size=11))
        fig_k.add_annotation(x=7.5, y=7.5, text="<b>STRATEGIC</b><br>(Long-Term Partnership)", showarrow=False, font=dict(color="#C62828", size=11))
        
        p_x = k_data.get("supply_risk", 7.5)
        p_y = k_data.get("profit_impact", 8.5)
        fig_k.add_trace(go.Scatter(
            x=[p_x], y=[p_y],
            mode="markers+text",
            marker=dict(size=28, color="#D32F2F", line=dict(width=3, color="#FFFFFF")),
            text=[f"<b>{selected_sub}</b>"],
            textposition="top center",
            name="Category Position"
        ))
        
        fig_k.update_layout(
            xaxis=dict(title="<b>Supply Market Risk (Complexity / Scarcity) →</b>", range=[0, 10], showgrid=True),
            yaxis=dict(title="<b>Profit & Business Impact (Downtime Risk) →</b>", range=[0, 10], showgrid=True),
            height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_k, use_container_width=True)
        
    with col_table:
        st.subheader("📋 Kraljic Category Positioning Card")
        st.info(f"**Identified Quadrant:** `{k_data.get('quadrant', 'Strategic')}`")
        st.markdown(f"**Recommended Horizon:** {k_data.get('contract_horizon', '3-5 Years Alliance')}")
        st.markdown(f"**Relationship Model:** {k_data.get('supplier_relationship', 'Collaborative Gainshare')}")
        st.markdown("---")
        st.markdown("**Core Kraljic Dimensions:**")
        st.write(f"- **Profit Impact:** {k_data.get('profit_impact', 8.5)} / 10")
        st.write(f"- **Supply Risk:** {k_data.get('supply_risk', 7.5)} / 10")
        st.markdown("---")
        st.caption("📌 **Buyer Directive:** Align sourcing strategy with quadrant boundaries to prevent supplier lock-in.")

# ---------------------------------------------------------
# SPECIALIZED VIEW B: RISK ASSESSMENT 5x5 HEATMAP & MITIGATION
# ---------------------------------------------------------
elif "Risk" in selected_analysis:
    col_map, col_score = st.columns([1.1, 0.9])
    risk_list = data.get("risk_items", [])
    
    with col_map:
        st.subheader("🔥 5x5 Category Risk Heatmap")
        z_colors = [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 6, 9, 12, 15],
            [4, 8, 12, 16, 20],
            [5, 10, 15, 20, 25]
        ]
        
        fig_h = go.Figure(data=go.Heatmap(
            z=z_colors,
            x=["1. Negligible", "2. Minor", "3. Moderate", "4. Major", "5. Catastrophic"],
            y=["1. Rare", "2. Unlikely", "3. Possible", "4. Likely", "5. Almost Certain"],
            colorscale=[[0.0, "#A5D6A7"], [0.3, "#FFF59D"], [0.6, "#FFB74D"], [1.0, "#EF5350"]],
            showscale=False
        ))
        
        if risk_list:
            df_r = pd.DataFrame(risk_list)
            fig_h.add_trace(go.Scatter(
                x=[p - 1 for p in df_r["impact"]],
                y=[p - 1 for p in df_r["prob"]],
                mode="markers+text",
                marker=dict(size=20, color="#1A237E", line=dict(width=2, color="#FFFFFF")),
                text=[f"<b>R{i+1}</b>" for i in range(len(df_r))],
                textposition="top center",
                hovertext=[f"{r['risk_name']} (Score: {r['score']})" for _, r in df_r.iterrows()],
                name="Identified Risks"
            ))
            
        fig_h.update_layout(
            xaxis=dict(title="<b>Impact Severity (Asset / Compliance / Cost) →</b>"),
            yaxis=dict(title="<b>Probability (Likelihood) →</b>"),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_h, use_container_width=True)
        
    with col_score:
        st.subheader("📊 Risk Score Ranking")
        if risk_list:
            df_r = pd.DataFrame(risk_list)
            st_table = df_r[["risk_name", "prob", "impact", "score", "severity"]].copy()
            st_table.columns = ["Risk Factor", "Prob (1-5)", "Impact (1-5)", "Score (1-25)", "Severity"]
            st.dataframe(st_table, use_container_width=True, height=350)
            
    st.markdown("---")
    st.subheader("🛡️ Category Risk Mitigation Plan & Governance")
    if risk_list:
        for idx, r in enumerate(risk_list):
            with st.expander(f"⚠️ **R{idx+1}: {r['risk_name']}** — Score: `{r['score']}/25` | Severity: `{r['severity']}` | Accountable Owner: `{r['owner']}`", expanded=True):
                st.markdown(f"**Actionable Mitigation Strategy:** {r['mitigation']}")

# ---------------------------------------------------------
# STANDARD VIEW: BAR CHART & FACTOR BREAKDOWN
# ---------------------------------------------------------
else:
    col_chart, col_table = st.columns([1.1, 0.9])
    with col_chart:
        st.subheader(f"📊 {data.get('chart_title', 'Cost Breakdown')}")
        if not df_chart.empty:
            fig = px.bar(
                df_chart, x="value", y="name", orientation="h",
                text=df_chart.apply(
                    lambda r: f"{unit} {r['value']:,.0f} ({r['Percentage']:.1f}%)" if unit in ["SAR", "USD"] else f"{r['value']} pts",
                    axis=1
                ),
                color="value", color_continuous_scale="Tealgrn"
            )
            fig.update_layout(
                showlegend=False,
                yaxis=dict(autorange="reversed"),
                height=370,
                margin=dict(l=10, r=10, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("📋 Factor Breakdown")
        if not df_chart.empty:
            tbl = df_chart[["name", "value", "Percentage"]].copy()
            tbl.columns = ["Factor / Element", f"Value ({unit})", "Share (%)"]
            if unit in ["SAR", "USD"]:
                tbl[f"Value ({unit})"] = tbl[f"Value ({unit})"].apply(lambda x: f"{unit} {x:,.2f}")
                tbl["Share (%)"] = tbl["Share (%)"].apply(lambda x: f"{x:.1f}%")
            else:
                tbl[f"Value ({unit})"] = tbl[f"Value ({unit})"].apply(lambda x: f"{x:,.0f} pts")
                tbl["Share (%)"] = tbl["Share (%)"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(tbl, use_container_width=True, height=350)

    st.markdown("---")
    st.subheader("📚 Cost Factor Definitions & Technical Explanations")
    if not df_chart.empty and "details" in df_chart.columns:
        cols = st.columns(2)
        for idx, row in df_chart.iterrows():
            with cols[idx % 2]:
                amt_str = f"{unit} {row['value']:,.2f} ({row['Percentage']:.1f}%)" if unit in ["SAR", "USD"] else f"{row['value']} pts"
                with st.expander(f"🔹 **{row['name']}** — {amt_str}", expanded=True):
                    st.write(row.get("details", "-"))

# ---------------------------------------------------------
# STRATEGIC SPLIT & MARKET BENCHMARK INSIGHTS
# ---------------------------------------------------------
st.markdown("---")
col_pie, col_ins = st.columns([1, 1])

with col_pie:
    st.subheader(f"💼 {data.get('secondary_chart_title', 'Strategic Distribution')}")
    pie_labels = data.get("secondary_chart_labels", ["Direct Costs", "Overhead & Margin"])
    pie_vals = data.get("secondary_chart_values", [85, 15])
    
    donut_fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=pie_vals,
        hole=.55,
        marker_colors=["#1E88E5", "#00E676", "#FFB300", "#E53935"]
    )])
    donut_fig.update_layout(
        height=270,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(donut_fig, use_container_width=True)

with col_ins:
    st.subheader("💡 Strategic Insights & Buyer Action Plan")
    insights = data.get("strategic_insights", {})
    
    if "market_benchmark_range" in insights:
        st.info(f"**Benchmark / Market Reality:** {insights['market_benchmark_range']}")
        
    st.markdown("**🔍 Primary Drivers & Risk Triggers:**")
    for d in insights.get("key_drivers_or_forces", []):
        st.markdown(f"- {d}")
        
    st.markdown("**🎯 Recommended Buyer Counter-Measures:**")
    for l in insights.get("buyer_actionable_levers", []):
        st.markdown(f"- {l}")