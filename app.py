import pandas as pd
import streamlit as st
from PIL import Image
import base64
import io
import os
import plotly.express as px
import plotly.graph_objects as go
import datetime

def style_chart(fig):
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1E3D59'),
        title_font=dict(size=24, color='#1E3D59'),
        legend_font=dict(size=12),
        xaxis=dict(
            gridcolor='#E8EEF2',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            gridcolor='#E8EEF2',
            tickfont=dict(size=12)
        ),
        margin=dict(t=50, l=50, r=30, b=50)
    )
    return fig

st.set_page_config(
    page_title="Global Companies Rankings",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        background-color: #1E3D59;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #FFFFFF;
        font-size: 2.8em;
        margin-bottom: 15px;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .sub-header {
        color: #F5F5F5;
        font-size: 1.3em;
    }
    .metric-card {
        background: linear-gradient(135deg, #17428D, #1E3D59);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-align: center;
        margin: 10px 0;
        color: white;
    }
    .metric-card h3 {
        color: #B8D9F5;
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .metric-card h2 {
        color: #FFFFFF;
        font-size: 1.8em;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 15px 20px;
        background-color: #F8F9FA;
        border-radius: 5px 5px 0 0;
        font-weight: 500;
        color: #1E3D59;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E8EEF2;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF;
        padding: 10px 10px 0 10px;
        border-radius: 10px 10px 0 0;
        gap: 5px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stDownloadButton button {
        background: linear-gradient(135deg, #17428D, #1E3D59);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .dataframe {
        background-color: #FFFFFF;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stats-card {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .footer {
        background: linear-gradient(135deg, #17428D, #1E3D59);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>🌍 Global Companies Rankings Dashboard</h1>
        <p class="sub-header">Comprehensive Analysis of World's Leading Companies</p>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        
        df = pd.read_csv("final.csv")
    except FileNotFoundError:
        try:
            
            df = pd.read_csv("data/final.csv")
        except FileNotFoundError:
            
            sample_data = {
                'Name': ['Apple', 'Microsoft', 'Google', 'Amazon', 'Meta'],
                'Market Cap': ['3610', '2971', '2116', '2271', '1706'],
                'Price': ['240.36', '399.73', '174.70', '214.35', '673.70']
            }
            df = pd.DataFrame(sample_data)
            st.warning("""
                ⚠️ Using sample data because 'final.csv' was not found.
                Please ensure your data file is properly uploaded.
                Expected file structure:
                - app.py
                - final.csv
                - requirements.txt
            """)
    
    try:
        df['Market Cap'] = df['Market Cap'].astype(str).str.replace(' ', '').astype(float)
        
        df['Price'] = df['Price'].astype(float)
        return df
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return pd.DataFrame(columns=['Name', 'Market Cap', 'Price'])

try:
    data = load_data().copy()
    if data.empty:
        st.warning("No data available. Please check your data source.")
        st.stop()
except Exception as e:
    st.error(f"Failed to process data: {e}")
    st.stop()

st.sidebar.markdown("## 🔍 Filter Options")
st.sidebar.markdown("---")

with st.sidebar:
   
    number_of_companies = st.slider("Number of Companies to Display", 5, len(data), 25)
    
    st.markdown("### 💰 Market Cap Filter (Billion USD)")
    market_cap_range = st.slider(
        "Select Range",
        float(data['Market Cap'].min()),
        float(data['Market Cap'].max()),
        (float(data['Market Cap'].min()), float(data['Market Cap'].max()))
    )
    
    st.markdown("### 💵 Stock Price Filter (USD)")
    price_range = st.slider(
        "Select Range",
        float(data['Price'].min()),
        float(data['Price'].max()),
        (float(data['Price'].min()), float(data['Price'].max()))
    )
    
    search_term = st.text_input("🔍 Search Company")
    
    st.markdown("### 📊 Sort By")
    sort_by = st.selectbox(
        "Order",
        ["Market Cap (High to Low)", "Market Cap (Low to High)", 
         "Price (High to Low)", "Price (Low to High)", 
         "Company Name (A-Z)"]
    )

filtered_data = data[
    (data['Market Cap'].between(market_cap_range[0], market_cap_range[1])) &
    (data['Price'].between(price_range[0], price_range[1]))
]

if search_term:
    filtered_data = filtered_data[filtered_data['Name'].str.contains(search_term, case=False)]

sort_dict = {
    "Market Cap (High to Low)": ('Market Cap', False),
    "Market Cap (Low to High)": ('Market Cap', True),
    "Price (High to Low)": ('Price', False),
    "Price (Low to High)": ('Price', True),
    "Company Name (A-Z)": ('Name', True)
}
sort_col, sort_asc = sort_dict[sort_by]
filtered_data = filtered_data.sort_values(sort_col, ascending=sort_asc)
filtered_data = filtered_data.head(number_of_companies)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Companies</h3>
            <h2>{}</h2>
        </div>
    """.format(len(filtered_data)), unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="metric-card">
            <h3>💰 Total Market Cap</h3>
            <h2>${:,.0f}B</h2>
        </div>
    """.format(filtered_data['Market Cap'].sum()), unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="metric-card">
            <h3>📈 Average Market Cap</h3>
            <h2>${:,.0f}B</h2>
        </div>
    """.format(filtered_data['Market Cap'].mean()), unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="metric-card">
            <h3>💵 Average Stock Price</h3>
            <h2>${:,.2f}</h2>
        </div>
    """.format(filtered_data['Price'].mean()), unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Rankings", "📈 Market Analysis", "💰 Price Analysis", "🔍 Insights"])

with tab1:
   
    st.markdown("### 🏢 Company Rankings")
    
   
    image_column = st.column_config.ImageColumn(label="", width="medium")
    name_column = st.column_config.TextColumn(label="Company Name", width="large")
    market_cap_column = st.column_config.NumberColumn(
        label="Market Cap 💰", 
        help="In Billion USD",
        format="$%.2f B"
    )
    price_column = st.column_config.NumberColumn(
        label="Stock Price 📈",
        help="Previous day closing price (USD)",
        format="$%.2f"
    )

    st.dataframe(
        filtered_data,
        column_config={
            "Logo": image_column,
            "Name": name_column,
            "Market Cap": market_cap_column,
            "Price": price_column
        },
        height=400
    )

with tab2:
   
    st.markdown("""
        <div style='background: linear-gradient(135deg, #1E3D59, #17428D); 
                    padding: 25px; 
                    border-radius: 10px; 
                    margin-bottom: 25px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='color: white; text-align: center; margin-bottom: 0; font-size: 2em;'>
                📈 Market Analysis Dashboard
            </h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                       padding: 20px; 
                       border-radius: 10px; 
                       box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                       border: 1px solid #E2E8F0;'>
                <h4 style='color: #1E3D59; text-align: center; margin-bottom: 15px; font-size: 1.2em;'>
                    🏢 Largest Company
                </h4>
                <p style='color: #2C5282; text-align: center; font-size: 1.4em; font-weight: bold; margin-bottom: 10px;'>
                    {}
                </p>
                <p style='color: #1E3D59; text-align: center; font-size: 1.2em;'>
                    ${:,.2f}B
                </p>
            </div>
        """.format(
            filtered_data.iloc[0]['Name'],
            filtered_data.iloc[0]['Market Cap']
        ), unsafe_allow_html=True)
    
    with col2:
        total_market_cap = filtered_data['Market Cap'].sum()
        top_5_market_cap = filtered_data.head(5)['Market Cap'].sum()
        concentration = (top_5_market_cap / total_market_cap) * 100
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                       padding: 20px; 
                       border-radius: 10px; 
                       box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                       border: 1px solid #E2E8F0;'>
                <h4 style='color: #1E3D59; text-align: center; margin-bottom: 15px; font-size: 1.2em;'>
                    💹 Top 5 Concentration
                </h4>
                <p style='color: #2C5282; text-align: center; font-size: 1.4em; font-weight: bold; margin-bottom: 10px;'>
                    {:.1f}%
                </p>
                <p style='color: #1E3D59; text-align: center; font-size: 1.2em;'>
                    of Total Market Cap
                </p>
            </div>
        """.format(concentration), unsafe_allow_html=True)
    
    with col3:
        avg_market_cap = filtered_data['Market Cap'].mean()
        median_market_cap = filtered_data['Market Cap'].median()
        ratio = avg_market_cap / median_market_cap
        st.markdown("""
            <div style='background: linear-gradient(135deg, #FFFFFF, #F8F9FA); 
                       padding: 20px; 
                       border-radius: 10px; 
                       box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                       border: 1px solid #E2E8F0;'>
                <h4 style='color: #1E3D59; text-align: center; margin-bottom: 15px; font-size: 1.2em;'>
                    📊 Mean/Median Ratio
                </h4>
                <p style='color: #2C5282; text-align: center; font-size: 1.4em; font-weight: bold; margin-bottom: 10px;'>
                    {:.2f}
                </p>
                <p style='color: #1E3D59; text-align: center; font-size: 1.2em;'>
                    Market Cap Distribution
                </p>
            </div>
        """.format(ratio), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        fig_market = go.Figure()
        fig_market.add_trace(go.Bar(
            x=filtered_data['Name'],
            y=filtered_data['Market Cap'],
            marker_color=filtered_data['Market Cap'],
            marker_colorscale='Blues',
            text=filtered_data['Market Cap'].round(1),
            textposition='outside',
            textfont=dict(size=12, color='#1E3D59'),
        ))
        
        fig_market.update_layout(
            title={
                'text': 'Market Capitalization Distribution',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='#1E3D59', family="Arial, sans-serif")
            },
            xaxis_tickangle=-45,
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            yaxis_title=dict(text='Market Cap (Billion USD)', font=dict(size=14, color='#1E3D59')),
            xaxis_title=dict(text='Companies', font=dict(size=14, color='#1E3D59')),
            showlegend=False,
            margin=dict(t=80, l=70, r=40, b=120),
            xaxis=dict(
                gridcolor='#E2E8F0',
                tickfont=dict(size=12, color='#1E3D59'),
                ticktext=filtered_data['Name'],
                tickvals=list(range(len(filtered_data))),
                tickmode='array'
            ),
            yaxis=dict(
                gridcolor='#E2E8F0',
                tickfont=dict(size=12, color='#1E3D59'),
                tickformat='$,.0f'
            )
        )
        
        fig_market.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Market Cap: $%{y:.2f}B<br>",
            textfont=dict(color='white')
        )
        
        st.plotly_chart(fig_market, use_container_width=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #F8F9FA, #FFFFFF); 
                       padding: 20px; 
                       border-radius: 10px; 
                       margin-top: 15px;
                       border: 1px solid #E2E8F0;
                       box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h4 style='color: #1E3D59; margin-bottom: 10px; font-size: 1.1em;'>💡 Distribution Insights</h4>
                <p style='color: #2C5282; font-size: 1em; line-height: 1.5;'>
                    The bar chart shows the significant market cap differences between companies,
                    highlighting the concentration of market value among top performers.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
       
        fig_pie = go.Figure(data=[go.Pie(
            labels=filtered_data.head(10)['Name'],
            values=filtered_data.head(10)['Market Cap'],
            hole=.3,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=px.colors.sequential.Blues_r),
            textfont=dict(size=12, color='#1E3D59'),
            pull=[0.1 if i == 0 else 0 for i in range(10)]
        )])
        
        fig_pie.update_layout(
            title={
                'text': 'Top 10 Companies Market Share',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color='#1E3D59', family="Arial, sans-serif")
            },
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.5,
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#1E3D59'),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#E2E8F0'
            ),
            margin=dict(t=80, l=50, r=50, b=100)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("""
            <div style='background: linear-gradient(135deg, #F8F9FA, #FFFFFF); 
                       padding: 20px; 
                       border-radius: 10px; 
                       margin-top: 15px;
                       border: 1px solid #E2E8F0;
                       box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h4 style='color: #1E3D59; margin-bottom: 10px; font-size: 1.1em;'>💡 Market Share Insights</h4>
                <p style='color: #2C5282; font-size: 1em; line-height: 1.5;'>
                    The donut chart illustrates market dominance of top 10 companies,
                    showing the relative market share distribution among industry leaders.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background: linear-gradient(135deg, #1E3D59, #17428D);
                    padding: 25px;
                    border-radius: 10px;
                    margin-top: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin-bottom: 15px; font-size: 1.4em;'>🎯 Market Trends Summary</h3>
            <p style='color: #E2E8F0; font-size: 1.1em; line-height: 1.6;'>
                The analysis reveals significant market concentration among top companies.
                The top 5 companies represent a substantial portion of the total market cap,
                indicating the dominant position of industry leaders in the global market.
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        
        fig_scatter = px.scatter(
            filtered_data,
            x='Market Cap',
            y='Price',
            size='Market Cap',
            color='Market Cap',
            hover_name='Name',
            title='Stock Price vs Market Cap Correlation'
        )
        fig_scatter.update_layout(height=500, title_x=0.5)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
     
        fig_box = px.box(
            filtered_data,
            y='Price',
            title='Stock Price Distribution'
        )
        fig_box.update_layout(height=500, title_x=0.5)
        st.plotly_chart(fig_box, use_container_width=True)

with tab4:
  
    st.markdown("""
        <div style='background-color: #1E3D59; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; text-align: center; margin-bottom: 0;'>📊 Statistical Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    def create_stats_card(title, stats_data, prefix="$"):
        stats_html = f"""
        <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: #1E3D59; text-align: center; margin-bottom: 20px; font-size: 1.3em;'>{title}</h3>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr style='background: #F5F7FA;'>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Count</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{int(stats_data['count'])}</td>
                </tr>
                <tr>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Mean</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['mean']:,.2f}</td>
                </tr>
                <tr style='background: #F5F7FA;'>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Std Dev</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['std']:,.2f}</td>
                </tr>
                <tr>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Min</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['min']:,.2f}</td>
                </tr>
                <tr style='background: #F5F7FA;'>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>25%</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['25%']:,.2f}</td>
                </tr>
                <tr>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Median</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['50%']:,.2f}</td>
                </tr>
                <tr style='background: #F5F7FA;'>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>75%</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['75%']:,.2f}</td>
                </tr>
                <tr>
                    <td style='padding: 12px; color: #1E3D59; font-weight: bold;'>Max</td>
                    <td style='padding: 12px; color: #1E3D59; text-align: right;'>{prefix}{stats_data['max']:,.2f}</td>
                </tr>
            </table>
        </div>
        """
        return stats_html

    with col1:
        stats_market = filtered_data['Market Cap'].describe()
        st.markdown(create_stats_card("Market Cap Statistics (Billion USD)", stats_market), unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: #F0F4F8; padding: 15px; border-radius: 10px; margin-top: 20px;'>
                <h4 style='color: #1E3D59; margin-bottom: 10px;'>💡 Market Cap Insights</h4>
                <p style='color: #2C5282; font-size: 0.9em;'>
                    The market capitalization distribution shows the concentration of value among top companies.
                    The gap between mean and median indicates market concentration among top performers.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        stats_price = filtered_data['Price'].describe()
        st.markdown(create_stats_card("Stock Price Statistics (USD)", stats_price), unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: #F0F4F8; padding: 15px; border-radius: 10px; margin-top: 20px;'>
                <h4 style='color: #1E3D59; margin-bottom: 10px;'>💡 Price Insights</h4>
                <p style='color: #2C5282; font-size: 0.9em;'>
                    Stock prices vary significantly across companies, influenced by factors like 
                    share structure and market perception rather than just company size.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='background: #1E3D59; padding: 20px; border-radius: 10px; margin-top: 30px;'>
            <h3 style='color: white; margin-bottom: 15px;'>🎯 Market Overview</h3>
            <p style='color: #B8D9F5; font-size: 1.1em; line-height: 1.6;'>
                This analysis covers the world's leading companies by market capitalization.
                The data shows significant variations in both market cap and stock prices,
                reflecting the diverse nature of global market leaders across different sectors.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"global_companies_ranking_{datetime.date.today()}.csv",
        mime="text/csv",
    )

st.markdown(
    f'<div class="footer">'
    f'<span style="font-size: 14px">📊 <strong>Source:</strong> companiesmarketcap.com | '
    f'📅 <strong>Last Updated:</strong> {datetime.date.today().strftime("%d.%m.%Y")} | '
    f'🔄 <strong>Auto-updates daily</strong></span>'
    '</div>',
    unsafe_allow_html=True
)
