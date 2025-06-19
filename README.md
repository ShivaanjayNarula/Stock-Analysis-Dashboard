# 📈 Stock Analysis Dashboard

It is a stock market analysis dashboard that provides **real-time stock data, price charts, technical indicators, and latest news** for both **Indian** and **US stocks**. This application utilizes **Yahoo Finance**, **DuckDuckGo Search**, and **Groq AI** to fetch stock prices, news articles, and provide AI-powered stock insights.

## 🚀 Features

- 📊 **Stock Price Charts**: Candlestick charts for stock price movements.
- 🔎 **Stock Search**: Supports both **Indian (NSE/BSE)** and **US (NASDAQ/NYSE)** stocks.
- 📰 **Latest News**: Fetches real-time news about selected stocks.
- 📈 **Technical Indicators**: RSI, Moving Averages (50-day & 200-day).
- 💰 **Key Statistics**: Latest price, 52-week range, trading volume, and more.
- 🤖 **AI Chatbot**: Ask stock-related questions powered by **Groq AI**.
- ⚡ **Fast & Interactive UI**: Built with **Streamlit** and **Plotly**.

## 📌 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (Interactive UI)
- **Data**: [Yahoo Finance (yfinance)](https://pypi.org/project/yfinance/) (Stock Market Data)
- **News Fetching**: [DuckDuckGo Search (DDGS)](https://pypi.org/project/duckduckgo-search/)
- **AI Chatbot**: [Groq AI](https://groq.com/)
- **Visualization**: [Plotly](https://plotly.com/) (Stock Charts)
- **Environment Management**: [python-dotenv](https://pypi.org/project/python-dotenv/)

## 📥 Installation & Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/stock-analysis-dashboard.git
   cd stock-analysis-dashboard
   ```

2. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up API keys**  
   Create a `.env` file in the project root and add your **Groq API key**:
   ```sh
   GROQ_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```sh
   streamlit run app.py
   ```

## 🎯 Usage

1. **Select a stock market** (Indian or US Stocks).
2. **Choose a stock** from the dropdown or enter a custom symbol.
3. **View stock charts** (Candlestick and Volume).
4. **Check key statistics** (Latest Price, Moving Averages, RSI, etc.).
5. **Read the latest news** about the selected stock.
6. **Chat with AI** to get stock insights.


## 📜 License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).

## 🌟 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)
- [Plotly](https://plotly.com/)
- [DuckDuckGo Search API](https://pypi.org/project/duckduckgo-search/)
- [Groq AI](https://groq.com/)

---

🔗 **Follow me on GitHub**: [ShivaanjayNarula](https://github.com/ShivaanjayNarula)  
📧 **Contact**: shivaanjaynarula@gmail.com
