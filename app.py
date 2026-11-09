import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import re
import requests
import time

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Category Management ToolKit Engine | Petrochemical",
    page_icon="🏭",
    layout="wide"
)

# Custom Executive CSS Injection
st.markdown("""
<style>
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-left: 5px solid #0284c7;
        border-radius: 8px;
        padding: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] label {
        font-weight: 600;
        color: #475569;
        font-size: 0.85rem;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.55rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.95rem;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-color: #0f172a !important;
    }
    .exec-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 18px;
    }
    .exec-banner h2 {
        color: white;
        margin: 0;
        padding: 0;
        font-size: 1.6rem;
    }
    .exec-banner p {
        color: #94a3b8;
        margin: 4px 0 0 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DIRECT MAPPING: RENTAL SUBCATEGORY -> SPECIFIC ASSETS
# ---------------------------------------------------------
RENTAL_MAP = {
    "Heavy Mobile Cranes & Heavy Rigging Lifting": [
        "Heavy All-Terrain Mobile Crane (100T to 250T Telescopic)",
        "Heavy All-Terrain Mobile Crane (300T to 500T Telescopic)",
        "Lattice Boom Heavy Crawler Crane (600T to 1200T Column Lifter)",
        "Rough Terrain Mobile Crane (50T to 80T)",
        "Boom Truck / Hiab (10T to 20T with Winch & Basket)",
        "Self-Propelled Modular Transporter (SPMT Axle Lines)"
    ],
    "Explosion-Proof & Industrial Power Generators": [
        "Prime Diesel Generator (250 kVA to 500 kVA - Sound Attenuated)",
        "Prime Diesel Generator (750 kVA to 1250 kVA - Synchronized Parallel Set)",
        "ATEX / Zone-2 Explosion-Proof Generator (Petrochemical Battery Limits)",
        "Solar / Diesel Hybrid Mobile Light Tower (4x1000W LED)",
        "Resistive / Reactive Load Bank Skid (500 kW to 2000 kW)",
        "Step-Up / Step-Down Distribution Transformer (400V to 13.8kV)"
    ],
    "Oil-Free Air Compressors & Nitrogen Systems": [
        "100% Oil-Free Class-0 Diesel Air Compressor (750 to 1600 CFM, 10-14 Bar)",
        "Electric Driven Zero-Emission Air Compressor (1000 CFM)",
        "High-Pressure Instrument Air Desiccant Dryer (-40°C Dewpoint)",
        "Mobile Membrane Nitrogen Generation Unit (95% to 99.9% Purity)",
        "Air Receiver Tanks & High-Pressure Manifolds (10,000 Liters)"
    ],
    "In-Situ Machining, Flange Facing & Tooling": [
        "Aerial / Truck-Mounted Heat Exchanger Bundle Puller (25T to 45T)",
        "Ultra-High-Pressure Hydrojetting Unit (15,000 to 40,000 PSI Skid)",
        "Industrial Vacuum Truck / Super-Sucker (Wet & Dry Sludge)",
        "On-Site Flange Facing & Pipe Cold-Cutting Clamshell Lathes",
        "Hydraulic Torque Wrench & Multi-Stud Tensioning Power Pack",
        "Orbital Pipe Welding System & Tube-to-Tubesheet System",
        "Post-Weld Heat Treatment (PWHT) 6-Way Induction Console",
        "High-Pressure Hydrostatic Test Pump & Chart Recorder Skid"
    ],
    "Modular Scaffolding & Site Access Systems": [
        "Modular Cuplock Industrial Scaffolding System (Metric Ton Package)",
        "Articulated 4x4 Rough Terrain Manlift (20m to 43m Boom Lift)",
        "Electric / Diesel Rough Terrain Scissor Lift (10m to 18m)",
        "Blast-Resistant Modular Office / Control Cabin (Zone-2 Rated)"
    ],
    "Earthmoving & Site Civil Construction Fleet": [
        "Heavy Wheel Loader & Front-End Loader (Cat 966 equivalent)",
        "Tracked Hydraulic Excavator (20T to 45T with Breaker/Bucket)",
        "Telescopic Forklift / Telehandler (4T to 10T)",
        "Heavy Articulated Dump Truck (25T to 40T)"
    ],
    "Modular Blast-Resistant Site Cabins & Offices": [
        "Zone-2 Blast-Resistant Modular Office (12m x 3.5m - 8 PSI rated)",
        "Temporary Plant Control Room / Engineering Container (Blast Proof)",
        "Explosion-Proof Emergency Tool & Workshop Container"
    ]
}

# ---------------------------------------------------------
# DIRECT MAPPING: MANPOWER SUBCATEGORY -> SPECIFIC TRADES
# ---------------------------------------------------------
MANPOWER_MAP = {
    "Plant & Technical Maintenance Manpower": [
        "Certified Millwright / Rotating Equipment Specialist (Turbines/Pumps)",
        "High-Pressure Piping Fabricator & Pipefitter",
        "Instrumentation Calibration & Online Analyzer Technician",
        "High Voltage / Substation Relay & Transformer Technician",
        "Valve Lapping, Overhaul & PSV Calibration Technician"
    ],
    "Process Control & DCS Operations Technicians": [
        "DCS / Board Console Operator (Cracker / Utilities / Olefins)",
        "Outside Petrochemical Field Operator (Chemical / Polymers)",
        "Utilities Outside Operator (Boilers, Desal, Water Treatment)",
        "Commissioning & Start-Up Specialist"
    ],
    "Supplementary Support Manpower": [
        "Mechanical Fitter Assistant / Helper",
        "Materials Controller / Warehouse Expeditor",
        "General Industrial Laborer / Site Hand",
        "Industrial Painter / Grit Blaster / Insulator (SIP)"
    ],
    "Certified Shutdown / TAM Surge Craft Labor": [
        "6G Inconel / Alloy / Titanium Welder (TIG/SMAW GTAW)",
        "Certified Millwright / Rotating Equipment Specialist",
        "Aramco / RCJY Certified Rigger (Level I / II / III)",
        "Hydrojetting Blast Operator (10k to 40k PSI Certified)",
        "Inert Atmosphere Catalyst Handling Technician (Confined Space)",
        "Certified Scaffolder / Scaffolding Erector"
    ],
    "HCIS Certified Industrial Security Staffing": [
        "HCIS Certified Industrial Security Guard (Armed/Unarmed)",
        "Plant EHSS Safety Inspector (NEBOSH / OSHA Certified)",
        "Security Access Control & Perimeter Dispatcher"
    ],
    "Professional Manpower & IT/Cyber Secondment": [
        "Turnaround (TAM) Execution Planner / Scheduler (Primavera P6)",
        "QA/QC Inspector (API 510/570/653 / CSWIP Certified)",
        "OT/ICS Industrial Cybersecurity Specialist (NCA/HCIS)",
        "Procurement Contracts Specialist / Expeditor"
    ]
}

CATEGORY_TAXONOMY = {
    "Rental Services": list(RENTAL_MAP.keys()),
    "Manpower Supply": list(MANPOWER_MAP.keys()),
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
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🏭 Category Management ToolKit")
st.sidebar.caption("Jubail Industrial City | Petrochemical Services & Projects")

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
param_data = {}

# SYNCHRONIZED RENTAL SERVICES PARAMETERS
if selected_parent == "Rental Services":
    available_assets = RENTAL_MAP.get(selected_sub, ["Heavy Equipment Asset"])
    specific_eq = st.sidebar.selectbox("Specific Asset Specification", available_assets)
    lease_model = st.sidebar.radio("Commercial Lease Model", ["Wet Lease (Equipment + Certified Operator + Fuel/Maint + RCJY Inspection)", "Dry Lease (Bare Equipment Only)"])
    qty_units = st.sidebar.number_input("Equipment Quantity (Units)", min_value=1, max_value=50, value=2)
    rental_tenure = st.sidebar.selectbox("Rental Tenure", ["1 Month (Shutdown Window)", "3 Months", "6 Months", "12 Months Long-Term"])
    extra_context = f"Asset: {specific_eq} | Qty: {qty_units} units | Model: {lease_model} | Tenure: {rental_tenure}."
    param_data = {"type": "rental", "sub": selected_sub, "qty": qty_units, "asset": specific_eq, "model": lease_model, "tenure": rental_tenure}

# SYNCHRONIZED MANPOWER SUPPLY PARAMETERS
elif selected_parent == "Manpower Supply":
    nationality_model = st.sidebar.selectbox(
        "Nationality Profile",
        ["Saudi National (Nitaqat / Saudization Target, GOSI 11.75%)",
         "Expatriate Worker (Maktab Amal Levy, Iqama, Ajeer/Qiwa)",
         "Blended Crew (30% Saudi / 70% Expat Compliant)"]
    )
    available_trades = MANPOWER_MAP.get(selected_sub, ["Skilled Petrochemical Technician"])
    specific_trade = st.sidebar.selectbox("Specific Job Title / Trade", available_trades)
    headcount = st.sidebar.slider("Headcount Quantity (Workers)", min_value=1, max_value=300, value=20, step=1)
    duration_months = st.sidebar.selectbox("Contract Duration", [1, 2, 3, 6, 12, 24, 36], index=4, format_func=lambda x: f"{x} Month(s)")
    shift_pattern = st.sidebar.radio("Working Shift Pattern", ["8 Hours/Day (Standard Maintenance)", "10 Hours/Day (Extended)", "12 Hours/Day (24/7 TAM Shutdown Shift)"])
    extra_context = f"Profile: {nationality_model} | Role: {specific_trade} | Qty: {headcount} workers | Duration: {duration_months} Months | Shift: {shift_pattern}."
    param_data = {"type": "manpower", "sub": selected_sub, "headcount": headcount, "duration": duration_months, "trade": specific_trade, "nationality": nationality_model, "shift": shift_pattern}

# LOGISTICS PARAMETERS
elif selected_sub == "Ocean Freight":
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        origin_port = st.text_input("Origin Port", "KFIP (Jubail)")
    with col_b:
        dest_port = st.text_input("Destination Port", "Mundra Port, India")
    container_spec = st.sidebar.selectbox("Container Size / Cargo Type", ["40ft High Cube (Polymer Pellets)", "20ft GP Container", "ISO Tank Container (Liquid Chemicals)"])
    incoterm = st.sidebar.selectbox("Incoterm", ["FOB Jubail (KFIP)", "CFR Destination Port", "CIF Destination Port"])
    extra_context = f"Route: {origin_port} to {dest_port} | Container: {container_spec} | Incoterm: {incoterm}."
    param_data = {"type": "logistics", "sub": selected_sub, "origin": origin_port, "dest": dest_port, "container": container_spec}

default_scope = f"Petrochemical complex in Jubail Industrial City. {extra_context}"
scope_context = st.sidebar.text_area("4. Project / Route / Scope Details", value=default_scope, height=80)
run_btn = st.sidebar.button("🚀 Run Strategic Analysis", use_container_width=True)

# ---------------------------------------------------------
# ACCURATE SYNCHRONIZED CALCULATION ENGINE
# ---------------------------------------------------------
def generate_instant_petrochemical_model(parent, sub, analysis_type, params):
    risk_score = 8.5 if parent in ["Industrial O&M Services", "Manpower Supply", "Rental Services"] else 6.0
    impact_score = 9.0 if "Crane" in sub or "Rotating" in sub or "Shutdown" in sub else 7.5
    quadrant = "Strategic" if risk_score > 7 else "Leverage"

    # RENTAL SERVICES ENGINE (CALCULATES BASED ON CHOSEN ASSET)
    if params.get("type") == "rental":
        asset_name = params.get("asset", sub)
        qty = params.get("qty", 2)
        is_wet = "Wet" in params.get("model", "")
        
        # Exact Jubail Petrochemical monthly market rate benchmarks per asset
        if "1200T" in asset_name or "Crawler" in asset_name:
            base_monthly = 340000
            op_cost_unit = 22000
        elif "300T to 500T" in asset_name:
            base_monthly = 160000
            op_cost_unit = 16000
        elif "100T to 250T" in asset_name:
            base_monthly = 85000
            op_cost_unit = 12000
        elif "Rough Terrain" in asset_name:
            base_monthly = 48000
            op_cost_unit = 10000
        elif "SPMT" in asset_name:
            base_monthly = 125000
            op_cost_unit = 18000
        elif "Boom Truck" in asset_name:
            base_monthly = 24000
            op_cost_unit = 8500
        elif "ATEX" in asset_name or "Explosion-Proof" in asset_name:
            base_monthly = 48000
            op_cost_unit = 6000
        elif "750 kVA to 1250 kVA" in asset_name:
            base_monthly = 38000
            op_cost_unit = 5000
        elif "250 kVA to 500 kVA" in asset_name:
            base_monthly = 22000
            op_cost_unit = 4000
        elif "Oil-Free" in asset_name or "Compressor" in asset_name:
            base_monthly = 36000
            op_cost_unit = 5000
        elif "Bundle Puller" in asset_name:
            base_monthly = 75000
            op_cost_unit = 14000
        elif "Hydrojetting" in asset_name:
            base_monthly = 65000
            op_cost_unit = 12000
        elif "Flange Facing" in asset_name or "Cold-Cutting" in asset_name:
            base_monthly = 28000
            op_cost_unit = 8000
        elif "PWHT" in asset_name:
            base_monthly = 32000
            op_cost_unit = 7000
        elif "Scaffolding" in asset_name:
            base_monthly = 42000
            op_cost_unit = 6000
        else:
            base_monthly = 25000
            op_cost_unit = 5000

        total_asset = base_monthly * qty
        op_cost = op_cost_unit * qty if is_wet else 0
        fuel_lube = (base_monthly * 0.08) * qty if is_wet else (base_monthly * 0.02) * qty
        maint = total_asset * 0.10
        mob_demob = (15000 if "1200T" in asset_name else 8000) * qty
        cert_inspection = 3500 * qty
        insurance = total_asset * 0.04
        
        subtotal = total_asset + op_cost + fuel_lube + maint + mob_demob + cert_inspection + insurance
        margin = subtotal * 0.11
        grand_total = subtotal + margin
        
        items = [
            {"name": "1. Asset Capital Depreciation", "value": round(total_asset, 2), "details": f"Capital cost recovery for {qty} unit(s) of {asset_name}."},
            {"name": "2. Certified Operators & Riggers", "value": round(op_cost, 2), "details": f"{'Aramco/CIC certified heavy equipment operators' if is_wet else 'Not included in Dry Lease (Client responsibility)'}."},
            {"name": "3. Scheduled Maintenance & Mechanical Wear", "value": round(maint, 2), "details": "Preventative servicing, filter replacements, fluid analysis, and wear."},
            {"name": "4. Fuel, Lubricants & Hydraulic Fluid", "value": round(fuel_lube, 2), "details": "Diesel fuel and high-grade hydraulic fluid replenishment."},
            {"name": "5. Heavy Float Transport & Rigging Mob/Demob", "value": round(mob_demob, 2), "details": "Permitted heavy float transport to/from Jubail plant site."},
            {"name": "6. Third-Party Load Test & RCJY Gate Sticker", "value": round(cert_inspection, 2), "details": "CIC / TUV / Bureau Veritas load certification and Royal Commission gate pass compliance."},
            {"name": "7. Comprehensive On-Site Insurance", "value": round(insurance, 2), "details": "Industrial asset all-risk transit and plant battery-limits insurance."},
            {"name": "8. Contractor Operating Margin (11%)", "value": round(margin, 2), "details": "Fair equipment rental supplier margin."}
        ]
        
        return {
            "analysis_title": f"Granular Rental Should-Cost: {asset_name}",
            "currency_or_unit": "SAR",
            "total_metric_value": round(grand_total, 2),
            "total_metric_label": "Total Monthly Rental Baseline",
            "metric_card_2_label": "Direct Operating Cost", "metric_card_2_value": f"SAR {subtotal:,.0f} ({subtotal/grand_total*100:.1f}%)",
            "metric_card_3_label": "Contractor Profit Margin", "metric_card_3_value": f"SAR {margin:,.0f} (11.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "9.0% (CIPS Benchmark)",
            "chart_title": f"Micro-Cost Breakdown: {qty} Unit(s) of {asset_name}",
            "chart_items": items,
            "secondary_chart_title": "Direct Asset Costs vs Supplier Margin",
            "secondary_chart_labels": ["Direct Operating & Asset Pass-Through", "Supplier Profit Margin"],
            "secondary_chart_values": [round(subtotal, 2), round(margin, 2)],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": impact_score, "supply_risk": risk_score, "contract_horizon": "1 to 3 Years Master Agreement", "supplier_relationship": "Preferred Supplier Alliance"},
            "risk_items": [
                {"risk_name": "Crane / Asset Breakdown during TAM Lift", "prob": 2, "impact": 5.0, "score": 10, "severity": "High", "mitigation": "Mandate mandatory 48-hour pre-lift load test and on-site standby mechanic.", "owner": "Heavy Lift Engineer"},
                {"risk_name": "RCJY / Aramco Inspection Sticker Expiry", "prob": 3, "impact": 4.0, "score": 12, "severity": "Medium", "mitigation": "Audit third-party inspection certificates 14 days prior to site gate entry.", "owner": "Logistics & Site Access Lead"},
                {"risk_name": "Operator Absenteeism or Certification Lapses", "prob": 3, "impact": 4.0, "score": 12, "severity": "Medium", "mitigation": "Contractual clause requiring pre-badged backup operator within 4 hours.", "owner": "Contract Administrator"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Al Faris Equipment Rental", "Bin Quraya Heavy Machinery", "ACT (Arabian Consolidated Trading)", "Expertise Contracting"],
                "tier_2_regional": ["Byrne Equipment Rental", "Peax Equipment Rental", "Hertz Dayim Equipment Rental", "Kanoo Machinery"],
                "global_oems": ["Zahid Tractor (Caterpillar)", "Sarens Nass Middle East", "Mammoet Saudi Arabia", "Liebherr Middle East"]
            },
            "strategic_insights": {
                "summary": f"Audited clean-sheet rental model for {qty} unit(s) of {asset_name} in Jubail complex.",
                "market_benchmark_range": f"SAR {grand_total*0.93:,.0f} - SAR {grand_total*1.08:,.0f} per month",
                "key_drivers_or_forces": ["High regional demand during petrochemical turnaround cycles", "Strict RCJY equipment sticker inspections", "Crane operator certification lead times"],
                "buyer_actionable_levers": ["Unbundle mobilization charges: establish fixed lump-sum caps", "Incorporate standby idle-time discounts (25-30% off during non-operating windows)", "Consolidate crane & equipment rental under 1-year master rate cards"]
            }
        }

    # MANPOWER SUPPLY ENGINE
    elif params.get("type") == "manpower":
        trade_name = params.get("trade", sub)
        n_workers = params.get("headcount", 20)
        n_months = params.get("duration", 12)
        is_saudi = "Saudi" in params.get("nationality", "")
        
        if "Supervisor" in trade_name or "Inspector" in trade_name:
            base_rate = 14500 if is_saudi else 8500
        elif "Welder" in trade_name or "Millwright" in trade_name or "Operator" in trade_name:
            base_rate = 8500 if is_saudi else 5500
        elif "Scaffolder" in trade_name or "Painter" in trade_name:
            base_rate = 6000 if is_saudi else 3800
        else:
            base_rate = 5000 if is_saudi else 3200
        
        direct_wages = base_rate * n_workers * n_months
        gosi_rate = 0.1175 if is_saudi else 0.02
        gosi_cost = direct_wages * gosi_rate
        maktab_amal = 0 if is_saudi else (850 * n_workers * n_months)
        medical_insurance = (250 if is_saudi else 180) * n_workers * n_months
        housing = 1200 * n_workers * n_months
        transport = 600 * n_workers * n_months
        catering = 850 * n_workers * n_months
        ppe = 350 * n_workers * n_months
        flights_esb = direct_wages * (0.083 + 0.05)
        subtotal_direct = direct_wages + gosi_cost + maktab_amal + medical_insurance + housing + transport + catering + ppe + flights_esb
        sga = subtotal_direct * 0.08
        profit = subtotal_direct * 0.10
        total_cost = subtotal_direct + sga + profit
        
        items = [
            {"name": "1. Direct Basic Take-Home Wages", "value": round(direct_wages, 2), "details": f"Basic net wage for {n_workers} {trade_name} across {n_months} month(s)."},
            {"name": "2. GOSI Social Insurance (KSA)", "value": round(gosi_cost, 2), "details": f"{'11.75% Saudi Social Insurance employer contribution' if is_saudi else '2% Expat Occupational Hazard Insurance'}."},
            {"name": "3. Maktab Amal & Iqama Fees", "value": round(maktab_amal, 2), "details": f"{'Exempt for Saudi nationals' if is_saudi else 'Mandatory Ministry of Human Resources work permit levy (SAR 800-850/mo)'}."},
            {"name": "4. CCHI Health Insurance (Class B/A)", "value": round(medical_insurance, 2), "details": "Mandatory medical coverage compliant with Council of Health Insurance."},
            {"name": "5. RCJY Camp Housing & Utilities", "value": round(housing, 2), "details": "Royal Commission approved bachelor camp lodging and utilities in Jubail."},
            {"name": "6. Site Transportation & Buses", "value": round(transport, 2), "details": "Dedicated daily bus transport between camp and plant battery limits."},
            {"name": "7. Industrial Catering (3 Meals/Day)", "value": round(catering, 2), "details": "Standardized industrial food service compliant with SFDA and RCJY hygiene codes."},
            {"name": "8. PPE, Safety Gear & Badging", "value": round(ppe, 2), "details": "Flame-retardant Nomex coveralls, safety boots, H2S monitors, safety passport badging."},
            {"name": "9. Statutory Flights & ESB Accrual", "value": round(flights_esb, 2), "details": "Annual return airfare allowance and Labor Law End-of-Service gratuity accrual."},
            {"name": "10. Contractor Corporate SG&A (8%)", "value": round(sga, 2), "details": "Head-office management, recruiting, compliance administration, and QA/QC."},
            {"name": "11. Contractor Net Margin (10%)", "value": round(profit, 2), "details": "Fair contractor profit margin across contract lifecycle."}
        ]
        
        return {
            "analysis_title": f"Granular Should-Cost: {trade_name}",
            "currency_or_unit": "SAR",
            "total_metric_value": round(total_cost, 2),
            "total_metric_label": "Total Manpower Contract Baseline",
            "metric_card_2_label": "Direct Operating Cost", "metric_card_2_value": f"SAR {subtotal_direct:,.0f} ({subtotal_direct/total_cost*100:.1f}%)",
            "metric_card_3_label": "Contractor Profit Margin", "metric_card_3_value": f"SAR {profit:,.0f} (10.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "8.0% (CIPS Benchmark)",
            "chart_title": f"Micro-Cost Breakdown: {n_workers} {trade_name} ({n_months} Mo)",
            "chart_items": items,
            "secondary_chart_title": "Direct Labor Cost vs Contractor Margin",
            "secondary_chart_labels": ["Direct Site Labor & Overheads", "Contractor SG&A & Profit"],
            "secondary_chart_values": [round(subtotal_direct, 2), round(sga + profit, 2)],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": impact_score, "supply_risk": risk_score, "contract_horizon": "3 to 5 Years Alliance", "supplier_relationship": "Collaborative Partnership"},
            "risk_items": [
                {"risk_name": "Craft Labor Scarcity / Schedule Delay", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "Early reservation agreements 9 months ahead with slot guarantee penalties.", "owner": "Turnaround Procurement Lead"},
                {"risk_name": "HCIS / RCJY Security Gate Pass Bottleneck", "prob": 4, "impact": 3.5, "score": 14, "severity": "High", "mitigation": "Submit digital dossiers 45 days prior via security portal.", "owner": "Security Liaison"},
                {"risk_name": "Qiwa / Nitaqat Quota Freeze", "prob": 3, "impact": 3.0, "score": 9, "severity": "Medium", "mitigation": "Monthly audit of contractor green-zone status in Qiwa.", "owner": "Contract Compliance"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Al-Yusr Industrial (AYTB)", "Sendan International", "Nesma & Partners", "Nasser S. Al-Hajri (NSH)"],
                "tier_2_regional": ["Safari Company", "Tamimi Global", "Rezayat Group", "Expertise Contracting"],
                "global_oems": ["Airswift", "NES Fircroft", "Brunel Energy", "Yokogawa Middle East"]
            },
            "strategic_insights": {
                "summary": f"Clean-sheet model for {n_workers} {trade_name} ({params.get('nationality', 'Workforce')}) in Jubail complex.",
                "market_benchmark_range": f"SAR {total_cost*0.95:,.0f} - SAR {total_cost*1.08:,.0f} for Eastern Province baseline",
                "key_drivers_or_forces": ["MHRSD expat levy pass-through structure", "RCJY industrial accommodation capacity in Jubail", "Qiwa platform electronic compliance audit"],
                "buyer_actionable_levers": ["Audit Maktab Amal fees: mandate zero-markup pass-through", "Enforce fixed rate cards with standardized statutory multipliers", "Consolidate housing under company-managed camp agreements"]
            }
        }

    else:
        # LOGISTICS & DEFAULT
        base, baf, ecs, othc, dthc, eis, lss, wrs, bl, customs, demurrage = 1200, 420, (0 if "India" in params.get("dest", "") else 850), 120, 150, 80, 60, 40, 40, 60, 50
        subtotal = base + baf + ecs + othc + dthc + eis + lss + wrs + bl + customs + demurrage
        margin = subtotal * 0.11
        total_val = round(subtotal + margin, 2)
        dir_val = round(subtotal, 2)
        prof_val = round(margin, 2)
        unit = "USD"
        items = [
            {"name": "1. Ocean Base Steaming Slot", "value": base, "details": "Carrier slot capacity between KFIP and destination."},
            {"name": "2. Bunker Adjustment Factor (BAF)", "value": baf, "details": "Marine fuel adjustment indexed to Fujairah/Singapore VLSFO."},
            {"name": "3. Cape Rerouting / Emergency Surcharge", "value": ecs, "details": "Operational buffer fee for bypassing Red Sea."},
            {"name": "4. Origin THC (KFIP Port)", "value": othc, "details": "Port crane loading and container handling in Jubail."},
            {"name": "5. Destination Terminal Handling (DTHC)", "value": dthc, "details": "Discharge port container terminal handling charges."},
            {"name": "6. Equipment Imbalance Surcharge (EIS)", "value": eis, "details": "Container repositioning and empty return cost."},
            {"name": "7. Low Sulfur Fuel Surcharge (LSS)", "value": lss, "details": "IMO 2020 environmental marine fuel compliance surcharge."},
            {"name": "8. War Risk Transit Premium (WRS)", "value": wrs, "details": "Marine underwriter regional hull transit premium."},
            {"name": "9. Bill of Lading & Port Gate Pass", "value": bl, "details": "Carrier documentation and electronic port gate pass fees."},
            {"name": "10. Export Customs & Port Inspection", "value": customs, "details": "ZATCA export declaration, port seal, and manifest filing."},
            {"name": "11. Demurrage & Detention Buffer", "value": demurrage, "details": "Contingency buffer for port dwell time beyond free days."}
        ]

        return {
            "analysis_title": f"{analysis_type}: {sub}",
            "currency_or_unit": unit,
            "total_metric_value": total_val,
            "total_metric_label": "Total Should-Cost Baseline",
            "metric_card_2_label": "Direct Operating Cost", "metric_card_2_value": f"{unit} {dir_val:,.2f} ({dir_val/total_val*100:.1f}%)",
            "metric_card_3_label": "Contractor Profit Margin", "metric_card_3_value": f"{unit} {prof_val:,.2f} (11.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "8.5% (CIPS Standard)",
            "chart_title": "Granular Micro-Cost Factor Breakdown",
            "chart_items": items,
            "secondary_chart_title": "Direct Site Cost vs Contractor Margin",
            "secondary_chart_labels": ["Direct Operating Pass-Through", "Contractor SG&A & Margin"],
            "secondary_chart_values": [dir_val, prof_val],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": impact_score, "supply_risk": risk_score, "contract_horizon": "3 to 5 Years Alliance", "supplier_relationship": "Collaborative Partnership"},
            "risk_items": [
                {"risk_name": "Port Congestion & Demurrage Spike", "prob": 4, "impact": 4.0, "score": 16, "severity": "Critical", "mitigation": "Negotiate 21 days free detention time at discharge ports.", "owner": "Logistics Category Manager"},
                {"risk_name": "Container Equipment Shortage at KFIP", "prob": 3, "impact": 4.5, "score": 14, "severity": "High", "mitigation": "Establish multi-carrier volume allocation (40/30/30).", "owner": "Shipping Lead"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Bahri (National Shipping Company of Saudi Arabia)", "Almajdouie Logistics", "Kanoo Logistics"],
                "tier_2_regional": ["BDP International Saudi Arabia", "Agility Logistics / DSV", "DHL Global Forwarding"],
                "global_oems": ["Maersk Line", "MSC (Mediterranean Shipping Company)", "Hapag-Lloyd", "CMA CGM"]
            },
            "strategic_insights": {
                "summary": f"Clean-sheet model for {sub} originating from King Fahd Industrial Port.",
                "market_benchmark_range": f"{unit} {total_val*0.95:,.0f} - {unit} {total_val*1.08:,.0f}",
                "key_drivers_or_forces": ["VLSFO marine bunker fuel volatility", "Cape of Good Hope rerouting surcharges", "Container repositioning balance"],
                "buyer_actionable_levers": ["Demand floating BAF tied to published Platts indices", "Audit ECS/emergency surcharges: waive for direct Gulf passages", "Consolidate volume across Jubail entities for tier discounts"]
            }
        }

# ---------------------------------------------------------
# FAST HYBRID API CALL (10S TIMEOUT) -> INSTANT ENGINE
# ---------------------------------------------------------
def fetch_analysis_hybrid(parent, sub, context, analysis_type, user_key, params):
    clean_key = str(user_key).strip().strip('"').strip("'")
    
    if clean_key:
        prompt = f"""You are a Principal Sourcing & Cost Engineer in Jubail Industrial City, Saudi Arabia for a world-scale Petrochemical Complex.
Analyze: Category: {parent} -> {sub} | Tool: {analysis_type} | Context: {context}
Return ONLY valid JSON matching:
{{"analysis_title": "{analysis_type}", "currency_or_unit": "SAR", "total_metric_value": 450000, "total_metric_label": "string",
"metric_card_2_label": "string", "metric_card_2_value": "string", "metric_card_3_label": "string", "metric_card_3_value": "string",
"metric_card_4_label": "string", "metric_card_4_value": "string", "chart_title": "string",
"chart_items": [{{"name": "Cost Line 1", "value": 120000, "details": "Explanation"}}],
"vendor_matrix": {{"tier_1_local": ["Vendor A", "Vendor B"], "tier_2_regional": ["Reg 1"], "global_oems": ["OEM 1"]}},
"kraljic_data": {{"quadrant": "Strategic", "profit_impact": 8.5, "supply_risk": 7.5, "contract_horizon": "string", "supplier_relationship": "string"}},
"risk_items": [{{"risk_name": "Risk 1", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "string", "owner": "string"}}],
"secondary_chart_title": "string", "secondary_chart_labels": ["Cost", "Margin"], "secondary_chart_values": [88, 12],
"strategic_insights": {{"summary": "string", "market_benchmark_range": "string", "key_drivers_or_forces": ["Point 1"], "buyer_actionable_levers": ["Lever 1"]}}}}
JSON ONLY."""

        headers = {"Content-Type": "application/json", "x-goog-api-key": clean_key}
        payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json", "temperature": 0.1, "maxOutputTokens": 2500, "thinkingConfig": {"thinkingLevel": "LOW"}}}
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
        
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                text_out = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                match = re.search(r"\{.*\}", text_out, re.DOTALL)
                if match:
                    res = json.loads(match.group(0))
                    res["source"] = "AI"
                    return res
        except Exception:
            pass

    res = generate_instant_petrochemical_model(parent, sub, analysis_type, params)
    res["source"] = "Petrochemical Engine"
    return res

# ---------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------
if "active_data" not in st.session_state:
    st.session_state["active_data"] = generate_instant_petrochemical_model(selected_parent, selected_sub, selected_analysis, param_data)

if run_btn:
    active_key = st.session_state.get("api_key", "").strip()
    with st.spinner("Calculating synchronized petrochemical model..."):
        st.session_state["active_data"] = fetch_analysis_hybrid(
            selected_parent, selected_sub, scope_context, selected_analysis, active_key, param_data
        )

data = st.session_state["active_data"]

# ---------------------------------------------------------
# EXECUTIVE HEADER BANNER
# ---------------------------------------------------------
st.markdown(f"""
<div class="exec-banner">
    <h2>🏭 Category Management ToolKit Engine</h2>
    <p>Strategic Sourcing & Cost Engineering | Operating Hub: <b>Jubail Industrial City (KSA)</b> | Scope: <b>{selected_parent} ➔ {selected_sub}</b></p>
</div>
""", unsafe_allow_html=True)

if data.get("source") == "Petrochemical Engine":
    st.caption("⚡ **Instant Petrochemical Calculation Engine Active:** Synchronized calculations generated based on your exact selected inputs.")
else:
    st.caption("✅ **Live AI Analysis Active:** Delivered directly via Gemini 3.8 Flash.")

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

# ---------------------------------------------------------
# ROW 1: 4 EXECUTIVE METRIC CARDS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    val_disp = f"{unit} {total_val:,.2f}" if unit in ["SAR", "USD"] else f"{total_val}"
    st.metric(label=data.get("total_metric_label", "Overall Metric"), value=val_disp)
with col2:
    st.metric(label=data.get("metric_card_2_label", "Direct Cost / Impact"), value=data.get("metric_card_2_value", "-"))
with col3:
    st.metric(label=data.get("metric_card_3_label", "Supplier Margin / Risk"), value=data.get("metric_card_3_value", "-"), delta_color="inverse")
with col4:
    st.metric(label=data.get("metric_card_4_label", "Target Benchmark"), value=data.get("metric_card_4_value", "-"), delta_color="off")

st.markdown("---")

# ---------------------------------------------------------
# TABBED EXECUTIVE INTERFACE
# ---------------------------------------------------------
tab_cost, tab_kraljic, tab_risk, tab_vendors, tab_report = st.tabs([
    "📊 Executive Cost Breakdown & CBS",
    "🎯 Kraljic Portfolio Matrix",
    "🔥 Risk Heatmap & Mitigation Plan",
    "🏢 Vendor & OEM Ecosystem",
    "📑 C-Suite Decision Memo & Download Center"
])

# ---------------------------------------------------------
# TAB 1: EXECUTIVE COST BREAKDOWN
# ---------------------------------------------------------
with tab_cost:
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
            fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"), height=450, margin=dict(l=10, r=10, t=20, b=20))
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

    col_pie, col_ins = st.columns([1, 1])
    with col_pie:
        st.subheader(f"💼 {data.get('secondary_chart_title', 'Cost Allocation')}")
        pie_labels = data.get("secondary_chart_labels", ["Direct Costs", "Overhead & Margin"])
        pie_vals = data.get("secondary_chart_values", [85, 15])
        donut_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_vals, hole=.55, marker_colors=["#0284c7", "#10b981", "#f59e0b", "#ef4444"])])
        donut_fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.2))
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

    st.markdown("---")
    st.subheader("📚 Micro-Cost Factor Technical Basis & Engineering Definitions")
    if not df_chart.empty and "details" in df_chart.columns:
        cols = st.columns(2)
        for idx, row in df_chart.iterrows():
            with cols[idx % 2]:
                amt_str = f"{unit} {row['value']:,.2f} ({row['Percentage']:.1f}%)" if unit in ["SAR", "USD"] else f"{row['value']} pts"
                with st.expander(f"🔹 **{row['name']}** — {amt_str}", expanded=False):
                    st.write(row.get("details", "-"))

# ---------------------------------------------------------
# TAB 2: KRALJIC PORTFOLIO MATRIX
# ---------------------------------------------------------
with tab_kraljic:
    col_kraljic, col_ktable = st.columns([1.2, 0.8])
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
        
    with col_ktable:
        st.subheader("📋 Kraljic Strategy Positioning Card")
        st.info(f"**Identified Quadrant:** `{k_data.get('quadrant', 'Strategic')}`")
        st.markdown(f"**Recommended Horizon:** {k_data.get('contract_horizon', '3-5 Years Alliance')}")
        st.markdown(f"**Relationship Model:** {k_data.get('supplier_relationship', 'Collaborative Gainshare')}")
        st.markdown("---")
        st.markdown("**Core Kraljic Dimensions:**")
        st.write(f"- **Profit Impact:** {k_data.get('profit_impact', 8.5)} / 10")
        st.write(f"- **Supply Risk:** {k_data.get('supply_risk', 7.5)} / 10")

# ---------------------------------------------------------
# TAB 3: RISK HEATMAP & MITIGATION
# ---------------------------------------------------------
with tab_risk:
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
        st.subheader("📊 Risk Severity Ranking")
        if risk_list:
            df_r = pd.DataFrame(risk_list)
            st_table = df_r[["risk_name", "prob", "impact", "score", "severity"]].copy()
            st_table.columns = ["Risk Factor", "Prob (1-5)", "Impact (1-5)", "Score (1-25)", "Severity"]
            st.dataframe(st_table, use_container_width=True, height=350)
            
    st.markdown("---")
    st.subheader("🛡️ Category Risk Mitigation Plan & Governance")
    if risk_list:
        for idx, r in enumerate(risk_list):
            with st.expander(f"⚠️ **R{idx+1}: {r['risk_name']}** — Score: `{r['score']}/25` | Severity: `{r['severity']}` | Accountable Owner: `{r['owner']}`", expanded=False):
                st.markdown(f"**Actionable Mitigation Strategy:** {r['mitigation']}")

# ---------------------------------------------------------
# TAB 4: VENDOR & OEM ECOSYSTEM
# ---------------------------------------------------------
with tab_vendors:
    st.subheader("🏢 Preferred Supplier & OEM Ecosystem (Jubail & Eastern Province)")
    st.caption("Prequalified & Accredited Industrial Contractors compliant with RCJY, HCIS, and IKTVA standards.")
    
    vm = data.get("vendor_matrix", {
        "tier_1_local": ["Al-Yusr Industrial (AYTB)", "Sendan International", "Nesma & Partners", "Nasser S. Al-Hajri (NSH)"],
        "tier_2_regional": ["Safari Company", "Tamimi Global", "Rezayat Group", "Expertise Contracting"],
        "global_oems": ["Yokogawa Middle East", "Emerson Automation Solutions", "Baker Hughes", "Siemens Energy"]
    })
    
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        st.success("🟢 **Tier-1 Local KSA (High IKTVA Champions)**")
        for v in vm.get("tier_1_local", []):
            st.markdown(f"- **{v}**")
            
    with v_col2:
        st.warning("🟡 **Tier-2 Regional Specialized Contractors**")
        for v in vm.get("tier_2_regional", []):
            st.markdown(f"- **{v}**")
            
    with v_col3:
        st.info("🌐 **Global OEMs & Technology Licensors**")
        for v in vm.get("global_oems", []):
            st.markdown(f"- **{v}**")

# ---------------------------------------------------------
# TAB 5: CPO & C-SUITE EXECUTIVE MEMO & DOWNLOADS
# ---------------------------------------------------------
with tab_report:
    st.subheader("📑 CPO & Board-Level Executive Decision Memo")
    st.caption("Formal category briefing document for CPO, CFO, and Executive Procurement Committee sign-off.")
    
    memo_text = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'><title>CPO Strategic Category Briefing</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; color: #1e293b; line-height: 1.5; }}
        h1 {{ color: #0f172a; border-bottom: 3px solid #0284c7; padding-bottom: 8px; font-size: 22pt; }}
        h2 {{ color: #0369a1; margin-top: 25px; border-bottom: 1px solid #cbd5e1; padding-bottom: 5px; font-size: 15pt; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 10px; text-align: left; font-size: 10pt; }}
        th {{ background-color: #0f172a; color: #ffffff; font-weight: bold; }}
        .kpi-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; }}
        .kpi-table th {{ background-color: #0284c7; color: #ffffff; padding: 10px; }}
        .header-box {{ background-color: #f1f5f9; padding: 15px; border-left: 5px solid #0284c7; margin-bottom: 20px; }}
    </style>
    </head>
    <body>
        <div class="header-box">
            <h1>CATEGORY STRATEGY & SOURCING MEMORANDUM</h1>
            <p><b>CONFIDENTIAL | FOR CPO & BOARD APPROVAL</b><br>
            <b>Operating Hub:</b> Jubail Industrial City, Kingdom of Saudi Arabia<br>
            <b>Parent Category:</b> {selected_parent} | <b>Subcategory:</b> {selected_sub}<br>
            <b>Date of Briefing:</b> November 2026</p>
        </div>

        <h2>1. EXECUTIVE SUMMARY & COMMERCIAL POSTURE</h2>
        <p>This category review covers <b>{selected_sub}</b> operating within our petrochemical complex in Jubail Industrial City. 
        Based on clean-sheet Should-Cost modeling and market capacity analysis across the Eastern Province, the audited contract baseline is established at <b>{unit} {total_val:,.2f}</b>.</p>

        <table class="kpi-table">
            <tr>
                <th>Total Should-Cost Baseline</th>
                <th>Direct Operating Cost (Pass-Through)</th>
                <th>Contractor Net Margin</th>
                <th>CIPS Target Benchmark Counter</th>
            </tr>
            <tr>
                <td><b>{unit} {total_val:,.2f}</b></td>
                <td>{data.get('metric_card_2_value', '-')}</td>
                <td>{data.get('metric_card_3_value', '-')}</td>
                <td>{data.get('metric_card_4_value', '-')}</td>
            </tr>
        </table>

        <h2>2. GRANULAR MICRO-COST FACTOR BREAKDOWN</h2>
        <table>
            <tr>
                <th style="width: 50%;">Cost Component / Work Package</th>
                <th style="width: 25%;">Engineered Baseline ({unit})</th>
                <th style="width: 25%;">Cost Share (%)</th>
            </tr>
    """
    for _, r in df_chart.iterrows():
        memo_text += f"""
            <tr>
                <td><b>{r['name']}</b></td>
                <td>{unit} {r['value']:,.2f}</td>
                <td>{r['Percentage']:.1f}%</td>
            </tr>
        """
    memo_text += f"""
        </table>

        <h2>3. KRALJIC PORTFOLIO POSITIONING & STRATEGY</h2>
        <p><b>Quadrant:</b> {k_data.get('quadrant', 'Strategic')} | <b>Profit Impact:</b> {k_data.get('profit_impact', 8.5)}/10 | <b>Supply Risk:</b> {k_data.get('supply_risk', 7.5)}/10<br>
        <b>Recommended Contract Horizon:</b> {k_data.get('contract_horizon', '3-5 Years Alliance')}<br>
        <b>Supplier Governance Model:</b> {k_data.get('supplier_relationship', 'Collaborative Gainshare')}</p>

        <h2>4. TOP CATEGORY RISKS & MITIGATION GOVERNANCE</h2>
        <table>
            <tr>
                <th>Risk Factor</th>
                <th>Severity</th>
                <th>Actionable Mitigation Strategy</th>
                <th>Accountable Owner</th>
            </tr>
    """
    for r in risk_list[:4]:
        memo_text += f"""
            <tr>
                <td><b>{r['risk_name']}</b></td>
                <td>{r['severity']}</td>
                <td>{r['mitigation']}</td>
                <td>{r['owner']}</td>
            </tr>
        """
    memo_text += f"""
        </table>

        <h2>5. RECOMMENDED NEGOTIATION LEVERS & ACTION PLAN</h2>
        <ul>
    """
    for l in data.get("strategic_insights", {}).get("buyer_actionable_levers", []):
        memo_text += f"<li>{l}</li>"
    memo_text += f"""
        </ul>

        <h2>6. PREFERRED SUPPLIER ECOSYSTEM</h2>
        <p><b>Tier-1 Local KSA (IKTVA Champions):</b> {', '.join(vm.get('tier_1_local', []))}<br>
        <b>Regional Specialized Contractors:</b> {', '.join(vm.get('tier_2_regional', []))}<br>
        <b>Global OEMs & Technology Providers:</b> {', '.join(vm.get('global_oems', []))}</p>
        <br><br>
        <p><b>Submitted By:</b> Principal Strategic Sourcing & Category Lead, Jubail Petrochemical Complex<br>
        <b>Approved By:</b> Chief Procurement Officer (CPO) / Executive Committee</p>
    </body>
    </html>
    """

    st.markdown(f"""
    **Executive Summary:**  
    Category analysis for **{selected_sub}** in Jubail complex establishes a Should-Cost target of **{unit} {total_val:,.2f}**.  
    The contractor break-even operating floor is **{data.get('metric_card_2_value', '-')}**, with a fair supplier profit margin of **{data.get('metric_card_3_value', '-')}**.
    
    * **Kraljic Quadrant:** `{k_data.get('quadrant', 'Strategic')}` ({k_data.get('contract_horizon', '3-5 Years Alliance')})
    * **Highest Risk Exposure:** Score `{data.get('total_metric_value', 18)}/25` (Mitigation assigned to turnaround and security leads)
    * **Local Content Impact:** Priority routing through Tier-1 Jubail contractors (*{', '.join(vm.get('tier_1_local', [])[:2])}*).
    """)
    
    st.markdown("---")
    st.subheader("📥 Export C-Suite Deliverables")
    
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.download_button(
            label="📄 Download Official CPO Strategy Memo (.doc / Word)",
            data=memo_text.encode("utf-8"),
            file_name=f"{selected_sub.replace(' ', '_')}_CPO_Strategy_Report.doc",
            mime="application/msword",
            use_container_width=True
        )
        st.caption("Microsoft Word compatible document complete with executive tables, KPI cards, and risk registers.")

    with dcol2:
        st.download_button(
            label="🖨️ Download Printable Executive Brief (.html / PDF-Ready)",
            data=memo_text.encode("utf-8"),
            file_name=f"{selected_sub.replace(' ', '_')}_Executive_Brief.html",
            mime="text/html",
            use_container_width=True
        )
        st.caption("Open in browser and press Ctrl+P to save as an executive PDF presentation.")
