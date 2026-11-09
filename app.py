import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import re
import requests
import time

# ---------------------------------------------------------
# PAGE CONFIGURATION & CONSULTING-TIER THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Category Management ToolKit Engine | Petrochemical",
    page_icon="🏭",
    layout="wide"
)

# McKinsey / Kearney Style Custom CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #F8FAFC;
    }

    .consulting-banner {
        background: linear-gradient(135deg, #0A192F 0%, #0F2A4A 55%, #1E3A8A 100%);
        color: #FFFFFF;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 22px;
        border-left: 6px solid #D97706;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.12), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
    }
    .consulting-banner h1 {
        color: #F8FAFC;
        margin: 0;
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .consulting-banner p {
        color: #94A3B8;
        margin: 6px 0 0 0;
        font-size: 0.95rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 8px;
    }
    .badge-amber { background-color: rgba(217, 119, 6, 0.25); color: #FBBF24; border: 1px solid rgba(217, 119, 6, 0.5); }
    .badge-blue { background-color: rgba(37, 99, 235, 0.25); color: #93C5FD; border: 1px solid rgba(37, 99, 235, 0.5); }
    .badge-red { background-color: rgba(220, 38, 38, 0.25); color: #FCA5A5; border: 1px solid rgba(220, 38, 38, 0.5); }

    div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.08);
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
        border: 1px solid #CBD5E1;
        border-left: 5px solid #475569;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(71, 85, 105, 0.08);
    }
    div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 1px solid #FDE68A;
        border-left: 5px solid #D97706;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.08);
    }
    div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #A7F3D0;
        border-left: 5px solid #059669;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.08);
    }
    div[data-testid="stMetric"] label {
        font-weight: 700;
        color: #334155;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0F172A;
        font-weight: 800;
        font-size: 1.65rem;
        letter-spacing: -0.02em;
    }

    .card-insight {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 1px solid #BAE6FD;
        border-left: 6px solid #0284C7;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(2, 132, 199, 0.08);
    }
    .card-kraljic-info {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 1px solid #FDE68A;
        border-left: 6px solid #D97706;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.08);
    }
    .card-geopolitics {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 1px solid #FECACA;
        border-left: 6px solid #DC2626;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.08);
        margin-bottom: 18px;
    }
    .vendor-card-tier1 {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #BBF7D0;
        border-top: 5px solid #16A34A;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(22, 163, 74, 0.08);
    }
    .vendor-card-tier2 {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border: 1px solid #FDE68A;
        border-top: 5px solid #D97706;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(217, 119, 6, 0.08);
    }
    .vendor-card-oem {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-top: 5px solid #2563EB;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.08);
    }
    .card-memo-preview {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-top: 6px solid #0F172A;
        border-radius: 10px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.06);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.92rem;
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        color: #475569;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border-color: #0F172A !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.25);
    }

    .consulting-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        overflow: hidden;
        background: #FFFFFF;
        margin-top: 8px;
    }
    .consulting-table th {
        background-color: #0F172A;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 12px 14px;
        text-align: left;
    }
    .consulting-table td {
        padding: 12px 14px;
        font-size: 0.88rem;
        border-bottom: 1px solid #E2E8F0;
        color: #334155;
    }
    .consulting-table tr:hover {
        background-color: #F8FAFC;
    }
    .sev-badge {
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
    }
    .sev-critical { background-color: #FEE2E2; color: #DC2626; border: 1px solid #FCA5A5; }
    .sev-high { background-color: #FFEDD5; color: #EA580C; border: 1px solid #FDBA74; }
    .sev-medium { background-color: #FEF9C3; color: #CA8A04; border: 1px solid #FDE047; }
    .sev-low { background-color: #DCFCE7; color: #16A34A; border: 1px solid #86EFAC; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPREHENSIVE LOGISTICS PORTS & HUBS REPOSITORY
# ---------------------------------------------------------
KSA_LOADING_PORTS = [
    "King Fahd Industrial Port, Jubail (KFIP) [Petrochemical Core]",
    "Jubail Commercial Port (JCP)",
    "King Abdulaziz Port, Dammam (KAPD)",
    "Jeddah Islamic Port (JIP)",
    "King Abdullah Port, Rabigh (KAP)",
    "Yanbu Industrial & Commercial Port",
    "Ras Al-Khair Port"
]

GLOBAL_DESTINATION_PORTS = [
    "Mundra Port, India (West Coast Gateway)",
    "Nhava Sheva / JNPT (Mumbai, India)",
    "Karachi Port, Pakistan",
    "Port Muhammad Bin Qasim, Pakistan",
    "Singapore Port (Southeast Asia Hub)",
    "Shanghai Port, China",
    "Ningbo-Zhoushan Port, China",
    "Port Klang, Malaysia",
    "Chittagong Port, Bangladesh",
    "Mersin Port, Turkey (East Med Hub)",
    "Ambarli / Istanbul Port, Turkey",
    "Aliaga / Izmir Port, Turkey",
    "Antwerp Port, Belgium (ARA Petrochem Hub)",
    "Rotterdam Port, Netherlands",
    "Genoa Port, Italy",
    "Jebel Ali Port, UAE",
    "Sohar Port, Oman",
    "Houston Port, USA (Gulf of Mexico)",
    "Santos Port, Brazil"
]

KSA_INLAND_ORIGINS = [
    "Jubail 1 Industrial City (Complex Plant Gate)",
    "Jubail 2 Industrial Area (Plastics Park)",
    "Ras Al-Khair Industrial City",
    "Dammam 2nd Industrial City",
    "Yanbu Industrial City"
]

KSA_INLAND_DESTINATIONS = [
    "KFIP Container Terminal (Jubail)",
    "King Abdulaziz Port, Dammam (KAPD)",
    "Riyadh Dry Port & Logistics Hub",
    "King Fahd Causeway (Bahrain Export Border)",
    "Al Batha Border (UAE Land Freight)",
    "Salwa Border (Qatar Land Freight)",
    "Al Nuwaiseeb Border (Kuwait Land Freight)",
    "Jeddah Islamic Port (Cross-Kingdom Shuttling)"
]

INLAND_TRUCK_FLEET = [
    "40ft Flatbed Semi-Trailer (Resin Pallets / 26 MT Max)",
    "Curtain-Sider Box Trailer (Weather Protected Polymers)",
    "Bulk Polymer Silo Bulker Truck (Pneumatic Discharge)",
    "Heavy ISO Tank Container Chassis (Liquid Chemicals)",
    "Multi-Axle Heavy Lowbed Trailer (Over-Dimensional Cargo)"
]

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
    "Logistics Services": [
        "Ocean Freight",
        "KSA Inland Transportation",
        "Product Shuttling (Plant to Port)",
        "Cross-Border Inland (GCC)",
        "Export Freight Forwarding",
        "Import Freight Forwarding",
        "Customs Clearance",
        "Terminal, Port & Hub (KFIP/Dammam)",
        "Warehousing & Open Yard",
        "Container / ISO Tank",
        "Bagging & Packing"
    ],
    "Rental Services": list(RENTAL_MAP.keys()),
    "Manpower Supply": list(MANPOWER_MAP.keys()),
    "Industrial O&M Services": [
        "Mechanical Maintenance (Piping, Static, Valves)",
        "Rotating Equipment Overhaul (Turbines/Compressors)",
        "Electrical Maintenance (Motors, VFDs, Switchgear)",
        "Instrumentation & Control (Analyzers, DCS)",
        "Inspection & Testing (NDT, RBI, Lifting)",
        "Industrial Cleaning (Hydrojetting 10k-40k PSI)",
        "Catalyst Handling under Inert Atmosphere",
        "Building & Civil Maintenance",
        "Material Handling Equipment Maintenance",
        "Safety & Fire Protection Systems Maintenance"
    ],
    "Soft / Facility Management": [
        "Workplace Operations (Cleaning & Janitorial)",
        "Industrial & Camp Catering Services",
        "Property & Worker Accommodations Lease (RCJY)",
        "Pest Control & Vector Management",
        "Potable Water & Bulk Fluid Supply",
        "Corporate Security & Guard Force",
        "Office Renovation & Workplace Support",
        "Waste Management & Hazardous Fluid Handling"
    ],
    "IT & Digital Services": [
        "Enterprise Subscription & Renewal (ERP/Core)",
        "Strategic Platform Partnership (Cloud/Hyperscalers)",
        "Managed Services Framework (AMS/Infra)",
        "Network & Telecom Framework (Plant Connectivity)",
        "Cybersecurity & OT Risk Model (HCIS/NCA CSCC)",
        "End-User Computing & Hardware Catalog"
    ],
    "Project & Construction": [
        "Brownfield EPC / EPCM Plant Debottlenecking",
        "Civil Works & Deep Foundations",
        "Mechanical Piping Tie-ins & Structural Revamp",
        "Electrical & Instrumentation Installation",
        "Scaffolding & Insulation (SIP Packages)",
        "Plant Modification Management of Change (MOC)"
    ],
    "Professional & Consultancy": [
        "Engineering Design & Licensor TSA (GES/GES+)",
        "Process Safety & HAZOP / SIL Studies",
        "Legal & Regulatory Advisory (Trade, REACH/KKDIK)",
        "Financial Audit & Tax Advisory (ZATCA)",
        "Corporate Strategy & Operating Model Optimization",
        "Petrochemical Feasibility & Market Forecasting"
    ],
    "HSE and Compliance": [
        "HCIS Physical Security Compliance Infrastructure",
        "Environmental Emissions Testing (RCER 2020)",
        "Hazardous Petrochemical Waste Incineration",
        "Fixed Fire Suppression & Deluge Maintenance",
        "Personal Protective Equipment (PPE) Contracts"
    ]
}

ANALYSIS_TYPES = [
    "Should-Cost & Cost Breakdown Structure (CBS)",
    "Porter's 5 Forces & Market Intelligence",
    "Kraljic Matrix Positioning & Strategic Portfolio",
    "Risk Assessment Scorecard, Heatmap & Mitigation Plan",
    "Kearney Purchasing Chessboard & Sourcing Strategy",
    "Total Cost of Ownership (TCO) Lifecycle Model"
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

# 1. OCEAN FREIGHT
if selected_sub == "Ocean Freight":
    st.sidebar.markdown("🚢 **Maritime Route & Volumes**")
    pol = st.sidebar.selectbox("Port of Loading (POL - Saudi Arabia)", KSA_LOADING_PORTS)
    pod = st.sidebar.selectbox("Port of Destination (POD - Global)", GLOBAL_DESTINATION_PORTS)
    container_vol = st.sidebar.number_input("Annual Container Volume (FEU / 40ft HC)", min_value=1, max_value=25000, value=1200, step=50)
    cargo_type = st.sidebar.selectbox("Cargo Specification", ["Polymer Resin Pellets (High Cube 40ft)", "Liquid Bulk Petrochemical (ISO Tank)", "General Chemical Cargo (20ft GP)"])
    incoterm = st.sidebar.selectbox("Commercial Incoterm", ["FOB Loading Port (Saudi Arabia)", "CFR Discharge Port", "CIF Discharge Port"])
    
    st.sidebar.markdown("🌍 **Geopolitical Maritime Chokepoints**")
    chokepoint_hormuz = st.sidebar.checkbox("Strait of Hormuz Active Risk (WRS Hull Surcharge)", value=True)
    chokepoint_bab = st.sidebar.checkbox("Bab al-Mandab / Red Sea Disruption (Cape Rerouting Buffer)", value=False if ("India" in pod or "Pakistan" in pod) else True)
    
    extra_context = f"POL: {pol} | POD: {pod} | Volume: {container_vol} FEU | Cargo: {cargo_type} | Incoterm: {incoterm} | Hormuz Risk: {chokepoint_hormuz} | Bab al-Mandab Disruption: {chokepoint_bab}."
    param_data = {
        "type": "ocean_freight", "sub": selected_sub, "pol": pol, "pod": pod,
        "volume": container_vol, "cargo": cargo_type, "incoterm": incoterm,
        "hormuz": chokepoint_hormuz, "bab_mandab": chokepoint_bab
    }

# 2. INLAND FREIGHT
elif selected_sub in ["KSA Inland Transportation", "Product Shuttling (Plant to Port)", "Cross-Border Inland (GCC)"]:
    st.sidebar.markdown("🚛 **Inland Freight Route & Fleet**")
    inland_orig = st.sidebar.selectbox("Origin Location (KSA Industrial Hub)", KSA_INLAND_ORIGINS)
    inland_dest = st.sidebar.selectbox("Destination Hub / Port", KSA_INLAND_DESTINATIONS)
    fleet_type = st.sidebar.selectbox("Trailer / Fleet Configuration", INLAND_TRUCK_FLEET)
    trip_count = st.sidebar.number_input("Annual Trip Count (Truckloads)", min_value=10, max_value=15000, value=650, step=25)
    diesel_index = st.sidebar.checkbox("Index to Aramco Diesel Price (SAR 1.15/L)", value=True)
    
    extra_context = f"Inland Route: {inland_orig} to {inland_dest} | Fleet: {fleet_type} | Trips: {trip_count} | Diesel Indexed: {diesel_index}."
    param_data = {
        "type": "inland_freight", "sub": selected_sub, "orig": inland_orig, "dest": inland_dest,
        "fleet": fleet_type, "trips": trip_count, "diesel_index": diesel_index
    }

# 3. RENTAL SERVICES
elif selected_parent == "Rental Services":
    available_assets = RENTAL_MAP.get(selected_sub, ["Heavy Equipment Asset"])
    specific_eq = st.sidebar.selectbox("Specific Asset Specification", available_assets)
    lease_model = st.sidebar.radio("Commercial Lease Model", ["Wet Lease (Equipment + Certified Operator + Fuel/Maint + RCJY Inspection)", "Dry Lease (Bare Equipment Only)"])
    qty_units = st.sidebar.number_input("Equipment Quantity (Units)", min_value=1, max_value=50, value=2)
    rental_tenure = st.sidebar.selectbox("Rental Tenure", ["1 Month (Shutdown Window)", "3 Months", "6 Months", "12 Months Long-Term"])
    extra_context = f"Asset: {specific_eq} | Qty: {qty_units} units | Model: {lease_model} | Tenure: {rental_tenure}."
    param_data = {"type": "rental", "sub": selected_sub, "qty": qty_units, "asset": specific_eq, "model": lease_model, "tenure": rental_tenure}

# 4. MANPOWER SUPPLY
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

default_scope = f"Petrochemical facility in Jubail Industrial City. {extra_context}"
scope_context = st.sidebar.text_area("4. Project / Route / Scope Details", value=default_scope, height=80)
run_btn = st.sidebar.button("🚀 Run Strategic Analysis", use_container_width=True)

# ---------------------------------------------------------
# ACCURATE SYNCHRONIZED CALCULATION ENGINE
# ---------------------------------------------------------
def generate_instant_petrochemical_model(parent, sub, analysis_type, params):
    risk_score = 8.5 if (parent in ["Industrial O&M Services", "Manpower Supply", "Rental Services"] or params.get("bab_mandab", False)) else 6.5
    impact_score = 9.0 if ("Crane" in sub or "Rotating" in sub or "Ocean Freight" in sub or "Shutdown" in sub) else 7.5
    quadrant = "Strategic" if (risk_score > 7 and impact_score > 7.5) else "Leverage"

    if params.get("type") == "ocean_freight":
        pod = params.get("pod", "Mundra Port, India")
        vol = params.get("volume", 1200)
        has_hormuz = params.get("hormuz", True)
        has_bab = params.get("bab_mandab", False)
        
        if "India" in pod or "Pakistan" in pod:
            base_slot = 480
            baf = 280
            is_red_sea_route = False
        elif "Turkey" in pod or "Mediterranean" in pod:
            base_slot = 1150
            baf = 420
            is_red_sea_route = True
        elif "Rotterdam" in pod or "Antwerp" in pod or "Europe" in pod:
            base_slot = 1350
            baf = 480
            is_red_sea_route = True
        elif "Houston" in pod or "USA" in pod or "Santos" in pod:
            base_slot = 1850
            baf = 560
            is_red_sea_route = True
        else:
            base_slot = 550
            baf = 310
            is_red_sea_route = False

        ecs = (950 if (has_bab and is_red_sea_route) else 0)
        wrs = 65 if has_hormuz else 20
        othc = 115
        dthc = 145
        eis = 75
        lss = 55
        bl = 40
        customs = 45
        demurrage = 40
        
        subtotal_box = base_slot + baf + ecs + wrs + othc + dthc + eis + lss + bl + customs + demurrage
        margin_box = subtotal_box * 0.10
        total_box = subtotal_box + margin_box
        total_annual = total_box * vol
        
        items = [
            {"name": "1. Ocean Base Steaming Slot", "value": round(base_slot * vol, 2), "details": f"Core carrier slot capacity from {params.get('pol', 'KFIP')} to {pod} (${base_slot}/box)."},
            {"name": "2. Bunker Adjustment Factor (BAF)", "value": round(baf * vol, 2), "details": f"Marine bunker fuel adjustment indexed to Fujairah/Singapore VLSFO (${baf}/box)."},
            {"name": "3. Bab al-Mandab Rerouting / ECS Surcharge", "value": round(ecs * vol, 2), "details": f"{'Active: Cape of Good Hope rerouting buffer (+$950/box)' if ecs > 0 else 'Zero: Route does not cross Southern Red Sea'}"},
            {"name": "4. Strait of Hormuz War Risk Premium (WRS)", "value": round(wrs * vol, 2), "details": f"Hull & transit regional underwriter premium for Arabian Gulf exit (${wrs}/box)."},
            {"name": "5. Origin THC (King Fahd Industrial Port)", "value": round(othc * vol, 2), "details": f"Jubail port container crane loading & terminal operations (${othc}/box)."},
            {"name": "6. Destination Terminal Handling (DTHC)", "value": round(dthc * vol, 2), "details": f"Discharge port container handling charges at {pod} (${dthc}/box)."},
            {"name": "7. Equipment Imbalance Surcharge (EIS)", "value": round(eis * vol, 2), "details": f"Container empty repositioning back to Arabian Gulf hubs (${eis}/box)."},
            {"name": "8. Low Sulfur Fuel Surcharge (LSS / IMO 2020)", "value": round(lss * vol, 2), "details": f"Environmental marine fuel compliance surcharge (${lss}/box)."},
            {"name": "9. Bill of Lading & Port Gate Pass", "value": round(bl * vol, 2), "details": f"Carrier electronic documentation and port security gate fees (${bl}/box)."},
            {"name": "10. Export Customs Clearance (ZATCA / Fasah)", "value": round(customs * vol, 2), "details": f"Electronic manifest filing, customs inspection, and port seal (${customs}/box)."},
            {"name": "11. Demurrage & Detention Buffer", "value": round(demurrage * vol, 2), "details": f"Contingency buffer for discharge port dwell time beyond free days (${demurrage}/box)."}
        ]
        
        return {
            "analysis_title": f"Ocean Freight Should-Cost: {params.get('pol', 'KFIP')} to {pod}",
            "currency_or_unit": "USD",
            "total_metric_value": round(total_annual, 2),
            "total_metric_label": f"Total Annual Freight Spend ({vol} FEU)",
            "metric_card_2_label": "Rate per Container (FEU)", "metric_card_2_value": f"USD {total_box:,.2f} / box",
            "metric_card_3_label": "Chokepoint Surcharges (ECS+WRS)", "metric_card_3_value": f"USD {(ecs+wrs):,.2f} ({(ecs+wrs)/total_box*100:.1f}%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "8.0% Margin Cap",
            "chart_title": f"Annual Cost Distribution: {vol} Containers to {pod}",
            "chart_items": items,
            "secondary_chart_title": "Base Steaming Slot vs Geopolitical Surcharges & Fees",
            "secondary_chart_labels": ["Base Steaming & Fuel", "Geopolitical Surcharges (Hormuz/ECS)", "Port Charges & Admin"],
            "secondary_chart_values": [round((base_slot + baf) * vol, 2), round((ecs + wrs) * vol, 2), round((othc + dthc + eis + lss + bl + customs + demurrage) * vol, 2)],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": 8.8, "supply_risk": risk_score, "contract_horizon": "1 to 2 Years Volume Framework", "supplier_relationship": "Core Carrier Strategic Program"},
            "risk_items": [
                {"risk_name": "Bab al-Mandab Missile/Drone Interdiction", "prob": 5 if is_red_sea_route else 1, "impact": 4.8, "score": 24 if is_red_sea_route else 5, "severity": "Critical" if is_red_sea_route else "Low", "mitigation": "Contractual clause waiving ECS if carriers operate direct convoy escort windows.", "owner": "Global Logistics Director"},
                {"risk_name": "Strait of Hormuz Escalation & GPS Spoofing", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "Establish multi-port contingency routing via KAPD Dammam and Yanbu land-bridge.", "owner": "Petrochemical Supply Chain VP"},
                {"risk_name": "Container Equipment Imbalance at Jubail KFIP", "prob": 4, "impact": 4.0, "score": 16, "severity": "High", "mitigation": "Allocate export volume 40/30/30 across top 3 container alliances (2M, Ocean, THE).", "owner": "Shipping Operations Manager"},
                {"risk_name": "Bunker Fuel (VLSFO) Price Shock in Fujairah", "prob": 3, "impact": 3.8, "score": 11, "severity": "Medium", "mitigation": "Demand transparent quarterly floating BAF indexed to Platts Fujairah.", "owner": "Category Lead Freight"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Bahri (National Shipping Company of Saudi Arabia)", "Almajdouie Logistics", "Kanoo Logistics"],
                "tier_2_regional": ["BDP International Saudi Arabia", "Agility Logistics / DSV", "DHL Global Forwarding"],
                "global_oems": ["Maersk Line (2M Alliance)", "MSC (Mediterranean Shipping Co)", "CMA CGM (Ocean Alliance)", "Hapag-Lloyd"]
            },
            "strategic_insights": {
                "summary": f"Audited freight model for {vol} containers from {params.get('pol', 'KFIP')} to {pod}. {'Route exposed to Southern Red Sea Cape rerouting' if is_red_sea_route else 'Route remains within direct Arabian Sea lanes.'}",
                "market_benchmark_range": f"USD {total_box*0.93:,.0f} - USD {total_box*1.08:,.0f} per container",
                "key_drivers_or_forces": ["Strait of Hormuz war risk insurance surcharges", "Suez Canal bypass lead-time extensions (+12-14 days)", "Platts Fujairah VLSFO marine bunker indices"],
                "buyer_actionable_levers": ["Demand floating index-linked BAF mechanism", "Unbundle and audit Cape rerouting ECS surcharges", "Commit baseline quarterly allocations in exchange for free-time detention (21 days)"]
            }
        }

    elif params.get("type") == "inland_freight":
        trips = params.get("trips", 650)
        fleet = params.get("fleet", "40ft Flatbed")
        is_indexed = params.get("diesel_index", True)
        
        base_trip = 1850 if "Riyadh" in params.get("dest", "") else (850 if "KFIP" in params.get("dest", "") or "Dammam" in params.get("dest", "") else 2400)
        fuel_cost = base_trip * 0.32
        driver_wage = base_trip * 0.22
        maint_tires = base_trip * 0.14
        truck_amortization = base_trip * 0.16
        gate_fees = 120
        subtotal_trip = fuel_cost + driver_wage + maint_tires + truck_amortization + gate_fees
        margin_trip = subtotal_trip * 0.11
        total_trip = subtotal_trip + margin_trip
        total_annual = total_trip * trips
        
        items = [
            {"name": "1. Diesel Fuel (Aramco SAR 1.15/L)", "value": round(fuel_cost * trips, 2), "details": f"Fuel consumption over route ({'Indexed to Aramco baseline' if is_indexed else 'Fixed quote'})."},
            {"name": "2. Certified Heavy Driver Wage & GOSI", "value": round(driver_wage * trips, 2), "details": "TGA certified commercial heavy vehicle driver wage, per-diem, and social insurance."},
            {"name": "3. Truck Capital Depreciation / Lease", "value": round(truck_amortization * trips, 2), "details": f"Asset amortization for {fleet}."},
            {"name": "4. Preventative Maintenance, Tires & Fluids", "value": round(maint_tires * trips, 2), "details": "Scheduled mechanical servicing and tire wear allocation per kilometer."},
            {"name": "5. Port / Industrial Gate Access & Tolls", "value": round(gate_fees * trips, 2), "details": "ZATCA electronic gate pass, port entry fees, and weighbridge charges."},
            {"name": "6. Transporter SG&A & Operating Margin", "value": round(margin_trip * trips, 2), "details": "Contractor dispatch overhead and net profit margin (11%)."}
        ]
        
        return {
            "analysis_title": f"Inland Transport Should-Cost: {params.get('orig', 'Jubail')} to {params.get('dest', 'Port')}",
            "currency_or_unit": "SAR",
            "total_metric_value": round(total_annual, 2),
            "total_metric_label": f"Annual Transport Spend ({trips} Trips)",
            "metric_card_2_label": "Rate per Trip", "metric_card_2_value": f"SAR {total_trip:,.2f} / trip",
            "metric_card_3_label": "Fuel Share (Aramco Diesel)", "metric_card_3_value": f"SAR {fuel_cost:,.2f} (32.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "8.5% Margin Cap",
            "chart_title": f"Annual Cost Distribution: {trips} Trips of {fleet}",
            "chart_items": items,
            "secondary_chart_title": "Fuel & Operating Costs vs Transporter Margin",
            "secondary_chart_labels": ["Fuel & Driver Pass-Through", "Asset Wear & Contractor Margin"],
            "secondary_chart_values": [round((fuel_cost + driver_wage) * trips, 2), round((maint_tires + truck_amortization + margin_trip) * trips, 2)],
            "kraljic_data": {"quadrant": "Leverage", "profit_impact": 7.0, "supply_risk": 5.5, "contract_horizon": "2 Years Master Rate Card", "supplier_relationship": "Competitive Sourcing"},
            "risk_items": [
                {"risk_name": "Aramco Domestic Diesel Price Adjustment", "prob": 4, "impact": 3.5, "score": 14, "severity": "High", "mitigation": "Establish mathematical fuel indexation formula tied directly to Ministry of Energy announcements.", "owner": "Logistics Sourcing Lead"},
                {"risk_name": "Port Gate Dwell & Demurrage Congestion", "prob": 3, "impact": 4.0, "score": 12, "severity": "Medium", "mitigation": "Implement pre-booked truck appointment system (Fasah) 24 hours prior.", "owner": "Dispatch Supervisor"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Almajdouie Logistics", "Bahri Logistics", "Bin Quraya Transport", "Hala Supply Chain"],
                "tier_2_regional": ["Mubarrad Transport", "Kanoo Logistics", "Al-Falak Transport"],
                "global_oems": ["Mercedes-Benz Actros (Juffali)", "Volvo Trucks (Zahid Tractor)", "MAN Truck & Bus"]
            },
            "strategic_insights": {
                "summary": f"Inland freight clean-sheet model for {trips} trips using {fleet}.",
                "market_benchmark_range": f"SAR {total_trip*0.94:,.0f} - SAR {total_trip*1.08:,.0f} per trip",
                "key_drivers_or_forces": ["Aramco domestic diesel price stability", "TGA driver work hour compliance regulations", "Port terminal turn-times"],
                "buyer_actionable_levers": ["Incorporate mathematical fuel adjustment formula", "Consolidate backhaul routes from Riyadh/Dammam to eliminate empty running", "Benchmark against TGA standard tariff schedules"]
            }
        }

    elif params.get("type") == "rental":
        asset_name = params.get("asset", sub)
        qty = params.get("qty", 2)
        is_wet = "Wet" in params.get("model", "")
        
        if "1200T" in asset_name or "Crawler" in asset_name:
            base_monthly = 340000; op_cost_unit = 22000
        elif "300T to 500T" in asset_name:
            base_monthly = 160000; op_cost_unit = 16000
        elif "100T to 250T" in asset_name:
            base_monthly = 85000; op_cost_unit = 12000
        elif "SPMT" in asset_name:
            base_monthly = 125000; op_cost_unit = 18000
        elif "750 kVA to 1250 kVA" in asset_name:
            base_monthly = 38000; op_cost_unit = 5000
        elif "250 kVA to 500 kVA" in asset_name:
            base_monthly = 22000; op_cost_unit = 4000
        elif "Oil-Free" in asset_name:
            base_monthly = 36000; op_cost_unit = 5000
        else:
            base_monthly = 28000; op_cost_unit = 6000

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
            {"name": "2. Certified Operators & Riggers", "value": round(op_cost, 2), "details": f"{'Aramco/CIC certified heavy equipment operators' if is_wet else 'Not included in Dry Lease'}."},
            {"name": "3. Scheduled Maintenance & Mechanical Wear", "value": round(maint, 2), "details": "Preventative servicing, filter replacements, fluid analysis, and wear."},
            {"name": "4. Fuel, Lubricants & Hydraulic Fluid", "value": round(fuel_lube, 2), "details": "Diesel fuel and high-grade hydraulic fluid replenishment."},
            {"name": "5. Heavy Float Transport & Rigging Mob/Demob", "value": round(mob_demob, 2), "details": "Permitted heavy float transport to/from Jubail plant site."},
            {"name": "6. Third-Party Load Test & RCJY Gate Sticker", "value": round(cert_inspection, 2), "details": "CIC / TUV load test certification and Royal Commission gate pass compliance."},
            {"name": "7. Comprehensive On-Site Insurance", "value": round(insurance, 2), "details": "Industrial asset all-risk transit and plant battery-limits insurance."},
            {"name": "8. Contractor Operating Margin (11%)", "value": round(margin, 2), "details": "Fair equipment rental supplier margin."}
        ]
        
        return {
            "analysis_title": f"Rental Should-Cost: {asset_name}",
            "currency_or_unit": "SAR",
            "total_metric_value": round(grand_total, 2),
            "total_metric_label": "Total Monthly Rental Baseline",
            "metric_card_2_label": "Direct Operating Cost", "metric_card_2_value": f"SAR {subtotal:,.0f} ({subtotal/grand_total*100:.1f}%)",
            "metric_card_3_label": "Contractor Profit Margin", "metric_card_3_value": f"SAR {margin:,.0f} (11.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "9.0% (CIPS Benchmark)",
            "chart_title": f"Micro-Cost Breakdown: {qty} Unit(s) of {asset_name}",
            "chart_items": items,
            "secondary_chart_title": "Direct Asset Costs vs Supplier Margin",
            "secondary_chart_labels": ["Direct Operating Pass-Through", "Supplier Profit Margin"],
            "secondary_chart_values": [round(subtotal, 2), round(margin, 2)],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": impact_score, "supply_risk": risk_score, "contract_horizon": "1 to 3 Years Master Agreement", "supplier_relationship": "Preferred Supplier Alliance"},
            "risk_items": [
                {"risk_name": "Asset Breakdown during Critical TAM Lift", "prob": 2, "impact": 5.0, "score": 10, "severity": "High", "mitigation": "Mandate mandatory 48-hour pre-lift load test and dedicated standby mechanic.", "owner": "Heavy Lift Engineer"},
                {"risk_name": "RCJY / Aramco Gate Inspection Sticker Expiry", "prob": 3, "impact": 4.0, "score": 12, "severity": "Medium", "mitigation": "Audit third-party certificates 14 days prior to site mobilization.", "owner": "Site Access Lead"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["Al Faris Equipment Rental", "Bin Quraya Heavy Machinery", "ACT (Arabian Consolidated Trading)", "Expertise Contracting"],
                "tier_2_regional": ["Byrne Equipment Rental", "Peax Equipment Rental", "Hertz Dayim Equipment Rental", "Kanoo Machinery"],
                "global_oems": ["Zahid Tractor (Caterpillar)", "Sarens Nass Middle East", "Mammoet Saudi Arabia", "Liebherr Middle East"]
            },
            "strategic_insights": {
                "summary": f"Audited clean-sheet rental model for {qty} unit(s) of {asset_name} in Jubail complex.",
                "market_benchmark_range": f"SAR {grand_total*0.93:,.0f} - SAR {grand_total*1.08:,.0f} per month",
                "key_drivers_or_forces": ["Turnaround season demand spikes in Eastern Province", "RCJY third-party safety compliance", "Certified operator availability"],
                "buyer_actionable_levers": ["Unbundle mobilization charges: establish fixed lump-sum caps", "Incorporate standby idle-time discounts (25-30% off)", "Consolidate fleet rental under master rate cards"]
            }
        }

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
            {"name": "2. GOSI Social Insurance (KSA)", "value": round(gosi_cost, 2), "details": f"{'11.75% Saudi Social Insurance' if is_saudi else '2% Expat Hazard Insurance'}."},
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
            "analysis_title": f"Manpower Should-Cost: {trade_name}",
            "currency_or_unit": "SAR",
            "total_metric_value": round(total_cost, 2),
            "total_metric_label": "Total Contract Baseline",
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
                {"risk_name": "HCIS / RCJY Security Gate Pass Bottleneck", "prob": 4, "impact": 3.5, "score": 14, "severity": "High", "mitigation": "Submit digital dossiers 45 days prior via security portal.", "owner": "Security Liaison"}
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
        return {
            "analysis_title": f"{analysis_type}: {sub}",
            "currency_or_unit": "SAR",
            "total_metric_value": 450000,
            "total_metric_label": "Total Should-Cost Baseline",
            "metric_card_2_label": "Direct Operating Cost", "metric_card_2_value": "SAR 396,000 (88.0%)",
            "metric_card_3_label": "Contractor Profit Margin", "metric_card_3_value": "SAR 54,000 (12.0%)",
            "metric_card_4_label": "Target Benchmark Counter", "metric_card_4_value": "8.5% (CIPS Standard)",
            "chart_title": "Granular Micro-Cost Factor Breakdown",
            "chart_items": [
                {"name": "1. Direct Skilled Labor", "value": 180000, "details": "Core technicians and certified specialists."},
                {"name": "2. Statutory KSA Fringe & GOSI", "value": 75000, "details": "Social insurance, visas, health coverage."},
                {"name": "3. Field Accommodation & Badging", "value": 55000, "details": "RCJY camp housing, transport, safety passports."},
                {"name": "4. Consumables & Tooling", "value": 45000, "details": "Industrial tooling wear and consumables."},
                {"name": "5. Corporate SG&A Overhead (8%)", "value": 41000, "details": "Head-office management and HSE compliance."},
                {"name": "6. Contractor Profit Margin (12%)", "value": 54000, "details": "Fair contractor profit margin."}
            ],
            "secondary_chart_title": "Direct Site Cost vs Contractor Margin",
            "secondary_chart_labels": ["Direct Operating Pass-Through", "Contractor SG&A & Margin"],
            "secondary_chart_values": [355000, 95000],
            "kraljic_data": {"quadrant": quadrant, "profit_impact": impact_score, "supply_risk": risk_score, "contract_horizon": "3 to 5 Years Alliance", "supplier_relationship": "Collaborative Partnership"},
            "risk_items": [
                {"risk_name": "Turnaround Schedule Delay", "prob": 4, "impact": 4.5, "score": 18, "severity": "Critical", "mitigation": "Early reservation 9 months ahead.", "owner": "Turnaround Procurement Lead"},
                {"risk_name": "RCJY Security Gate Pass Delays", "prob": 4, "impact": 3.5, "score": 14, "severity": "High", "mitigation": "Submit digital dossiers 45 days prior.", "owner": "Security Liaison"}
            ],
            "vendor_matrix": {
                "tier_1_local": ["AYTB", "Sendan", "Nesma & Partners"],
                "tier_2_regional": ["Safari Company", "Tamimi Global"],
                "global_oems": ["Yokogawa", "Baker Hughes", "Siemens Energy"]
            },
            "strategic_insights": {
                "summary": f"Clean-sheet model for {sub} in Jubail Industrial City.",
                "market_benchmark_range": "SAR 430,000 - SAR 490,000",
                "key_drivers_or_forces": ["Turnaround capacity bottlenecks in Eastern Province", "Strict RCJY environmental codes", "Qiwa compliance validation"],
                "buyer_actionable_levers": ["Unbundle statutory pass-throughs", "Enforce fixed rate cards with volume discounts", "Establish core partner alliances"]
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
{{"analysis_title": "{analysis_type}", "currency_or_unit": "USD" or "SAR", "total_metric_value": 450000, "total_metric_label": "string",
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
    with st.spinner(f"Executing consulting-grade {selected_analysis}..."):
        st.session_state["active_data"] = fetch_analysis_hybrid(
            selected_parent, selected_sub, scope_context, selected_analysis, active_key, param_data
        )

data = st.session_state["active_data"]

# ---------------------------------------------------------
# CONSULTING-GRADE EXECUTIVE HEADER BANNER (NO INDENTATION BUG)
# ---------------------------------------------------------
pol_pod_display = ""
if param_data.get("type") == "ocean_freight":
    pol_pod_display = f" | Route: <b>{param_data.get('pol', 'KFIP')} ➔ {param_data.get('pod', 'Global Port')}</b> ({param_data.get('volume', 1200)} FEU)"
elif param_data.get("type") == "inland_freight":
    pol_pod_display = f" | Inland Route: <b>{param_data.get('orig', 'Jubail')} ➔ {param_data.get('dest', 'Port')}</b> ({param_data.get('trips', 650)} Trips)"

badges_html = '<span class="badge-pill badge-amber">Jubail Industrial Complex</span><span class="badge-pill badge-blue">CIPS & Kearney Methodology</span>'
if param_data.get('hormuz'):
    badges_html += '<span class="badge-pill badge-red">⚠️ Strait of Hormuz Risk Active</span>'
if param_data.get('bab_mandab'):
    badges_html += '<span class="badge-pill badge-red">⚠️ Cape of Good Hope Reroute Active</span>'

status_label = "Live AI Model" if data.get('source') == 'AI' else "Instant Petrochemical Engine"

# Assembled with zero indentation to guarantee proper HTML rendering
banner_html = f"""<div class="consulting-banner"><div style="display: flex; justify-content: space-between; align-items: flex-start;"><div>{badges_html}<h1 style="margin-top: 8px;">🏭 Category Management ToolKit Engine</h1><p>Petrochemical Strategic Sourcing & Cost Engineering | Active Scope: <b>{selected_parent} ➔ {selected_sub}</b>{pol_pod_display}</p></div><div style="text-align: right;"><span style="font-size: 0.85rem; color: #94A3B8;">Primary Tool:</span><br><span style="font-weight: 800; color: #FBBF24; font-size: 1.05rem;">{selected_analysis}</span><br><span style="font-weight: 700; color: #10B981; font-size: 0.85rem;">● {status_label}</span></div></div></div>"""
st.markdown(banner_html, unsafe_allow_html=True)

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
# ROW 1: 4 DISTINCT COLORED METRIC CARDS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    val_disp = f"{unit} {total_val:,.2f}" if unit in ["SAR", "USD"] else f"{total_val}"
    st.metric(label=data.get("total_metric_label", "Overall Baseline"), value=val_disp)
with col2:
    st.metric(label=data.get("metric_card_2_label", "Direct Cost"), value=data.get("metric_card_2_value", "-"))
with col3:
    st.metric(label=data.get("metric_card_3_label", "Supplier Margin / Chokepoint"), value=data.get("metric_card_3_value", "-"), delta_color="inverse")
with col4:
    st.metric(label=data.get("metric_card_4_label", "Target Benchmark"), value=data.get("metric_card_4_value", "-"), delta_color="off")

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TABBED EXECUTIVE INTERFACE (ALL 7 TOOLS FULLY POPULATED)
# ---------------------------------------------------------
tab_cost, tab_5forces, tab_kraljic, tab_risk, tab_kearney, tab_vendors, tab_report = st.tabs([
    "📊 Should-Cost & Granular CBS",
    "🌐 Porter's 5 Forces & Market Intel",
    "🎯 Kraljic Portfolio Matrix",
    "🔥 Geopolitical Risk & Heatmap",
    "♟️ Kearney Chessboard & Levers",
    "🏢 Vendor Ecosystem (Local/OEMs)",
    "📑 C-Suite Decision Memo & Exports"
])

# ---------------------------------------------------------
# TAB 1: EXECUTIVE COST BREAKDOWN & CBS
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
                color="value",
                color_continuous_scale=[[0.0, "#0284C7"], [0.5, "#0EA5E9"], [1.0, "#0369A1"]],
                template="plotly_white"
            )
            fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"), height=460, margin=dict(l=10, r=10, t=20, b=20))
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
            st.dataframe(tbl, use_container_width=True, height=430)

    col_pie, col_ins = st.columns([1, 1])
    with col_pie:
        st.subheader(f"💼 {data.get('secondary_chart_title', 'Cost Allocation')}")
        pie_labels = data.get("secondary_chart_labels", ["Direct Costs", "Overhead & Margin"])
        pie_vals = data.get("secondary_chart_values", [85, 15])
        donut_fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_vals, hole=.60, marker_colors=["#0284C7", "#DC2626", "#F59E0B", "#10B981"])])
        donut_fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=-0.2), template="plotly_white")
        st.plotly_chart(donut_fig, use_container_width=True)

    with col_ins:
        st.subheader("💡 Strategic Insights & Buyer Action Plan")
        insights = data.get("strategic_insights", {})
        
        insight_html = '<div class="card-insight">'
        if "market_benchmark_range" in insights:
            insight_html += f"<p style='color:#0369A1; font-weight:800; margin-bottom:8px;'><b>📌 Market Benchmark:</b> {insights['market_benchmark_range']}</p>"
        insight_html += "<p style='color:#0F172A; font-weight:700; margin:10px 0 4px 0;'>🔍 Primary Cost Drivers & Surcharges:</p><ul style='margin-top:4px; padding-left:20px; color:#334155;'>"
        for d in insights.get("key_drivers_or_forces", []):
            insight_html += f"<li>{d}</li>"
        insight_html += "</ul>"
        insight_html += "<p style='color:#0F172A; font-weight:700; margin:10px 0 4px 0;'>🎯 Recommended Negotiation Levers:</p><ul style='margin-top:4px; padding-left:20px; color:#334155;'>"
        for l in insights.get("buyer_actionable_levers", []):
            insight_html += f"<li><b>{l}</b></li>"
        insight_html += "</ul></div>"
        st.markdown(insight_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: PORTER'S 5 FORCES & INDUSTRY INTEL
# ---------------------------------------------------------
with tab_5forces:
    st.subheader(f"🌐 Porter's 5 Forces Competitive Intensity Scorecard: {selected_sub}")
    st.caption("Quantitative Market Power Evaluation for Petrochemical Sourcing in Eastern Province / GCC")
    
    col_pchart, col_ptext = st.columns([1.1, 0.9])
    is_logistics = selected_parent == "Logistics Services"
    p_forces = [
        {"force": "1. Supplier Bargaining Power", "score": 82 if is_logistics else 75, "rating": "HIGH", "desc": "Global shipping alliances (2M, Ocean Alliance) control vessel capacity; strict equipment allocation at KFIP."},
        {"force": "2. Buyer Bargaining Power", "score": 68 if is_logistics else 72, "rating": "MODERATE-HIGH", "desc": "High annual export volume from Jubail petrochemical complex provides anchor customer leverage."},
        {"force": "3. Threat of New Entrants", "score": 28, "rating": "LOW", "desc": "Massive capital expenditure required for mega-containerships, heavy crawler cranes, and port terminal concessions."},
        {"force": "4. Threat of Substitutes", "score": 35, "rating": "LOW-MODERATE", "desc": "Limited substitution; ocean freight is irreplaceable for high-tonnage polymer exports to Asia/Europe."},
        {"force": "5. Competitive Rivalry", "score": 74, "rating": "HIGH", "desc": "Fierce competition on non-chokepoint trade lanes; carriers compete aggressively on long-term annual contracts."}
    ]
    df_pf = pd.DataFrame(p_forces)
    
    with col_pchart:
        fig_pf = px.bar(
            df_pf, x="score", y="force", orientation="h",
            text=df_pf.apply(lambda r: f"{r['score']} / 100 ({r['rating']})", axis=1),
            color="score",
            color_continuous_scale=[[0.0, "#10B981"], [0.5, "#F59E0B"], [1.0, "#DC2626"]],
            template="plotly_white"
        )
        fig_pf.update_layout(showlegend=False, yaxis=dict(autorange="reversed"), height=360, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_pf, use_container_width=True)
        
    with col_ptext:
        forces_summary_html = f"""<div class="card-insight"><h4 style="color:#0369A1; margin-top:0;">📊 Strategic Market Power Balance</h4><p style="color:#334155; font-size:0.9rem;"><b>Overall Market Regime:</b> <span class="badge-pill badge-amber">Carrier / Supplier Dominated</span><br>Due to maritime chokepoints and carrier consolidation, supplier power remains elevated. However, <b>Jubail's aggregate export volume</b> enables Procurement to break standard rate cards by structuring multi-year commitments.</p><hr style="border:0; border-top:1px solid #BAE6FD; margin:10px 0;"><p style="color:#0F172A; font-weight:700; margin-bottom:4px;">Recommended Procurement Counter-Strategy:</p><ul style="padding-left:18px; color:#334155; font-size:0.88rem; margin:0;"><li>Tender across alliances (2M, Ocean, THE Alliance) to stimulate rivalry.</li><li>Carve out local terminal handling from ocean base to eliminate hidden margin stacking.</li><li>Demand index-linked BAF to prevent paying fuel risk premiums during market downturns.</li></ul></div>"""
        st.markdown(forces_summary_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: KRALJIC PORTFOLIO MATRIX
# ---------------------------------------------------------
with tab_kraljic:
    col_kraljic, col_ktable = st.columns([1.2, 0.8])
    k_data = data.get("kraljic_data", {"quadrant": "Strategic", "profit_impact": 8.5, "supply_risk": 7.5})
    
    with col_kraljic:
        st.subheader("🎯 Kraljic Portfolio Matrix (2x2)")
        fig_k = go.Figure()
        
        fig_k.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5, fillcolor="#F1F5F9", opacity=0.7, line_width=1, line_color="#CBD5E1")
        fig_k.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5, fillcolor="#FEF3C7", opacity=0.7, line_width=1, line_color="#FDE68A")
        fig_k.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10, fillcolor="#E0F2FE", opacity=0.7, line_width=1, line_color="#BAE6FD")
        fig_k.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10, fillcolor="#FEE2E2", opacity=0.7, line_width=1, line_color="#FECACA")
        
        fig_k.add_shape(type="line", x0=5, y0=0, x1=5, y1=10, line=dict(color="#64748B", width=2, dash="dash"))
        fig_k.add_shape(type="line", x0=0, y0=5, x1=10, y1=5, line=dict(color="#64748B", width=2, dash="dash"))
        
        fig_k.add_annotation(x=2.5, y=2.5, text="<b>ROUTINE / NON-CRITICAL</b><br><span style='font-size:10px;color:#64748B'>Simplify & Digitalize</span>", showarrow=False, font=dict(color="#475569", size=12))
        fig_k.add_annotation(x=7.5, y=2.5, text="<b>BOTTLENECK</b><br><span style='font-size:10px;color:#D97706'>Secure Volume & Buffer</span>", showarrow=False, font=dict(color="#B45309", size=12))
        fig_k.add_annotation(x=2.5, y=7.5, text="<b>LEVERAGE</b><br><span style='font-size:10px;color:#0284C7'>Competitive Sourcing</span>", showarrow=False, font=dict(color="#0369A1", size=12))
        fig_k.add_annotation(x=7.5, y=7.5, text="<b>STRATEGIC</b><br><span style='font-size:10px;color:#DC2626'>Long-Term Partnership</span>", showarrow=False, font=dict(color="#B91C1C", size=12))
        
        p_x = k_data.get("supply_risk", 7.5)
        p_y = k_data.get("profit_impact", 8.5)
        
        fig_k.add_trace(go.Scatter(
            x=[p_x], y=[p_y],
            mode="markers+text",
            marker=dict(size=32, color="#0A192F", line=dict(width=3, color="#D97706")),
            text=[f"<b>{selected_sub}</b>"],
            textposition="top center",
            textfont=dict(size=12, color="#0F172A", family="Plus Jakarta Sans"),
            name="Category Position"
        ))
        
        fig_k.update_layout(
            xaxis=dict(title="<b>Supply Market Risk (Complexity / Scarcity / Chokepoints) →</b>", range=[0, 10], showgrid=False, zeroline=False),
            yaxis=dict(title="<b>Profit & Business Impact (Downtime / Export Revenue) →</b>", range=[0, 10], showgrid=False, zeroline=False),
            height=430,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            template="plotly_white"
        )
        st.plotly_chart(fig_k, use_container_width=True)
        
    with col_ktable:
        st.subheader("📋 Kraljic Strategy Positioning Card")
        k_card_html = f"""<div class="card-kraljic-info"><h3 style="color:#B45309; margin-top:0; font-size:1.3rem;">🎯 Quadrant: {k_data.get('quadrant', 'Strategic')}</h3><p style="color:#0F172A; font-weight:700; margin:10px 0 4px 0;"><b>Contract Horizon:</b></p><p style="color:#475569; margin-top:2px;">{k_data.get('contract_horizon', '1-2 Years Framework')}</p><p style="color:#0F172A; font-weight:700; margin:10px 0 4px 0;"><b>Supplier Governance Model:</b></p><p style="color:#475569; margin-top:2px;">{k_data.get('supplier_relationship', 'Core Carrier Strategic Alliance')}</p><hr style="border: 0; border-top: 1px solid #FDE68A; margin: 14px 0;"><p style="color:#334155; margin:0;"><b>Profit Impact Score:</b> {k_data.get('profit_impact', 8.5)} / 10<br><b>Supply Risk Score:</b> {k_data.get('supply_risk', 7.5)} / 10</p><p style="color:#92400E; font-size:0.8rem; margin-top:12px;">📌 <i>Buyer Directive: Align contractual volume commitments to secure slot allocation and eliminate spot rate surcharges.</i></p></div>"""
        st.markdown(k_card_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 4: GEOPOLITICAL RISK HEATMAP & MITIGATION
# ---------------------------------------------------------
with tab_risk:
    st.markdown("""<div class="card-geopolitics"><h4 style="color:#B91C1C; margin-top:0; font-weight:800;">🚨 Geopolitical Maritime Vulnerability Notice (Middle East Corridors)</h4><p style="color:#7F1D1D; font-size:0.9rem; margin:0;"><b>1. Strait of Hormuz:</b> Mandatory transit for all petrochemical exports originating from KFIP (Jubail) and Dammam. Subject to regional War Risk Surcharges (WRS) and naval escort contingencies.<br><b>2. Bab al-Mandab & Southern Red Sea:</b> Vessel diversions around the Cape of Good Hope add <b>10–14 days</b> steaming lead-time and <b>+$850 to +$1,100 per container</b> in emergency fuel/operating surcharges.</p></div>""", unsafe_allow_html=True)

    col_map, col_score = st.columns([1.1, 0.9])
    risk_list = data.get("risk_items", [])
    
    with col_map:
        st.subheader("🔥 5x5 Geopolitical & Category Risk Heatmap")
        
        impact_labels = ["1. Negligible", "2. Minor", "3. Moderate", "4. Major", "5. Catastrophic"]
        prob_labels = ["1. Rare", "2. Unlikely", "3. Possible", "4. Likely", "5. Almost Certain"]
        
        z_matrix = [
            [1, 2, 3, 4, 5],
            [2, 4, 6, 8, 10],
            [3, 6, 9, 12, 15],
            [4, 8, 12, 16, 20],
            [5, 10, 15, 20, 25]
        ]
        
        fig_h = go.Figure(data=go.Heatmap(
            z=z_matrix,
            x=impact_labels,
            y=prob_labels,
            colorscale=[
                [0.0, "#A7F3D0"],
                [0.2, "#D1FAE5"],
                [0.4, "#FEF3C7"],
                [0.6, "#FED7AA"],
                [1.0, "#FCA5A5"]
            ],
            showscale=False,
            hoverinfo="none"
        ))
        
        if risk_list:
            def clamp_label(val, label_list):
                idx = max(0, min(4, int(round(val)) - 1))
                return label_list[idx]

            cell_groups = {}
            for i, r in enumerate(risk_list):
                coord = (clamp_label(r.get("impact", 3), impact_labels), clamp_label(r.get("prob", 3), prob_labels))
                if coord not in cell_groups:
                    cell_groups[coord] = []
                cell_groups[coord].append((f"R{i+1}", r))

            scatter_x, scatter_y, scatter_text, scatter_hover = [], [], [], []

            for (x_val, y_val), items in cell_groups.items():
                scatter_x.append(x_val)
                scatter_y.append(y_val)
                badge_label = ", ".join([it[0] for it in items])
                scatter_text.append(f"<b>{badge_label}</b>")
                
                hover_entries = []
                for it in items:
                    hover_entries.append(f"<b>{it[0]}: {it[1]['risk_name']}</b><br>Score: {it[1]['score']}/25 | Severity: {it[1]['severity']}<br>Mitigation: {it[1]['mitigation']}")
                scatter_hover.append("<br><br>".join(hover_entries))

            fig_h.add_trace(go.Scatter(
                x=scatter_x,
                y=scatter_y,
                mode="markers+text",
                marker=dict(
                    size=34 if any("," in t for t in scatter_text) else 28,
                    color="#0A192F",
                    line=dict(width=2.5, color="#FFFFFF")
                ),
                text=scatter_text,
                textposition="middle center",
                textfont=dict(color="#FFFFFF", size=10, family="Plus Jakarta Sans"),
                hovertext=scatter_hover,
                hoverinfo="text",
                name="Category Risks"
            ))
            
        fig_h.update_layout(
            xaxis=dict(title="<b>Impact Severity (Asset / Supply / Cost) →</b>", tickfont=dict(size=10, family="Plus Jakarta Sans"), categoryorder="array", categoryarray=impact_labels),
            yaxis=dict(title="<b>Probability (Likelihood) →</b>", tickfont=dict(size=10, family="Plus Jakarta Sans"), categoryorder="array", categoryarray=prob_labels),
            height=430,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            template="plotly_white"
        )
        st.plotly_chart(fig_h, use_container_width=True)
        
    with col_score:
        st.subheader("📊 Risk Severity Register")
        if risk_list:
            rows_html = "".join([
                f'<tr><td><b>R{i+1}</b></td><td>{r["risk_name"]}</td><td><b>{r["score"]}</b>/25</td><td><span class="sev-badge sev-{r.get("severity", "Medium").lower()}">{r.get("severity", "Medium")}</span></td></tr>'
                for i, r in enumerate(risk_list)
            ])
            table_html = f'<table class="consulting-table"><thead><tr><th style="width: 12%;">ID</th><th style="width: 58%;">Risk Factor</th><th style="width: 15%;">Score</th><th style="width: 15%;">Severity</th></tr></thead><tbody>{rows_html}</tbody></table>'
            st.markdown(table_html, unsafe_allow_html=True)
            
    st.markdown("---")
    st.subheader("🛡️ Category Risk Mitigation Plan & Governance")
    if risk_list:
        for idx, r in enumerate(risk_list):
            sev = r.get("severity", "Medium")
            with st.expander(f"⚠️ **R{idx+1}: {r['risk_name']}** — Severity: `{sev}` | Score: `{r['score']}/25` | Owner: `{r['owner']}`", expanded=False):
                st.markdown(f"**Actionable Mitigation Strategy:** {r['mitigation']}")

# ---------------------------------------------------------
# TAB 5: KEARNEY CHESSBOARD & SOURCING STRATEGY
# ---------------------------------------------------------
with tab_kearney:
    st.subheader(f"♟️ Kearney Purchasing Chessboard Sourcing Levers: {selected_sub}")
    st.caption("Strategic Value Levers based on Buyer vs Supplier Power Balance")
    
    k_col1, k_col2 = st.columns([1, 1])
    with k_col1:
        st.markdown("""<div class="card-kraljic-info"><h4 style="color:#B45309; margin-top:0;">🎯 Core Kearney Strategy: Core Partner Alliance & Target Costing</h4><p style="color:#334155; font-size:0.9rem;">Based on position in the <b>Strategic Quadrant</b> (High Demand, Market Concentration), standard transactional bidding results in margin leakage. Procurement must deploy <b>Value Chain Restructuring</b> and <b>Formula-Based Pricing</b>.</p><hr style="border:0; border-top:1px solid #FDE68A; margin:10px 0;"><p style="color:#0F172A; font-weight:700;">Key Kearney Action Levers:</p><ul style="padding-left:18px; color:#334155; font-size:0.88rem; margin:0;"><li><b>Unbundled Cost Transparency:</b> Separate base operating rates from fuel and pass-throughs.</li><li><b>Demand Pooling:</b> Aggregate volume across all Jubail manufacturing entities.</li><li><b>Indexation:</b> Tie variable surcharges to transparent published indices.</li></ul></div>""", unsafe_allow_html=True)
        
    with k_col2:
        st.markdown("""<div class="card-insight"><h4 style="color:#0284C7; margin-top:0;">💰 Projected 3-Year Value Capture</h4><table style="width:100%; border-collapse:collapse; font-size:0.88rem;"><tr style="border-bottom:1px solid #BAE6FD;"><td style="padding:8px 0; color:#334155;"><b>Type 1 (Hard P&L Savings):</b></td><td style="text-align:right; font-weight:700; color:#0F172A;">6.5% - 8.0%</td></tr><tr style="border-bottom:1px solid #BAE6FD;"><td style="padding:8px 0; color:#334155;"><b>Type 2 (Cost Avoidance / Cap):</b></td><td style="text-align:right; font-weight:700; color:#0F172A;">12.0% - 15.0%</td></tr><tr style="border-bottom:1px solid #BAE6FD;"><td style="padding:8px 0; color:#334155;"><b>Type 3 (Working Capital / Detention Free-Time):</b></td><td style="text-align:right; font-weight:700; color:#0F172A;">21 Days Guaranteed</td></tr></table><p style="color:#0369A1; font-size:0.8rem; margin-top:10px;"><i>Reconciled against CIPS procurement savings standards.</i></p></div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 6: VENDOR & OEM ECOSYSTEM
# ---------------------------------------------------------
with tab_vendors:
    st.subheader("🏢 Preferred Supplier & Carrier Ecosystem (Jubail & Global)")
    st.caption("Prequalified & Accredited Industrial Contractors compliant with RCJY, HCIS, and IKTVA standards.")
    
    vm = data.get("vendor_matrix", {
        "tier_1_local": ["Bahri (National Shipping Company of Saudi Arabia)", "Almajdouie Logistics", "Kanoo Logistics"],
        "tier_2_regional": ["BDP International Saudi Arabia", "Agility Logistics / DSV", "DHL Global Forwarding"],
        "global_oems": ["Maersk Line", "MSC (Mediterranean Shipping Company)", "Hapag-Lloyd", "CMA CGM"]
    })
    
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        v1_html = "<div class='vendor-card-tier1'>"
        v1_html += "<h4 style='color:#15803D; margin-top:0; font-weight:800;'>🟢 Tier-1 Local KSA</h4>"
        v1_html += "<p style='color:#166534; font-size:0.8rem; margin-top:-6px;'>High IKTVA Champions & Prime Fleet</p><hr style='border:0; border-top:1px solid #BBF7D0; margin:10px 0;'><ul style='padding-left:18px; color:#14532D; margin:0;'>"
        for v in vm.get("tier_1_local", []):
            v1_html += f"<li style='margin-bottom:6px;'><b>{v}</b></li>"
        v1_html += "</ul></div>"
        st.markdown(v1_html, unsafe_allow_html=True)
            
    with v_col2:
        v2_html = "<div class='vendor-card-tier2'>"
        v2_html += "<h4 style='color:#B45309; margin-top:0; font-weight:800;'>🟡 Tier-2 Regional</h4>"
        v2_html += "<p style='color:#92400E; font-size:0.8rem; margin-top:-6px;'>Specialized Fleet & Freight Forwarders</p><hr style='border:0; border-top:1px solid #FDE68A; margin:10px 0;'><ul style='padding-left:18px; color:#78350F; margin:0;'>"
        for v in vm.get("tier_2_regional", []):
            v2_html += f"<li style='margin-bottom:6px;'><b>{v}</b></li>"
        v2_html += "</ul></div>"
        st.markdown(v2_html, unsafe_allow_html=True)
            
    with v_col3:
        v3_html = "<div class='vendor-card-oem'>"
        v3_html += "<h4 style='color:#1D4ED8; margin-top:0; font-weight:800;'>🌐 Global Shipping Alliances & OEMs</h4>"
        v3_html += "<p style='color:#1E40AF; font-size:0.8rem; margin-top:-6px;'>Global Container Lines & Asset Licensors</p><hr style='border:0; border-top:1px solid #BFDBFE; margin:10px 0;'><ul style='padding-left:18px; color:#1E3A8A; margin:0;'>"
        for v in vm.get("global_oems", []):
            v3_html += f"<li style='margin-bottom:6px;'><b>{v}</b></li>"
        v3_html += "</ul></div>"
        st.markdown(v3_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 7: CPO & C-SUITE EXECUTIVE MEMO & DOWNLOADS
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
            <b>Selected Scope:</b> {extra_context}<br>
            <b>Date of Briefing:</b> November 2026</p>
        </div>

        <h2>1. EXECUTIVE SUMMARY & COMMERCIAL POSTURE</h2>
        <p>This category review covers <b>{selected_sub}</b>. 
        Based on clean-sheet Should-Cost modeling and market capacity analysis across the Eastern Province, the audited contract baseline is established at <b>{unit} {total_val:,.2f}</b>.</p>

        <table class="kpi-table">
            <tr>
                <th>Total Baseline Commitment</th>
                <th>Direct Operating Cost (Pass-Through)</th>
                <th>Supplier Profit Margin</th>
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
        <b>Recommended Contract Horizon:</b> {k_data.get('contract_horizon', '1-2 Years Framework')}<br>
        <b>Supplier Governance Model:</b> {k_data.get('supplier_relationship', 'Core Carrier Strategic Alliance')}</p>

        <h2>4. TOP GEOPOLITICAL & CATEGORY RISKS</h2>
        <table>
            <tr>
                <th>Risk Factor</th>
                <th>Severity</th>
                <th>Actionable Mitigation Strategy</th>
                <th>Accountable Owner</th>
            </tr>
    """
    for r in risk_list[:5]:
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

        <h2>6. PREFERRED CARRIER & SUPPLIER ECOSYSTEM</h2>
        <p><b>Tier-1 Local KSA (IKTVA Champions):</b> {', '.join(vm.get('tier_1_local', []))}<br>
        <b>Regional Specialized Contractors:</b> {', '.join(vm.get('tier_2_regional', []))}<br>
        <b>Global Shipping Alliances & OEMs:</b> {', '.join(vm.get('global_oems', []))}</p>
        <br><br>
        <p><b>Submitted By:</b> Principal Strategic Sourcing & Category Lead, Jubail Petrochemical Complex<br>
        <b>Approved By:</b> Chief Procurement Officer (CPO) / Executive Committee</p>
    </body>
    </html>
    """

    memo_preview_html = f"""<div class="card-memo-preview"><h3 style="color:#0F172A; margin-top:0;">📋 CPO Executive Decision Briefing Preview</h3><p style="color:#334155; font-size:0.95rem; line-height:1.6;">Category review for <b>{selected_sub}</b> ({pol_pod_display}) establishes an audited contract Should-Cost baseline of <b>{unit} {total_val:,.2f}</b>.<br>The contractor break-even operating floor is <b>{data.get('metric_card_2_value', '-')}</b>, with supplier margin / chokepoint surcharges at <b>{data.get('metric_card_3_value', '-')}</b>.</p><div style="margin: 12px 0;"><span class="badge-pill badge-amber">Kraljic: {k_data.get('quadrant', 'Strategic')}</span><span class="badge-pill badge-blue">Horizon: {k_data.get('contract_horizon', '1-2 Years Framework')}</span><span class="badge-pill badge-red">Max Risk Score: {data.get('total_metric_value', 18)}/25</span></div><p style="color:#64748B; font-size:0.85rem; margin-bottom:0;"><b>Local Content Route:</b> Priority allocation to Tier-1 leaders (<i>{', '.join(vm.get('tier_1_local', [])[:2])}</i>).</p></div>"""
    st.markdown(memo_preview_html, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
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
