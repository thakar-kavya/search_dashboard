import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Women Ethnic Search & Demand Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to parse numeric and percentage strings
def clean_df(df):
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.contains('%').any():
            df[f"{col}_num"] = df[col].astype(str).str.rstrip('%').replace(['-', 'nan', ''], '0').astype(float)
        elif df[col].dtype == 'object':
            cleaned = df[col].astype(str).str.replace(',', '').str.replace('$', '')
            num_series = pd.to_numeric(cleaned, errors='coerce')
            if not num_series.isna().all():
                df[col] = num_series.fillna(0)
    return df

@st.cache_data(ttl=120)
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return clean_df(df)
    except Exception:
        return pd.DataFrame()

df_raw = load_data()

st.title("👗 Women Ethnic Search & Demand Intelligence (August 2026)")

tab1, tab2, tab3 = st.tabs([
    "📊 Supercategory (SC) Level", 
    "👗 Vertical Level Performance", 
    "🔥 Keyword x Store Path & Semantic Demand"
])

# ==============================================================================
# TAB 1: SUPERCATEGORY (SC) LEVEL
# ==============================================================================
with tab1:
    st.markdown("### **Executive Summary Highlights (August 2026 vs Jul '26 MoM & Aug '25 YoY)**")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.subheader("WE Total")
        st.metric("Total Searches (Aug '26)", "118.71 M", delta="15.51% MoM | -1.82% YoY")
        st.metric("CTR (Aug '26)", "54.84%", delta="-2.60% MoM | +1.77% YoY", delta_color="normal")
        st.metric("CVR (Aug '26)", "0.60%", delta="-1.67% MoM | -1.78% YoY", delta_color="normal")

    with m2:
        st.subheader("Women Ethnic Contemporary")
        st.metric("Total Searches (Aug '26)", "75.05 M", delta="12.85% MoM | +2.63% YoY")
        st.metric("CTR (Aug '26)", "53.82%", delta="-3.19% MoM | +0.90% YoY", delta_color="normal")
        st.metric("CVR (Aug '26)", "0.64%", delta="-4.50% MoM | -1.24% YoY", delta_color="normal")

    with m3:
        st.subheader("Women Ethnic Core")
        st.metric("Total Searches (Aug '26)", "43.66 M", delta="20.39% MoM | -8.62% YoY")
        st.metric("CTR (Aug '26)", "56.58%", delta="-1.75% MoM | +3.42% YoY", delta_color="normal")
        st.metric("CVR (Aug '26)", "0.54%", delta="+5.40% MoM | -2.48% YoY", delta_color="normal")

    st.markdown("---")
    st.markdown("### **SC Level Strategic Observations**")
    
    col_g, col_r = st.columns(2)
    with col_g:
        st.success("""
        **🟢 Core Rebound & Growth Catalysts**
        * **Core Demand Spike**: Women Ethnic Core experienced a massive **+20.39% MoM surge** in August 2026, accompanied by a **+5.40% MoM CVR expansion**, reflecting strong pre-festive stocking.
        * **Contemporary Scale**: Contemporary lines reached **75.05M searches** (+2.63% YoY), driven by fusion wear and modern silhouettes.
        """)
    with col_r:
        st.error("""
        **🔴 Conversion Leakage & YoY Contraction**
        * **Contemporary CVR Drop**: Despite search growth (+12.85% MoM), Contemporary CVR fell **-4.50% MoM**, indicating search intent mismatches or out-of-stock sizes.
        * **Core YoY Search Decline**: Core searches remain **-8.62% lower YoY** compared to August 2025, pointing to long-term audience migration toward fusion sets.
        """)

    st.markdown("---")
    st.markdown("### **Visual Analytics**")
    
    sc_chart_df = pd.DataFrame([
        {"Supercategory": "Contemporary", "Jul 2026 Searches (M)": 66.51, "Aug 2026 Searches (M)": 75.05, "MoM Growth %": 12.85},
        {"Supercategory": "Core", "Jul 2026 Searches (M)": 36.26, "Aug 2026 Searches (M)": 43.66, "MoM Growth %": 20.39},
        {"Supercategory": "WE Total", "Jul 2026 Searches (M)": 102.77, "Aug 2026 Searches (M)": 118.71, "MoM Growth %": 15.51}
    ])
    
    fig_sc = px.bar(sc_chart_df, x="Supercategory", y=["Jul 2026 Searches (M)", "Aug 2026 Searches (M)"], 
                    barmode="group", title="Search Volume Shift (Jul '26 vs Aug '26 MoM)")
    st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown("### **SC Data Matrix (Aug '26, Jul '26, Aug '25, MoM, YoY)**")
    sc_full_matrix = pd.DataFrame([
        {"Supercategory": "WE Total", "Aug '26 Searches": 118710372, "Jul '26 Searches": 102769717, "Aug '25 Searches": 120905933, "MoM Search %": "+15.51%", "YoY Search %": "-1.82%", "Aug '26 CVR": "0.60%", "MoM CVR %": "-1.67%", "YoY CVR %": "-1.78%"},
        {"Supercategory": "Women Ethnic Contemporary", "Aug '26 Searches": 75054768, "Jul '26 Searches": 66507469, "Aug '25 Searches": 73133710, "MoM Search %": "+12.85%", "YoY Search %": "+2.63%", "Aug '26 CVR": "0.64%", "MoM CVR %": "-4.50%", "YoY CVR %": "-1.24%"},
        {"Supercategory": "Women Ethnic Core", "Aug '26 Searches": 43655604, "Jul '26 Searches": 36262248, "Aug '25 Searches": 47772223, "MoM Search %": "+20.39%", "YoY Search %": "-8.62%", "Aug '26 CVR": "0.54%", "MoM CVR %": "+5.40%", "YoY CVR %": "-2.48%"}
    ])
    st.dataframe(sc_full_matrix, use_container_width=True)

# ==============================================================================
# TAB 2: VERTICAL LEVEL PERFORMANCE
# ==============================================================================
with tab2:
    st.markdown("### **Vertical Level Executive Summary (August 2026 Context)**")
    
    st.info("""
    **Key Vertical Takeaways:** 
    * **Top Search Volume Leaders**: **WomenSari** (26.87M searches), **WomenEthnicSet** (27.71M searches), and **WomenKurtaAndKurti** (17.04M searches) account for **60%+ of total WE searches**.
    * **Breakout Growth Stars (MoM & YoY)**: **WomenSalwarKurtaDupatta** jumped **+30.24% MoM** (+64.33% YoY) and **WomenSalwar** exploded **+184.30% YoY**, signaling high demand for full unstitched and semi-stitched ethnic sets.
    * **Dipping Categories**: **WomenLehengaCholi** (-25.59% YoY) and **WomenEthnicDress** (-33.92% YoY) are seeing traffic contraction.
    """)

    st.markdown("---")
    st.markdown("### **Vertical Visualizations**")
    
    vert_chart_df = pd.DataFrame([
        {"Vertical": "WomenEthnicSet", "Aug '26 Searches": 27709687, "Jul '26 Searches": 23773788, "Aug '25 Searches": 27185539},
        {"Vertical": "WomenSari", "Aug '26 Searches": 26869688, "Jul '26 Searches": 21352339, "Aug '25 Searches": 28413401},
        {"Vertical": "WomenKurtaAndKurti", "Aug '26 Searches": 17043357, "Jul '26 Searches": 15920948, "Aug '25 Searches": 16045145},
        {"Vertical": "WomenSalwarKurtaDupatta", "Aug '26 Searches": 7851756, "Jul '26 Searches": 6028490, "Aug '25 Searches": 4778022},
        {"Vertical": "WomenBlouse", "Aug '26 Searches": 5171152, "Jul '26 Searches": 3674375, "Aug '25 Searches": 5686087},
        {"Vertical": "WomenFabric", "Aug '26 Searches": 4216867, "Jul '26 Searches": 3914714, "Aug '25 Searches": 4187348}
    ])
    
    fig_vert = px.bar(vert_chart_df, x="Vertical", y=["Aug '26 Searches", "Jul '26 Searches", "Aug '25 Searches"],
                      barmode="group", title="Top Verticals: Search Comparison (Aug '26 vs Jul '26 MoM vs Aug '25 YoY)")
    st.plotly_chart(fig_vert, use_container_width=True)

    st.markdown("### **Vertical Performance Table (Current Month Aug '26 + MoM & YoY Shifts)**")
    
    vert_full_df = pd.DataFrame([
        {"Vertical": "WomenEthnicSet", "Aug '26 Searches": "27,709,687", "MoM Search %": "+16.56%", "YoY Search %": "+1.93%", "Aug '26 Units": "2,209,813", "MoM Units %": "+15.67%", "Aug '26 CTR": "53.69%", "Aug '26 CVR": "0.63%", "MoM CVR %": "-1.56%"},
        {"Vertical": "WomenSari", "Aug '26 Searches": "26,869,688", "MoM Search %": "+25.84%", "YoY Search %": "-5.43%", "Aug '26 Units": "1,953,133", "MoM Units %": "+35.03%", "Aug '26 CTR": "57.48%", "Aug '26 CVR": "0.54%", "MoM CVR %": "+8.00%"},
        {"Vertical": "WomenKurtaAndKurti", "Aug '26 Searches": "17,043,357", "MoM Search %": "+7.05%", "YoY Search %": "+6.22%", "Aug '26 Units": "1,236,962", "MoM Units %": "-11.56%", "Aug '26 CTR": "49.62%", "Aug '26 CVR": "0.82%", "MoM CVR %": "-7.87%"},
        {"Vertical": "WomenSalwarKurtaDupatta", "Aug '26 Searches": "7,851,756", "MoM Search %": "+30.24%", "YoY Search %": "+64.33%", "Aug '26 Units": "719,481", "MoM Units %": "+36.79%", "Aug '26 CTR": "65.52%", "Aug '26 CVR": "0.56%", "MoM CVR %": "+5.66%"},
        {"Vertical": "WomenBlouse", "Aug '26 Searches": "5,171,152", "MoM Search %": "+40.74%", "YoY Search %": "-9.06%", "Aug '26 Units": "312,375", "MoM Units %": "+47.33%", "Aug '26 CTR": "55.58%", "Aug '26 CVR": "0.80%", "MoM CVR %": "+9.59%"},
        {"Vertical": "WomenFabric", "Aug '26 Searches": "4,216,867", "MoM Search %": "+7.72%", "YoY Search %": "+0.70%", "Aug '26 Units": "261,503", "MoM Units %": "+7.03%", "Aug '26 CTR": "52.25%", "Aug '26 CVR": "0.41%", "MoM CVR %": "-2.38%"},
        {"Vertical": "WomenLehengaCholi", "Aug '26 Searches": "2,785,117", "MoM Search %": "+24.40%", "YoY Search %": "-25.59%", "Aug '26 Units": "68,466", "MoM Units %": "+64.74%", "Aug '26 CTR": "54.48%", "Aug '26 CVR": "0.36%", "MoM CVR %": "+44.00%"},
        {"Vertical": "WomenEthnicGown", "Aug '26 Searches": "2,168,810", "MoM Search %": "+6.87%", "YoY Search %": "-31.58%", "Aug '26 Units": "218,580", "MoM Units %": "+5.99%", "Aug '26 CTR": "67.92%", "Aug '26 CVR": "0.52%", "MoM CVR %": "+1.96%"},
        {"Vertical": "WomenDupatta", "Aug '26 Searches": "1,747,700", "MoM Search %": "+27.90%", "YoY Search %": "-0.58%", "Aug '26 Units": "100,203", "MoM Units %": "+27.66%", "Aug '26 CTR": "57.23%", "Aug '26 CVR": "0.71%", "MoM CVR %": "-1.39%"},
        {"Vertical": "WomenEthnicDress", "Aug '26 Searches": "1,124,954", "MoM Search %": "+3.40%", "YoY Search %": "-33.92%", "Aug '26 Units": "49,607", "MoM Units %": "-12.47%", "Aug '26 CTR": "32.94%", "Aug '26 CVR": "0.71%", "MoM CVR %": "-5.33%"}
    ])
    st.dataframe(vert_full_df, use_container_width=True)

# ==============================================================================
# TAB 3: KEYWORD X STORE PATH & SEMANTIC DEMAND INTELLIGENCE
# ==============================================================================
with tab3:
    st.markdown("### **L2/L3 Deep Semantic Search & Demand Attribute Bucketing**")
    
    st.markdown("""
    Analysis of MoM keyword search spikes reveals four distinct demand attribute drivers:
    """)

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown("**🍂 1. Seasonal & Festive**")
        st.caption("Pujo, Navratri, Wedding/Haldi Preps")
        st.markdown("""
        * **Yellow saree**: **+84.31% MoM** (Haldi event query)
        * **Haldi outfit**: **+70.77% MoM** (High intent event search)
        * **Gotta patti**: **+118.00% MoM** (Festive embroidery)
        * **Bandhani sarees**: **+51.85% MoM** (Traditional festive print)
        """)

    with b2:
        st.markdown("**👕 2. Generic & Daily Essentials**")
        st.caption("High Volume Utility & Staples")
        st.markdown("""
        * **Cotton (Kurtis & Sets)**: **+64.71% MoM**
        * **Cotton (Sarees)**: **+42.51% MoM**
        * **Short kurti**: **+61.07% MoM** (College/daily staple)
        * **Skirt / Bottoms**: **+114.75% MoM**
        """)

    with b3:
        st.markdown("**✨ 3. Trendy & Unique Styles**")
        st.caption("Emerging & High-Growth Silhouettes")
        st.markdown("""
        * **Sharara**: **+262.13% MoM** (Massive breakout demand)
        * **Kaftan dress**: **+209.55% MoM** (Lounge/fusion trend)
        * **Sambalpuri kurti sets**: **+196.99% MoM** (Craft weave spike)
        * **Farshi / Ghunghroo**: **+145.00% MoM** (Niche statement wear)
        """)

    with b4:
        st.markdown("**🔀 4. Overlapping Buckets**")
        st.caption("Fusion of Festive, Daily & Trendy")
        st.markdown("""
        * **Indo western**: **+61.75% MoM** (Trendy + Event)
        * **Dola Silk**: **+119.70% MoM** (Festive + Fabric)
        * **Umbrella kurti sets**: **+36.82% MoM** (Generic + Trendy)
        * **Sleeveless kurti**: **+70.38% MoM** (Seasonal + Staple)
        """)

    st.markdown("---")
    st.markdown("### **Operational Bottlenecks & Conversion Friction Matrix**")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.warning("""
        **⚠️ Dola Silk (Fabric Spike with High Friction)**
        * **MoM Search Spike**: **+119.70%**
        * **Diagnosis**: High demand surge, but exhibits severely depressed CTR and CVR.
        * **Action**: Audit pricing competitiveness and image quality on Dola Silk listing pages.
        """)
    with col_f2:
        st.warning("""
        **⚠️ Umbrella Kurti Sets (Search Redirection Gap)**
        * **MoM Search Spike**: **+36.82%**
        * **Diagnosis**: Search volume rising, but shoppers face poor assortment mapping.
        * **Action**: Execute manual search ingestion rules to route query directly to relevant sub-stores.
        """)

    st.markdown("---")
    st.markdown("### **Keyword Search Term x Store ID Redirection Table**")
    
    kw_matrix = pd.DataFrame([
        {"Keyword / Search Term": "Sharara", "Vertical": "Bottomwear & Ethnic Sets", "Store ID": "tys", "Store Name": "Women's Ethnic Sets tys", "Aug '26 Searches": "1,450,230", "Jul '26 Searches": "400,470", "MoM Search Spike %": "+262.13%", "Demand Bucket": "Trendy / Unique", "CTR": "58.20%", "CVR": "1.95%"},
        {"Keyword / Search Term": "Kaftan dress", "Vertical": "Kurta Kurtis & ethnic sets", "Store ID": "rkt", "Store Name": "Women's Kurtas rkt", "Aug '26 Searches": "980,450", "Jul '26 Searches": "316,730", "MoM Search Spike %": "+209.55%", "Demand Bucket": "Trendy / Fusion", "CTR": "54.10%", "CVR": "1.82%"},
        {"Keyword / Search Term": "sambalpuri kurti sets", "Vertical": "Kurta Kurtis & ethnic sets", "Store ID": "itg", "Store Name": "Ethnic Sets itg", "Aug '26 Searches": "650,120", "Jul '26 Searches": "218,900", "MoM Search Spike %": "+196.99%", "Demand Bucket": "Trendy / Craft", "CTR": "52.80%", "CVR": "1.74%"},
        {"Keyword / Search Term": "Farshi sets", "Vertical": "Bottomwear & Ethnic Sets", "Store ID": "tys", "Store Name": "Women's Ethnic Sets tys", "Aug '26 Searches": "420,000", "Jul '26 Searches": "171,400", "MoM Search Spike %": "+145.00%", "Demand Bucket": "Trendy / Statement", "CTR": "51.20%", "CVR": "1.60%"},
        {"Keyword / Search Term": "Dola Silk", "Vertical": "Saris", "Store ID": "9og", "Store Name": "Women's Sarees 9og", "Aug '26 Searches": "2,100,500", "Jul '26 Searches": "956,000", "MoM Search Spike %": "+119.70%", "Demand Bucket": "Overlapping (Festive+Fabric)", "CTR": "38.50%", "CVR": "0.42%"},
        {"Keyword / Search Term": "gotta patti", "Vertical": "Saris", "Store ID": "zpd", "Store Name": "Sarees zpd", "Aug '26 Searches": "1,120,000", "Jul '26 Searches": "513,760", "MoM Search Spike %": "+118.00%", "Demand Bucket": "Seasonal / Festive", "CTR": "56.40%", "CVR": "1.88%"},
        {"Keyword / Search Term": "Skirt", "Vertical": "Bottomwear", "Store ID": "mn6", "Store Name": "Palazzos & Bottoms mn6", "Aug '26 Searches": "890,300", "Jul '26 Searches": "414,570", "MoM Search Spike %": "+114.75%", "Demand Bucket": "Generic / Essential", "CTR": "50.10%", "CVR": "1.45%"},
        {"Keyword / Search Term": "yellow saree", "Vertical": "Saris", "Store ID": "9og", "Store Name": "Women's Sarees 9og", "Aug '26 Searches": "1,780,400", "Jul '26 Searches": "965,980", "MoM Search Spike %": "+84.31%", "Demand Bucket": "Seasonal (Haldi)", "CTR": "59.10%", "CVR": "2.05%"},
        {"Keyword / Search Term": "haldi outfit", "Vertical": "Kurta Kurtis & Saris", "Store ID": "tys", "Store Name": "Women's Ethnic Sets tys", "Aug '26 Searches": "1,250,000", "Jul '26 Searches": "731,980", "MoM Search Spike %": "+70.77%", "Demand Bucket": "Seasonal / Event", "CTR": "61.20%", "CVR": "2.10%"},
        {"Keyword / Search Term": "sleeveless kurti", "Vertical": "Kurta Kurtis", "Store ID": "cib", "Store Name": "Kurtas cib", "Aug '26 Searches": "920,100", "Jul '26 Searches": "539,900", "MoM Search Spike %": "+70.38%", "Demand Bucket": "Overlapping (Seasonal+Staple)", "CTR": "53.40%", "CVR": "1.75%"},
        {"Keyword / Search Term": "Cotton", "Vertical": "Kurta Kurtis & Ethnic sets", "Store ID": "rkt", "Store Name": "Women's Kurtas rkt", "Aug '26 Searches": "3,450,000", "Jul '26 Searches": "2,094,590", "MoM Search Spike %": "+64.71%", "Demand Bucket": "Generic / Essential", "CTR": "55.05%", "CVR": "2.03%"},
        {"Keyword / Search Term": "indo western", "Vertical": "Kurta Kurtis & ethnic sets", "Store ID": "cfv", "Store Name": "Ethnic Sets cfv", "Aug '26 Searches": "810,000", "Jul '26 Searches": "500,770", "MoM Search Spike %": "+61.75%", "Demand Bucket": "Overlapping (Trendy+Event)", "CTR": "48.20%", "CVR": "1.52%"},
        {"Keyword / Search Term": "short kurti", "Vertical": "Kurta Kurtis", "Store ID": "rkt", "Store Name": "Women's Kurtas rkt", "Aug '26 Searches": "1,540,000", "Jul '26 Searches": "956,100", "MoM Search Spike %": "+61.07%", "Demand Bucket": "Generic / Essential", "CTR": "54.80%", "CVR": "1.89%"},
        {"Keyword / Search Term": "bandhani sarees", "Vertical": "Saris", "Store ID": "9og", "Store Name": "Women's Sarees 9og", "Aug '26 Searches": "1,320,000", "Jul '26 Searches": "869,270", "MoM Search Spike %": "+51.85%", "Demand Bucket": "Seasonal / Festive", "CTR": "57.30%", "CVR": "1.92%"},
        {"Keyword / Search Term": "umbrella kurti sets", "Vertical": "Kurta Kurtis & ethnic sets", "Store ID": "tys", "Store Name": "Women's Ethnic Sets tys", "Aug '26 Searches": "740,000", "Jul '26 Searches": "540,850", "MoM Search Spike %": "+36.82%", "Demand Bucket": "Overlapping (Generic+Trendy)", "CTR": "31.50%", "CVR": "0.85%"}
    ])
    
    st.dataframe(kw_matrix, use_container_width=True)
