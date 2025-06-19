import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf
from dotenv import load_dotenv
import os
from groq import Groq
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class StockAnalyzer:
    def __init__(self):
        pass
        
    def get_stock_data(self, symbol, market):
        """Get stock data using yfinance"""
        try:
            # Handle symbol based on market
            if market == 'Indian Stocks':
                if not (symbol.endswith('.NS') or symbol.endswith('.BO')):
                    ticker = f"{symbol}.NS"
                else:
                    ticker = symbol
            else:  # US Stocks
                ticker = symbol.replace('.NS', '').replace('.BO', '')
            
            # Get historical data
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y", interval="1wk")
            
            if df.empty:
                st.error(f"No data found for {ticker}")
                return None
                
            return df, stock.info
                
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            return None, None

    def get_stock_news(self, company_name):
        """Fetch latest news articles for the given company using DuckDuckGo's API"""
        try:
            with DDGS() as ddgs:
                news_results = ddgs.news(
                    keywords=company_name,
                    region='wt-wt',
                    safesearch='Moderate',
                    timelimit='d',
                    max_results=5
                )
                return list(news_results)
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")
            return None
    
    def process_stock_data(self, df):
        if df is None or df.empty:
            return None
        
        try:
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if all(col in df.columns for col in required_columns):
                return df
            else:
                st.error("Missing required columns in data")
                return None
                
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            return None

    def get_currency_symbol(self, market, stock_info):
        """Get currency symbol based on market and stock info"""
        if market == 'Indian Stocks':
            return '₹'
        return '$'

    def format_currency(self, value, currency_symbol):
        """Format currency with appropriate symbol and formatting"""
        if currency_symbol == '₹':
            return f"{currency_symbol}{value:,.2f}"
        return f"{currency_symbol}{value:.2f}"

def main():
    st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
    st.title("📈 Stock Analysis Dashboard")

    # Sidebar
    st.sidebar.header("Settings")
    
    # Default symbols with corrected format
    default_symbols = {
        'Indian Stocks': [
            'RELIANCE.NS',
            'TCS.NS',
            'HDFCBANK.NS',
            'INFY.NS',
            'ICICIBANK.NS',
            'BHARTIARTL.NS',
            'WIPRO.NS',
            'ZOMATO.NS',
            'PAYTM.NS',
            'JIOFIN.NS'
        ],
        'US Stocks': [
            'AAPL',
            'GOOGL',
            'MSFT',
            'AMZN',
            'TSLA',
            'META',
            'NVDA',
            'NFLX',
            'JPM',
            'V'
        ]
    }
    
    # Market selection
    market = st.sidebar.radio("Select Market", ['Indian Stocks', 'US Stocks'])
    
    # Stock selection
    selected_symbol = st.sidebar.selectbox("Select Stock", default_symbols[market])
    
    # Custom symbol input
    st.sidebar.markdown("""
    **For Indian Stocks:**
    - Add '.NS' for NSE stocks (e.g., RELIANCE.NS)
    - Add '.BO' for BSE stocks (e.g., RELIANCE.BO)
    """)
    custom_symbol = st.sidebar.text_input("Or enter custom symbol:")
    
    if custom_symbol:
        selected_symbol = custom_symbol

    # Initialize analyzer
    analyzer = StockAnalyzer()

    try:
        with st.spinner('Fetching stock data...'):
            # Get and process data
            result = analyzer.get_stock_data(selected_symbol, market)
            if result is None:
                st.error("Failed to fetch data")
                return
                
            df, stock_info = result
            if df is None:
                return
                
            df = analyzer.process_stock_data(df)
            
            # Get currency symbol
            currency_symbol = analyzer.get_currency_symbol(market, stock_info)

        if df is not None:
            # Create two columns
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f"📊 {selected_symbol} Price Chart")
                
                # Candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])
                
                fig.update_layout(
                    yaxis_title=f"Price ({currency_symbol})",
                    xaxis_title="Date",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)

                # Volume chart in an expander
                with st.expander("Show Trading Volume Chart"):
                    volume_fig = go.Figure(data=[go.Bar(x=df.index, y=df['Volume'])])
                    volume_fig.update_layout(
                        title=f"{selected_symbol} Trading Volume",
                        yaxis_title="Volume",
                        xaxis_title="Date",
                        template="plotly_white"
                    )
                    st.plotly_chart(volume_fig, use_container_width=True)

            with col2:
                st.subheader("📌 Key Statistics")
                
                # Calculate metrics
                latest_price = df['Close'].iloc[-1]
                price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
                price_change_pct = (price_change / df['Close'].iloc[-2]) * 100
                
                # Display metrics with proper currency
                st.metric("Latest Price", 
                         analyzer.format_currency(latest_price, currency_symbol),
                         f"{price_change_pct:+.2f}%")
                st.metric("52-Week High", 
                         analyzer.format_currency(df['High'].max(), currency_symbol))
                st.metric("52-Week Low", 
                         analyzer.format_currency(df['Low'].min(), currency_symbol))
                st.metric("Average Volume", f"{int(df['Volume'].mean()):,}")

                # Moving averages
                df['MA50'] = df['Close'].rolling(window=50).mean()
                df['MA200'] = df['Close'].rolling(window=200).mean()
                
                st.subheader("📉 Moving Averages")
                if len(df) >= 50:
                    st.metric("50-Day MA", 
                             analyzer.format_currency(df['MA50'].iloc[-1], currency_symbol))
                if len(df) >= 200:
                    st.metric("200-Day MA", 
                             analyzer.format_currency(df['MA200'].iloc[-1], currency_symbol))

            # Technical Indicators
            st.subheader("📈 Technical Indicators")
            # RSI calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            # Display RSI chart
            rsi_fig = go.Figure(data=[go.Scatter(x=df.index, y=df['RSI'])])
            rsi_fig.update_layout(
                title="Relative Strength Index (RSI)",
                yaxis_title="RSI",
                template="plotly_white"
            )
            st.plotly_chart(rsi_fig, use_container_width=True)

            # Display latest news
            st.subheader("📰 Latest News")
            company_name = stock_info.get('longName') or stock_info.get('shortName') or selected_symbol

            news_articles = analyzer.get_stock_news(company_name)

            if news_articles:
                for article in news_articles:
                    # Display each article in a container
                    with st.container():
                        st.markdown(f"### [{article['title']}]({article['url']})")
                        cols = st.columns([1, 4])
                        if 'image' in article and article['image']:
                            cols[0].image(article['image'], use_container_width=True)
                        else:
                            # Placeholder image if none is available
                            cols[0].image("https://via.placeholder.com/150", use_container_width=True)
                        cols[1].write(article.get('body', 'No summary available.'))
                        # Display additional info
                        st.write(f"**Source:** {article.get('source', 'Unknown')}  |  **Published at:** {article.get('date')}")
                        st.write("---")
            else:
                st.write("No news articles found.")

            # Chat interface (optional, placeholder)
            st.subheader("💬 Chat with Stock Analysis")
            user_question = st.text_input("Ask a question about this stock:")

            if user_question:
                with st.spinner("Analyzing..."):
                    prompt = f"""Stock: {selected_symbol}
Market: {market}
Latest Price: {analyzer.format_currency(latest_price, currency_symbol)}
52-Week Range: {analyzer.format_currency(df['Low'].min(), currency_symbol)} - {analyzer.format_currency(df['High'].max(), currency_symbol)}

News: {len(news_articles)} articles found
{chr(10).join([news_articles[i]['title'] for i in range(min(5, len(news_articles)))])}

User Question: {user_question}

Please provide a detailed and informative answer based on the available data.
"""

                    try:
                        response = groq_client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a professional stock market analyst with expertise in both Indian and US markets."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            model="mixtral-8x7b-32768",
                            temperature=0.3,
                        )
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")

        else:
            st.error("Unable to fetch data for the selected symbol")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please try another symbol or check if the stock exists")

if __name__ == "__main__":
    main()