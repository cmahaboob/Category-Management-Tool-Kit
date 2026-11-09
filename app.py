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
    /* Metric Cards Styling */
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
    /* Tab Styling */
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
    /* Executive Banner */
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
# PETROCHEMICAL CATALOGS
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
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🏭 Category Management ToolKit")
st.sidebar.caption("Jubail Industrial City | Services & Projects")

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
    extra_context = f"Profile: {nationality_model} | Role: {specific_trade} | Qty: {headcount} workers | Duration: {duration_months} Months | Shift: {shift_pattern}."
    param_data = {"type": "manpower", "headcount": headcount, "duration": duration_months, "trade": specific_trade, "nationality": nationality_model, "shift": shift_pattern}

# DYNAMIC PARAMETERS: RENTAL SERVICES
elif selected_parent == "Rental Services":
    eq_category = st.sidebar.selectbox("Equipment Family", list(RENTAL_CATALOG.keys()))
    specific_eq = st.sidebar.selectbox("Specific Asset / Rig Specification", RENTAL_CATALOG[eq_category])
    lease_model = st.sidebar.radio("Commercial Lease Model", ["Wet Lease (Equipment + Certified Operator + Fuel/Maint + RCJY Inspection)", "Dry Lease (Bare Equipment Only)"])
    qty_units = st.sidebar.number_input("Equipment Quantity (Units)", min_value=1, max_value=50, value=2)
    rental_tenure = st.sidebar.selectbox("Rental Tenure", ["1 Month (Shutdown Window)", "3 Months", "6 Months", "12 Months Long-Term"])
    extra_context = f"Asset: {specific_eq} | Qty: {qty_units} units | Model: {lease_model} | Tenure: {rental_tenure}."
    param_data = {"type": "rental", "qty": qty_units, "asset": specific_eq, "model": lease_model, "tenure": rental_tenure}

# DYNAMIC PARAMETERS: LOGISTICS (OCEAN FREIGHT)
elif selected_sub == "Ocean Freight":
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        origin_port = st.text_input("Origin Port", "KFIP (Jubail)")
    with col_b:
        dest_port = st.text_input("Destination Port", "Mundra Port, India")
    container_spec = st.sidebar.selectbox("Container Size / Cargo Type", ["40ft High Cube (Polymer Pellets)", "20ft GP Container", "ISO Tank Container (Liquid Chemicals)"])
    incoterm = st.sidebar.selectbox("Incoterm", ["FOB Jubail (KFIP)", "CFR Destination Port", "CIF Destination Port"])
    extra_context = f"Route: {origin_port} to {dest_port} | Container: {container_spec} | Incoterm: {incoterm}."
    param_data = {"type": "logistics", "origin": origin_port, "dest": dest_port, "container": container_spec}

default_scope = f"Petrochemical complex in Jubail Industrial City. {extra_context}"
scope_context = st.sidebar.text_area("4. Project / Route / Scope Details", value=default_scope, height=80)
run_btn = st.sidebar.button("🚀 Run Strategic Analysis", use_container_width=True)

# ---------------------------------------------------------
# INSTANT CALCULATION ENGINE
# ---------------------------------------------------------
def generate_instant_petrochemical_model(parent, sub, analysis_type, params):
    risk_score = 8.5 if parent in ["Industrial O&M Services", "Manpower Supply"] else 6.0
    impact_score = 9.0 if "Turnaround" in sub or "Rotating" in sub or "Cracker" in sub else 7.5
    quadrant = "Strategic" if risk_score > 7 else "Leverage"

    if params.get("type") == "manpower":
        n_workers = params.get("headcount", 20)
        n_months = params.get("duration", 12)
        is_saudi = "Saudi" in params.get("nationality", "")
        base_rate = 8500 if "Supervisor" in params.get("trade", "") else (5500 if "Welder" in params.get("trade", "") or "Millwright" in params.get("trade", "") else 3800)
        
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
            {"name": "1. Direct Basic Take-Home Wages", "value": round(direct_wages, 2), "details": f"Basic net wages for {n_workers} {params.get('trade', 'technicians')} across {n_months} month(s)."},
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
        total_val = round(total_cost, 2)
        dir_val = round(subtotal_direct, 2)
        prof_val = round(profit, 2)
        unit = "SAR"
        
    elif params.get("type") == "rental":
        qty = params.get("qty", 2)
        base_asset = 85000 if "Crane" in params.get("asset", "") else (25000 if "Generator" in params.get("asset", "") else 18000)
        total_asset = base_asset * qty
        is_wet = "Wet" in params.get("model", "")
        op_cost = 12000 * qty if is_wet else 0
        fuel_lube = 6500 * qty if is_wet else 1500 * qty
        maint = total_asset * 0.12
        mob_demob = 8000 * qty
        cert_inspection = 2500 * qty
        insurance = total_asset * 0.05
        subtotal = total_asset + op_cost + fuel_lube + maint + mob_demob + cert_inspection + insurance
        margin = subtotal * 0.12
        total_val = round(subtotal + margin, 2)
        dir_val = round(subtotal, 2)
        prof_val = round(margin, 2)
        unit = "SAR"
        
        items = [
            {"name": "1. Asset Depreciation & Amortization", "value": round(total_asset, 2), "details": f"Capital cost recovery for {qty} unit(s) of {params.get('asset', 'equipment')}."},
            {"name": "2. Certified Operators / Riggers", "value": round(op_cost, 2), "details": f"{'Aramco/CIC certified heavy equipment operators' if is_wet else 'Not included (Dry Lease)'}."},
            {"name": "3. Scheduled Maintenance & Wear", "value": round(maint, 2), "details": "Routine servicing, filters, fluid changes, and mechanical wear."},
            {"name": "4. Fuel, Oil & Lubricants", "value": round(fuel_lube, 2), "details": "Industrial diesel and hydraulic oil replenishment."},
            {"name": "5. Heavy Mobilization & Demob", "value": round(mob_demob, 2), "details": "Lowbed float transport to and from Jubail site."},
            {"name": "6. Third-Party Load Test & RCJY Inspection", "value": round(cert_inspection, 2), "details": "CIC / Bureau Veritas load test certification & Royal Commission gate pass sticker."},
            {"name": "7. Asset Comprehensive Insurance", "value": round(insurance, 2), "details": "All-risk industrial equipment transit and on-site insurance coverage."},
            {"name": "8. Contractor Net Margin (12%)", "value": round(margin, 2), "details": "Equipment rental supplier operating profit margin."}
        ]
    else:
        # Logistics / General Should-Cost
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
            {"name": "11. Demurrage & Detention Buffer", "valu
