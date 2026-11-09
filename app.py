import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import re
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
# COMPREHENSIVE PETROCHEMICAL TRADES REPOSITORY
# ---------------------------------------------------------
MANPOWER_CATALOG = {
    "Supervisory & Inspection": [
        "Shift Operations Supervisor (Cracker / Polymers / Utilities)",
        "Mechanical Maintenance Turnaround (TAM) Supervisor",
        "Electrical & Instrumentation (E&I) Supervisor",
        "QA/QC Inspector (API 510/570/653 / CSWIP Certified)",
        "Plant EHSS Safety Inspector (NEBOSH / OSHA Certified)",
        "Turnaround (TAM) Execution Planner / Scheduler (Primavera P6)",
        "Scaffolding Supervisor & Inspector (CISRS / CITB Standard)"
    ],
    "Operations & Commissioning": [
        "DCS / Board Console Operator (Cracker / Utilities / Olefins)",
        "Outside Petrochemical Field Operator (Chemical / Polymers)",
        "Utilities Outside Operator (Boilers, Desal, Water Treatment)",
        "Commissioning & Start-Up Specialist"
    ],
    "Skilled Mechanical & Static Craft": [
        "Certified Millwright / Rotating Equipment Specialist (Turbines/Pumps)",
        "6G Inconel / Alloy / Titanium Welder (TIG/SMAW GTAW)",
        "High-Pressure Piping Fabricator & Pipefitter",
        "Valve Lapping, Overhaul & PSV Calibration Technician",
        "Hydrojetting Blast Operator (10k to 40k PSI Certified)",
        "Inert Atmosphere Catalyst Handling Technician (Confined Space)",
        "Aramco / RCJY Certified Rigger (Level I / II / III)"
    ],
    "Skilled Electrical, Instrumentation & Inspection": [
        "Instrumentation Calibration & Online Analyzer Technician",
        "High Voltage / Substation Relay & Transformer Technician",
        "DCS / PLC Loop & Logic Maintenance Technician",
        "NDT Technician (Level II RT, UT, MPI, DPI, Eddy Current)",
        "Transformer Oil Sampling & Testing Specialist"
    ],
    "Semi-Skilled & General Plant Support": [
        "Certified Scaffolder / Scaffolding Erector",
        "Industrial Painter / Grit Blaster / Insulator (SIP)",
        "Mechanical Fitter Assistant / Helper",
        "Materials Controller / Warehouse Expeditor",
        "General Industrial Laborer / Site Hand"
    ]
}

# ---------------------------------------------------------
# PETROCHEMICAL INDUSTRIAL RENTAL ASSET CATALOG
# ---------------------------------------------------------
RENTAL_CATALOG = {
    "Heavy Cranes & Rigging": [
        "Heavy All-Terrain Mobile Crane (100T to 250T Telescopic)",
        "Heavy All-Terrain Mobile Crane (300T to 500T Telescopic)",
        "Lattice Boom Heavy Crawler Crane (600T to 1200T Column Lifter)",
        "Rough Terrain Mobile Crane (30T to 80T)",
        "Boom Truck / Hiab (10T to 20T with Winch & Basket)",
        "Self-Propelled Modular Transporter (SPMT Axle Lines)"
    ],
    "Industrial Power, Generation & Lighting": [
        "Prime Diesel Generator (250 kVA to 500 kVA - Sound Attenuated)",
        "Prime Diesel Generator (750 kVA to 1250 kVA - Synchronized Parallel Set)",
        "ATEX / Zone-2 Explosion-Proof Generator (Petrochemical Battery Limits)",
        "Solar / Diesel Hybrid Mobile Light Tower (4x1000W LED)",
        "Resistive / Reactive Load Bank Skid (500 kW to 2000 kW)",
        "Step-Up / Step-Down Distribution Transformer (400V to 13.8kV)"
    ],
    "Compressed Air, Nitrogen & Process Utilities": [
        "100% Oil-Free Class-0 Diesel Air Compressor (750 to 1600 CFM, 10-14 Bar)",
        "Electric Driven Zero-Emission Air Compressor (1000 CFM)",
        "High-Pressure Instrument Air Desiccant Dryer (-40°C Dewpoint)",
        "Mobile Membrane Nitrogen Generation Unit (95% to 99.9% Purity)",
        "Air Receiver Tanks & High-Pressure Manifolds (10,000 Liters)"
    ],
    "Specialized Turnaround & In-Situ Tooling": [
        "Aerial / Truck-Mounted Heat Exchanger Bundle Puller (25T to 45T)",
        "Ultra-High-Pressure Hydrojetting Unit (15,000 to 40,000 PSI Skid)",
        "Industrial Vacuum Truck / Super-Sucker (Wet & Dry Sludge)",
        "On-Site Flange Facing & Pipe Cold-Cutting Clamshell Lathes",
        "Hydraulic Torque Wrench & Multi-Stud Tensioning Power Pack",
        "Orbital Pipe Welding System & Tube-to-Tubesheet System",
        "Post-Weld Heat Treatment (PWHT) 6-Way Induction Console",
        "High-Pressure Hydrostatic Test Pump & Chart Recorder Skid"
    ],
    "Scaffolding, Access & Modular Site Facilities": [
        "Modular Cuplock Industrial Scaffolding System (Metric Ton Package)",
        "Articulated 4x4 Rough Terrain Manlift (20m to 43m Boom Lift)",
        "Electric / Diesel Rough Terrain Scissor Lift (10m to 18m)",
        "Blast-Resistant Modular Office / Control Cabin (Zone-2 Rated)"
    ]
}

# ---------------------------------------------------------
# PARENT CATEGORY TAXONOMY
# ---------------------------------------------------------
CATEGORY_TAXONOMY = {
    "Manpower Supply": [
        "Plant & Technical Maintenance Manpower",
        "Process Control & DCS Operations Technicians",
        "Supplementary Support Manpower",
        "Certified Shutdown / TAM Surge Craft Labor",
        "HCIS Certified Industrial Security Staffing",
        "Professional Manpower & IT/Cyber Secondment"
    ],
    "Rental Services": [
        "Heavy Mobile Cranes & Heavy Rigging Lifting",
        "Oil-Free Air Compressors & Nitrogen Systems",
        "Explosion-Proof & Industrial Power Generators",
        "In-Situ Machining, Flange Facing & Tooling",
        "Modular Scaffolding & Site Access Systems",
        "Earthmoving & Site Civil Construction Fleet",
        "Modular Blast-Resistant Site Cabins & Offices"
    ],
    "Logistics Services": [
        "Ocean Freight", "Export Freight Forwarding", "KSA Inland Transportation",
        "Cross-Border Inland (GCC)", "Air Freight & Courier", "Warehousing & Open Yard",
        "Terminal, Port & Hub (KFIP/Dammam)", "Container / ISO Tank", "Bagging & Packing",
        "Container Operations", "Loading & Unloading", "Product Shuttling (Plant to Port)",
        "Import Freight Forwarding", "Customs Clearance"
    ],
    "Industrial O&M Services": [
        "Mechanical Maintenance (Piping, Static, Valves)", "Rotating Equipment Overhaul (Turbines/Compressors)",
        "Electrical Maintenance (Motors, VFDs, Switchgear)", "Instrumentation & Control (Analyzers, DCS)",
        "Inspection & Testing (NDT, RBI, Lifting)", "Industrial Cleaning (Hydrojetting 10k-40k PSI)",
        "Catalyst Handling under Inert Atmosphere", "Building & Civil Maintenance",
        "Material Handling Equipment Maintenance", "Safety & Fire Protection Systems Maintenance"
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
    "Professional & Consultancy": [
        "Engineering Design & Licensor TSA (GES/GES+)", "Process Safety & HAZOP / SIL Studies",
        "Legal & Regulatory Advisory (Trade, REACH/KKDIK)", "Financial Audit & Tax Advisory (ZATCA)",
        "Corporate Strategy & Operating Model Optimization", "Petrochemical Feasibility & Market Forecasting"
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
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.title("🏭 Category Management ToolKit")
st.sidebar.caption("Jubail Industrial City | Petrochemical Services & Projects")

# Read Secret automatically
secret_key = st.secrets.get("GEMINI_API_KEY", "")

api_key_input = st.sidebar.text_input(
    "Google AI Studio API Key",
    type="password",
    value=secret_key if secret_key else st.session_state.get("api_key", ""),
    help="Pre-loaded securely from Streamlit Secrets"
)
if api_key_input:
    st.session_state["api_key"] = api_key_input

st.sidebar.markdown("---")

selected_parent = st.sidebar.selectbox("1. Parent Category", list(CATEGORY_TAXONOMY.keys()))
sub_options = CATEGORY_TAXONOMY[selected_parent]
selected_sub = st.sidebar.selectbox("2. Subcategory", sub_options)
selected_analysis = st.sidebar.selectbox("3. Analysis Tool", ANALYSIS_TYPES)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Technical Sourcing Parameters")

extra_context = ""

# DYNAMIC PARAMETERS: MANPOWER SUPPLY
if selected_parent == "Manpower Supply":
    nationality_model = st.sidebar.selectbox(
        "Nationality Profile",
        ["Saudi National (Nitaqat / Saudization Target, GOSI 11.75%)",
         "Expatriate Worker (Maktab Amal Levy, Iqama, Ajeer/Qiwa)",
         "Blended Crew (30% Saudi / 70% Expat Compliant)"]
    )
    job_family = st.sidebar.selectbox("Job Family Grouping", list(MANPOWER_CATALOG.keys()))
    specific_trade = st.sidebar.selectbox("Specific Job Title / Trade", MANPOWER_CATALOG[job_family])
    headcount = st.sidebar.slider("Headcount Quantity (Workers)", min_value=1, max_value=300, value=20, step=1)
    duration_months = st.sidebar.selectbox("Contract Duration", [1, 2, 3, 6, 12, 24, 36], index=4, format_func=lambda x: f"{x} Month(s)")
    shift_pattern = st.sidebar.radio("Working Shift Pattern", ["8 Hours/Day (Standard Maintenance)", "10 Hours/Day (Extended)", "12 Hours/Day (24/7 TAM Shutdown Shift)"])
    extra_context = f"Profile: {nationality_model} | Family: {job_family} | Role: {specific_trade} | Qty: {headcount} workers | Duration: {duration_months} Months | Shift: {shift_pattern}."

# DYNAMIC PARAMETERS: RENTAL SERVICES
elif selected_parent == "Rental Services":
    eq_category = st.sidebar.selectbox("Equipment Family", list(RENTAL_CATALOG.keys()))
    specific_eq = st.sidebar.selectbox("Specific Asset / Rig Specification", RENTAL_CATALOG[eq_category])
    lease_model = st.sidebar.radio("Commercial Lease Model", ["Wet Lease (Equipment + Certified Operator + Fuel/Maint + RCJY Inspection)", "Dry Lease (Bare Equipment Only)"])
    qty_units = st.sidebar.number_input("Equipment Quantity (Units)", min_value=1, max_value=50, value=2)
    rental_tenure = st.sidebar.selectbox("Rental Tenure", ["1 Month (Shutdown Window)", "3 Months", "6 Months", "12 Months Long-Term"])
    extra_context = f"Asset Family: {eq_category} | Asset: {specific_eq} | Qty: {qty_units} units | Model: {lease_model} | Tenure: {rental_tenure}."

# DYNAMIC PARAMETERS: LOGISTICS (OCEAN FREIGHT)
elif selected_sub == "Ocean Freight":
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        origin_port = st.text_input("Origin Port", "King Fahd Industrial Port (KFIP - Jubail)")
    with col_b:
        dest_port = st.text_input("Destination Port", "Mundra Port, India")
    container_spec = st.sidebar.selectbox("Container Size / Cargo Type", ["40ft High Cube (Polymer Pellets)", "20ft GP Container", "ISO Tank Container (Liquid Chemicals)"])
    incoterm = st.sidebar.selectbox("Incoterm", ["FOB Jubail (KFIP)", "CFR Destination Port", "CIF Destination Port"])
    extra_context = f"Route: {origin_port} to {dest_port} | Container: {container_spec} | Incoterm: {incoterm}."

default_scope = f"Petrochemical manufacturing facility in Jubail Industrial City. {extra_context}"
scope_context = st.sidebar.text_area("4. Project / Route / Scope Details", value=default_scope, height=80)
run_btn = st.sidebar.button("🚀 Run Strategic Analysis", use_container_width=True)

# ---------------------------------------------------------
# DEFAULT BENCHMARKS (GRANULAR MICRO-COSTS & VENDOR MATRIX)
# ---------------------------------------------------------
DEFAULT_DATABASE = {
    "Should-Cost & Cost Breakdown Structure (CBS)": {
        "analysis_title": "Granular Should-Cost & Micro-CBS Model",
        "currency_or_unit": "SAR",
        "total_metric_value": 450000,
        "total_metric_label": "Total Should-Cost",
        "metric_card_2_label": "Direct Operating Cost",
        "metric_card_2_value": "SAR 396,000 (88%)",
        "metric_card_3_label": "Supplier Net Profit",
        "metric_card_3_value": "SAR 54,000 (12%)",
        "metric_card_4_label": "Target Benchmark Counter",
        "metric_card_4_value": "8.5% (CIPS Benchmark)",
        "chart_title": "Micro-Cost Factor Breakdown (8-12 Line Items)",
        "chart_items": [
            {"name": "1. Direct Basic Take-Home Wages", "value": 160000, "details": "Core net base monthly wage paid to deployed technicians in Jubail."},
            {"name": "2. GOSI & Social Insurance (KSA)", "value": 32000, "details": "Mandatory Saudi occupational hazard (2% expat) or social insurance (11.75% Saudi)."},
            {"name": "3. Maktab Amal & Iqama Fees", "value": 38400, "details": "Ministry of Human Resources expat work permit and levy fees (pass-through)."},
            {"name": "4. CCHI Health Insurance (Class B/A)", "value": 24000, "details": "Medical insurance coverage compliant with Council of Cooperative Health Insurance."},
            {"name": "5. RCJY Camp Housing & Utilities", "value": 48000, "details": "Royal Commission approved bachelor camp lodging and utility costs in Jubail."},
            {"name": "6. Site Transportation & Shuttle Buses", "value": 24000, "details": "Daily bus transport between RCJY camps and plant security gates."},
            {"name": "7. Industrial Catering (3 Meals/Day)", "value": 33600, "details": "Subsidized industrial food services conforming to Jubail hygiene standards."},
            {"name": "8. PPE, Safety Gear & Safety Passports", "value": 16000, "details": "Nomex coveralls, safety footwear, H2S monitors, SABIC/Aramco safety badging."},
            {"name": "9. Statutory Flight Ticket & ESB Accrual", "value": 20000, "details": "Annual leave airfare allowance and Labor Law End-of-Service benefit accrual."},
            {"name": "10. Contractor Corporate SG&A Overhead (8%)", "value": 36000, "details": "Contractor head-office administration, HR, and HSE management."},
            {"name": "11. Contractor Net Margin (12%)", "value": 54000, "details": "Contractor profit margin across the project lifecycle."}
        ],
        "secondary_chart_title": "Direct Site Cost vs. Contractor Overhead & Profit",
        "secondary_chart_labels": ["Direct Site Labor & Overheads", "Contractor SG&A & Profit"],
        "secondary_chart_values": [360000, 90000],
        "vendor_matrix": {
            "tier_1_local": ["Al-Yusr Industrial Contracting (AYTB)", "Sendan International", "Nesma & Partners", "Nasser S. Al-Hajri (NSH)"],
            "tier_2_regional": ["Safari Company", "Tamimi Global", "Rezayat Group", "Expertise Contracting"],
            "global_oems": ["Yokogawa Middle East", "Emerson Automation Solutions", "Baker Hughes", "Siemens Energy"]
        },
        "strategic_insights": {
            "summary": "High-granularity micro-cost model isolating statutory pass-throughs from addressable contractor labor markups.",
            "market_benchmark_range": "SAR 440,000 - SAR 490,000 for standard Eastern Province crew packages",
            "key_drivers_or_forces": [
                "Strict enforcement of MHRSD expat levy and Qiwa wage protection compliance.",
                "RCJY industrial housing availability drives high accommodation costs during turnarounds.",
                "Contractor margin stacking on insurance and visa statutory pass-through items."
            ],
            "buyer_actionable_levers": [
                "Audit Maktab Amal fees: require transparent pass-through billing with zero contractor markup.",
                "Enforce master rate card based on clean basic wages + fixed statutory multiplier.",
                "Consolidate accommodation booking through company-managed camp agreements."
            ]
        }
    }
}

# ---------------------------------------------------------
# GEMINI 3.8 FLASH WITH AUTOMATIC 503 RETRY LOGIC
# ---------------------------------------------------------
def fetch_analysis_via_direct_api(parent, sub, context, analysis_type, user_key):
    import urllib3
    import time
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    clean_key = str(user_key).strip().strip('"').strip("'")

    prompt = f"""You are the Principal Sourcing & Cost Engineer in Jubail Industrial City, Saudi Arabia for a world-scale Petrochemical Complex.
Analyze the following scope with HIGH GRANULARITY (Break down into 8 to 12 distinct cost items):
- Parent Category: {parent}
- Subcategory: {sub}
- Selected Tool: {analysis_type}
- Technical Parameters & Scope: {context}

CRITICAL RULES:
1. If Manpower: Reflect exact nationality profile (Saudi GOSI 11.75% vs Expat Maktab Amal fees). Break down: Basic Wages, GOSI, Maktab Amal/Iqama, Medical Insurance, RCJY Camp Housing, Transportation, Catering, PPE/Safety Badging, Flights/ESB, SG&A Overhead, Net Margin.
2. If Rental Services: Break down: Asset Depreciation, Preventative Maintenance, 3rd Party/CIC Load Test Cert, Certified Operator/Rigger Wage, Mobilization/Float Haulage, Consumables/Lube, Standby Allowance, Insurance, Contractor Margin.
3. If Logistics / Ocean Freight: Break down: Ocean Base Steaming Slot, Bunker Adjustment Factor (BAF), Emergency/Cape Rerouting Surcharge, Origin THC (KFIP), Destination THC, Equipment Imbalance (EIS), Low Sulfur Fuel (LSS), War Risk (WRS), Bill of Lading (B/L), Export Customs Clearance, Demurrage Buffer.
4. Populate a verified Vendor Landscape Matrix: Tier-1 Local KSA (IKTVA leaders), Tier-2 Regional, and Global OEMs/Foreign specialists relevant to this exact category in Eastern Province.

Return ONLY a valid JSON object matching this exact schema:
{{
  "analysis_title": "{analysis_type}",
  "currency_or_unit": "SAR",
  "total_metric_value": 450000,
  "total_metric_label": "Total Should-Cost / Score",
  "metric_card_2_label": "Direct Operating Cost / Profit Impact",
  "metric_card_2_value": "SAR 396,000 (88%)",
  "metric_card_3_label": "Supplier Profit / Supply Risk",
  "metric_card_3_value": "SAR 54,000 (12%)",
  "metric_card_4_label": "Target Benchmark / Posture",
  "metric_card_4_value": "8.5% / Strategic",
  "chart_title": "Granular Factor Breakdown (8-12 Micro-Items)",
  "chart_items": [
    {{"name": "Cost Line 1", "value": 120000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 2", "value": 80000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 3", "value": 60000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 4", "value": 45000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 5", "value": 35000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 6", "value": 30000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 7", "value": 25000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 8", "value": 20000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 9", "value": 18000, "details": "Detailed technical explanation"}},
    {{"name": "Cost Line 10", "value": 17000, "details": "Detailed technical explanation"}}
  ],
  "vendor_matrix": {{
    "tier_1_local": ["Vendor A (KSA/Jubail)", "Vendor B (KSA)", "Vendor C"],
    "tier_2_regional": ["Regional Contractor 1", "Regional Contractor 2"],
    "global_oems": ["Global OEM 1", "Global OEM 2"]
  }},
  "kraljic_data": {{
    "quadrant": "Strategic",
    "profit_impact": 8.5,
    "supply_risk": 7.5,
    "contract_horizon": "3 to 5 Years Alliance",
    "supplier_relationship": "Collaborative Partnership"
  }},
  "risk_items": [
    {{"risk_name": "Craft Labor Scarcity / Schedule Delay", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "Early reservation 9 months ahead.", "owner": "Turnaround Procurement Lead"}},
    {{"risk_name": "HCIS / RCJY Security Gate Pass Bottleneck", "prob": 4, "impact": 3.5, "score": 14, "severity": "High", "mitigation": "Submit digital dossiers 45 days prior.", "owner": "Security Liaison"}},
    {{"risk_name": "Process Safety Subcontractor Incident", "prob": 2, "impact": 5.0, "score": 10, "severity": "High", "mitigation": "Safety passport audits & stop-work authority.", "owner": "Plant EHSS"}},
    {{"risk_name": "Qiwa / Nitaqat Quota Freeze", "prob": 3, "impact": 3.0, "score": 9, "severity": "Medium", "mitigation": "Monthly audit of green-zone status in Qiwa.", "owner": "Contract Compliance"}},
    {{"risk_name": "Specialized Fitting / Spare Stockout", "prob": 2, "impact": 4.0, "score": 8, "severity": "Medium", "mitigation": "Consignment inventory at Jubail warehouse.", "owner": "Reliability Specialist"}}
  ],
  "secondary_chart_title": "Direct Cost vs. Contractor Overhead & Profit",
  "secondary_chart_labels": ["Direct Operating Pass-Through", "Contractor SG&A & Margin"],
  "secondary_chart_values": [88, 12],
  "strategic_insights": {{
    "summary": "Executive summary of findings grounded in Jubail industrial reality",
    "market_benchmark_range": "Prevailing benchmark range in SAR or USD",
    "key_drivers_or_forces": ["Key Driver 1", "Key Driver 2", "Key Driver 3"],
    "buyer_actionable_levers": ["Action Lever 1", "Action Lever 2", "Action Lever 3"]
  }}
}}
No markdown fences, no conversational text. JSON only."""

    def parse_json_from_text(raw_text):
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return None

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": clean_key
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.1,
            "maxOutputTokens": 3500,
            "thinkingConfig": {
                "thinkingLevel": "LOW"
            }
        }
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
    last_err = None

    # Automated 3-attempt retry loop with exponential backoff for 503 spikes
    for attempt in range(3):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=120)
            if r.status_code == 200:
                resp_json = r.json()
                text_out = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                parsed = parse_json_from_text(text_out)
                if parsed:
                    return parsed
            elif r.status_code in [503, 429]:
                # Server busy spike: pause 2 seconds on attempt 1, 4 seconds on attempt 2
                time.sleep(2 * (attempt + 1))
                last_err = f"HTTP {r.status_code} (Temporary Server Demand Spike)"
                continue
            else:
                last_err = f"HTTP {r.status_code}: {r.text[:200]}"
                break
        except Exception as e:
            last_err = str(e)
            time.sleep(2)

    raise Exception(f"Gemini 3.8 Flash: {last_err}")
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
        with st.spinner(f"Engineering granular micro-breakdown for {selected_sub}..."):
            try:
                st.session_state["active_data"] = fetch_analysis_via_direct_api(
                    selected_parent, selected_sub, scope_context, selected_analysis, active_key
                )
                st.session_state["active_tool"] = selected_analysis
                st.success(f"✅ Granular {selected_analysis} generated successfully via Gemini!")
            except Exception as e:
                st.error(f"Error fetching data from Gemini: {str(e)}")
    else:
        st.warning("⚠️ Enter your Google AI Studio API Key in the left sidebar to generate custom models.")

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
# STANDARD VIEW: BAR CHART & FACTOR BREAKDOWN (8-12 ITEMS)
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
                height=450,
                margin=dict(l=10, r=10, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("📋 Micro-Cost Factor Table")
        if not df_chart.empty:
            tbl = df_chart[["name", "value", "Percentage"]].copy()
            tbl.columns = ["Cost Component", f"Amount ({unit})", "Share (%)"]
            if unit in ["SAR", "USD"]:
                tbl[f"Amount ({unit})"] = tbl[f"Amount ({unit})"].apply(lambda x: f"{unit} {x:,.2f}")
                tbl["Share (%)"] = tbl["Share (%)"].apply(lambda x: f"{x:.1f}%")
            else:
                tbl[f"Amount ({unit})"] = tbl[f"Amount ({unit})"].apply(lambda x: f"{x:,.0f} pts")
                tbl["Share (%)"] = tbl["Share (%)"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(tbl, use_container_width=True, height=420)

    st.markdown("---")
    st.subheader("📚 Micro-Cost Factor Definitions & Engineering Basis")
    if not df_chart.empty and "details" in df_chart.columns:
        cols = st.columns(2)
        for idx, row in df_chart.iterrows():
            with cols[idx % 2]:
                amt_str = f"{unit} {row['value']:,.2f} ({row['Percentage']:.1f}%)" if unit in ["SAR", "USD"] else f"{row['value']} pts"
                with st.expander(f"🔹 **{row['name']}** — {amt_str}", expanded=True):
                    st.write(row.get("details", "-"))

# ---------------------------------------------------------
# ROW 4: STRATEGIC SPLIT & MARKET BENCHMARK INSIGHTS
# ---------------------------------------------------------
st.markdown("---")
col_pie, col_ins = st.columns([1, 1])

with col_pie:
    st.subheader(f"💼 {data.get('secondary_chart_title', 'Cost Allocation')}")
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

# ---------------------------------------------------------
# ROW 5: PREFERRED VENDOR & OEM LANDSCAPE (JUBAIL / KSA)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🏢 Preferred Vendor Landscape & OEM Supplier Matrix")
st.caption("Prequalified & Accredited Suppliers in Jubail Industrial City & Eastern Province")

vm = data.get("vendor_matrix", {
    "tier_1_local": ["Al-Yusr Industrial Contracting (AYTB)", "Sendan International", "Nesma & Partners", "Nasser S. Al-Hajri (NSH)"],
    "tier_2_regional": ["Safari Company", "Tamimi Global", "Rezayat Group", "Expertise Contracting"],
    "global_oems": ["Yokogawa Middle East", "Emerson Automation Solutions", "Baker Hughes", "Siemens Energy"]
})

v_col1, v_col2, v_col3 = st.columns(3)

with v_col1:
    st.markdown("🟢 **Tier-1 Local KSA (High IKTVA Champions):**")
    for v in vm.get("tier_1_local", []):
        st.markdown(f"- **{v}**")

with v_col2:
    st.markdown("🟡 **Tier-2 Regional Specialized Contractors:**")
    for v in vm.get("tier_2_regional", []):
        st.markdown(f"- **{v}**")

with v_col3:
    st.markdown("🌐 **Global OEMs & Technology Providers:**")
    for v in vm.get("global_oems", []):
        st.markdown(f"- **{v}**")
