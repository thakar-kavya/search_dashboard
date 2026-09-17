import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.parse

st.set_page_config(
    page_title="Women Ethnic Search Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

SHEET_ID = "12uVqwpXwUquW3jLySF3ue5fDCkEeX1PxYgvqPDqskWE"

def build_gviz_url(sheet_name, cell_range=None):
    encoded_name = urllib.parse.quote(sheet_name)
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
    if cell_range:
        url += f"&range={cell_range}"
    return url

def clean_numeric_dataframe(df):
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].astype(str).str.contains('%').any():
            df[f"{col}_num"] = df[col].astype(str).str.rstrip('%').replace(['-', 'nan', ''], '0').astype(float)
        elif df[col].dtype == 'object':
            cleaned_series = df[col].astype(str).str.replace(',', '').str.replace('$', '')
            numeric_series = pd.to_numeric(cleaned_series, errors='coerce')
            if not numeric_series.isna().all():
                df[col] = numeric_series.fillna(0)
    return df

@st.cache_data(ttl=120)
def load_all_tabs():
    sc_url = build_gviz_url("SC level")
    df_sc = pd.read_csv(sc_url, skiprows=5)
    df_sc = clean_numeric_dataframe(df_sc)

    vert_url = build_gviz_url("Vertical level", "A6:S54")
    df_vert = pd.read_csv(vert_url)
    df_vert = clean_numeric_dataframe(df_vert)

    try:
        kw_url = build_gviz_url("Vertical x storeID")
        df_kw = pd.read_csv(kw_url, skiprows=5)
    except Exception:
        kw_url = build_gviz_url("Keyword x Store path")
        df_kw = pd.read_csv(kw_url, skiprows=5)
    df_kw = clean_numeric_dataframe(df_kw)

    return df_sc, df_vert, df_kw

st.title("👗 Women Ethnic Search Intelligence Dashboard")

try:
    df_sc, df_vert, df_kw = load_all_tabs()

    tab1, tab2, tab3 = st.tabs([
        "📊 Supercategory (SC) Level & Observations", 
        "👗 Vertical Level Performance", 
        "🔥 Spiking Trends, Keywords & Store Paths"
    ])

    # ==============================================================================
    # TAB 1: SUPERCATEGORY (SC) LEVEL & CONSOLIDATED OBSERVATIONS
    # ==============================================================================
    with tab1:
        st.header("August 2026 — Executive Summary Header")
        
        # Top Metrics in Millions
        m1, m2, m3 = st.columns(3)
        with m1:
            st.subheader("WE Total")
            st.metric("Total Searches", "118.71 M", delta="15.51% MoM | -1.82% YoY")
            st.metric("CTR", "54.84%", delta="-2.60% MoM | +1.77% YoY", delta_color="normal")
            st.metric("CVR", "0.60%", delta="-1.67% MoM | -1.78% YoY", delta_color="normal")

        with m2:
            st.subheader("Women Ethnic Contemporary")
            st.metric("Total Searches", "75.05 M", delta="12.85% MoM | +2.63% YoY")
            st.metric("CTR", "53.82%", delta="-3.19% MoM | +0.90% YoY", delta_color="normal")
            st.metric("CVR", "0.64%", delta="-4.50% MoM | -1.24% YoY", delta_color="normal")

        with m3:
            st.subheader("Women Ethnic Core")
            st.metric("Total Searches", "43.66 M", delta="20.39% MoM | -8.62% YoY")
            st.metric("CTR", "56.58%", delta="-1.75% MoM | +3.42% YoY", delta_color="normal")
            st.metric("CVR", "0.54%", delta="+5.40% MoM | -2.48% YoY", delta_color="normal")

        st.divider()

        # Consolidated Summary Observations Section
        st.header("📋 Consolidated Executive Observations")
        
        col_green, col_red = st.columns(2)
        
        with col_green:
            st.success("### 🟢 Green Flags (Growth Drivers & Opportunities)")
            st.markdown("""
            * **WE Core Strong MoM Rebound**: Core searches jumped **+20.39% MoM** accompanied by a healthy **+5.40% CVR improvement**, driven by festive/seasonal demand.
            * **Massive Category Spikes**: 
                * **Sharara** surging by **+262.13% MoM** (Bottomwear & Ethnic Sets).
                * **Kaftan dresses** up **+209.55% MoM**.
                * **Sambalpuri kurti sets** spiking by **+196.99% MoM**.
            * **High-Performing Verticals**:
                * **WomenSalwarKurtaDupatta**: Outstanding YoY expansion (+64.33% Searches, +76.26% Units).
                * **WomenSalwar**: Phenomenal growth (+184.30% YoY Searches, +285.61% YoY Units).
            * **Fabric / Attribute Demand**: **Cotton** experiencing strong cross-vertical momentum (+64.71% in Kurtas/Sets, +42.51% in Sarees).
            """)

        with col_red:
            st.error("### 🔴 Red Flags (Conversion Dips & Assortment Gaps)")
            st.markdown("""
            * **Contemporary CVR Drop**: Women Ethnic Contemporary searches grew (+12.85% MoM), but CVR dropped by **-4.50% MoM**, indicating search traffic is not converting efficiently.
            * **Assortment & Search Redirection Gaps**:
                * **Umbrella Kurti Sets**: High spike (+36.82%), but flagged for **poor assortment** requiring manual ingestion in search indexing.
                * **Dola Silk**: Search spike of +119.70%, but severely impacted by **poor CTR & CVR**, signaling pricing or listing quality friction.
            * **Dipping Verticals (YoY Contracts)**:
                * **WomenEthnicDress**: -33.92% YoY Searches (-14.78% Units).
                * **WomenLehengaCholi**: -25.59% YoY Searches.
                * **WomenEthnicGown**: -31.58% YoY Searches.
            """)

        st.divider()

        # SC Visual Representations
        st.header("📈 SC Level Visual Analytics")
        sc_chart_col1, sc_chart_col2 = st.columns(2)

        with sc_chart_col1:
            sc_volume_data = pd.DataFrame({
                "Super Category": ["WE Contemporary", "WE Core", "WE Contemporary", "WE Core"],
                "Period": ["Jul 2026", "Jul 2026", "Aug 2026", "Aug 2026"],
                "Searches (Millions)": [66.51, 36.26, 75.05, 43.66]
            })
            fig_sc_bar = px.bar(
                sc_volume_data, x="Period", y="Searches (Millions)", color="Super Category",
                barmode="group", text_auto=True, title="MoM Search Volume Comparison (Jul '26 vs Aug '26)"
            )
            st.plotly_chart(fig_sc_bar, use_container_width=True)

        with sc_chart_col2:
            sc_rate_data = pd.DataFrame({
                "Super Category": ["WE Contemporary", "WE Core", "WE Total"],
                "MoM Search Growth %": [12.85, 20.39, 15.51],
                "MoM CVR Growth %": [-4.50, 5.40, -1.67]
            })
            fig_sc_rates = px.bar(
                sc_rate_data, x="Super Category", y=["MoM Search Growth %", "MoM CVR Growth %"],
                barmode="group", title="MoM Search Growth vs CVR Change %"
            )
            st.plotly_chart(fig_sc_rates, use_container_width=True)

        st.subheader("Raw SC Level Data Matrix")
        st.dataframe(df_sc, use_container_width=True)

    # ==============================================================================
    # TAB 2: VERTICAL LEVEL PERFORMANCE
    # ==============================================================================
    with tab2:
        st.header("👗 Vertical Level Trends & Analysis")
        
        st.info("""
        **Vertical Executive Summary:** Search volume is heavily concentrated in **WomenSari**, **WomenEthnicSet**, and **WomenKurtaAndKurti**. 
        **WomenSalwarKurtaDupatta** and **WomenSalwar** are emerging as major growth engines (+64% to +184% YoY search spikes).
        """)

        first_vert_col = df_vert.columns[0]
        vert_cols = [c for c in df_vert.columns if df_vert[c].dtype in ['int64', 'float64']]

        v_col1, v_col2 = st.columns(2)
        with v_col1:
            selected_verticals = st.multiselect(
                "Select Verticals to Compare", 
                options=df_vert[first_vert_col].dropna().unique(),
                default=df_vert[first_vert_col].dropna().unique()[:6]
            )
        with v_col2:
            vert_metric = st.selectbox("Select Metric for Charting", vert_cols, index=0)

        filtered_vert = df_vert[df_vert[first_vert_col].isin(selected_verticals)]

        v_chart1, v_chart2 = st.columns(2)
        with v_chart1:
            fig_vbar = px.bar(
                filtered_vert, x=first_vert_col, y=vert_metric, color=first_vert_col,
                title=f"{vert_metric} across Selected Verticals"
            )
            st.plotly_chart(fig_vbar, use_container_width=True)

        with v_chart2:
            if len(vert_cols) >= 2:
                fig_vscat = px.scatter(
                    filtered_vert, x=vert_cols[0], y=vert_cols[1], size=vert_cols[2] if len(vert_cols)>2 else None,
                    color=first_vert_col, hover_name=first_vert_col, title="Vertical Metric Correlation Scatter"
                )
                st.plotly_chart(fig_vscat, use_container_width=True)

        st.subheader("Vertical Level Data Grid (Range A6:S54)")
        st.dataframe(filtered_vert, use_container_width=True)

    # ==============================================================================
    # TAB 3: KEYWORD, SPIKING TRENDS & STORE PATHS
    # ==============================================================================
    with tab3:
        st.header("🔥 Spiking Keywords & Search Redirection Analysis")

        st.subheader("MoM Demand Surges & Attribute Trend Analysis")
        
        spikes_df = pd.DataFrame([
            {"Trend / Keyword": "Sharara", "Vertical": "Bottomwear & Ethnic Sets", "MoM Spike %": "+262.13%", "Demand Category": "Style Surge", "Observation": "Massive seasonal demand surge"},
            {"Trend / Keyword": "Kaftan dress", "Vertical": "Kurta Kurtis & ethnic sets", "MoM Spike %": "+209.55%", "Demand Category": "Comfort / Casual", "Observation": "Emerging high-growth trend"},
            {"Trend / Keyword": "sambalpuri kurti sets", "Vertical": "Kurta Kurtis & ethnic sets", "MoM Spike %": "+196.99%", "Demand Category": "Regional / Weave", "Observation": "Strong ethnic craft preference"},
            {"Trend / Keyword": "Dola Silk", "Vertical": "Saris", "MoM Spike %": "+119.70%", "Demand Category": "Fabric / Texture", "Observation": "⚠️ Spiking searches but poor CTR & CVR"},
            {"Trend / Keyword": "gotta patti", "Vertical": "Saris", "MoM Spike %": "+118.00%", "Demand Category": "Occasion / Work", "Observation": "Festive embroidary demand"},
            {"Trend / Keyword": "Skirt", "Vertical": "Bottomwear", "MoM Spike %": "+114.75%", "Demand Category": "Style / Fusion", "Observation": "High fusion wear growth"},
            {"Trend / Keyword": "yellow saree", "Vertical": "Saris", "MoM Spike %": "+84.31%", "Demand Category": "Occasion (Haldi)", "Observation": "Wedding/Haldi ritual query"},
            {"Trend / Keyword": "haldi outfit", "Vertical": "Kurta Kurtis & Saris", "MoM Spike %": "+70.77%", "Demand Category": "Event Specific", "Observation": "High intent occasion query"},
            {"Trend / Keyword": "sleeveless kurti", "Vertical": "Kurta Kurtis & sets", "MoM Spike %": "+70.38%", "Demand Category": "Silhouette", "Observation": "Summer style preference"},
            {"Trend / Keyword": "Cotton", "Vertical": "Kurta Kurtis & Ethnic sets", "MoM Spike %": "+64.71%", "Demand Category": "Core Fabric", "Observation": "Primary fabric driver across categories"},
            {"Trend / Keyword": "short kurti", "Vertical": "Kurta Kurtis", "MoM Spike %": "+61.07%", "Demand Category": "Casual Wear", "Observation": "Youth/college staple"},
            {"Trend / Keyword": "indo western", "Vertical": "Kurta Kurtis & sets", "MoM Spike %": "+61.75%", "Demand Category": "Fusion", "Observation": "Growing fusion preference"},
            {"Trend / Keyword": "bandhani sarees", "Vertical": "Saris", "MoM Spike %": "+51.85%", "Demand Category": "Craft / Print", "Observation": "Traditional print surge"},
            {"Trend / Keyword": "umbrella kurti sets", "Vertical": "Kurta Kurtis & sets", "MoM Spike %": "+36.82%", "Demand Category": "Silhouette", "Observation": "⚠️ Poor assortment, requires manual search ingestion"}
        ])

        st.dataframe(spikes_df, use_container_width=True)

        st.divider()

        st.subheader("Keyword x Store Path Redirection Matrix")
        
        search_kw = st.text_input("🔍 Filter by Keyword, Store ID, or Vertical", "")
        if search_kw:
            mask = df_kw.astype(str).apply(lambda row: row.str.contains(search_kw, case=False).any(), axis=1)
            filtered_kw = df_kw[mask]
        else:
            filtered_kw = df_kw

        st.dataframe(filtered_kw, use_container_width=True)

        kw_numeric = [c for c in filtered_kw.columns if filtered_kw[c].dtype in ['int64', 'float64']]
        if len(kw_numeric) >= 2:
            st.subheader("Redirection Efficiency Scatter Chart")
            fig_kw_scatter = px.scatter(
                filtered_kw, x=kw_numeric[0], y=kw_numeric[1], 
                hover_data=filtered_kw.columns[:3], 
                title=f"{kw_numeric[0]} vs {kw_numeric[1]} (Keyword x Store Path)"
            )
            st.plotly_chart(fig_kw_scatter, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dashboard: {e}. Please ensure Google Sheet sharing permissions are set to 'Anyone with the link can view'.")
