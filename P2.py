import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh   # correct import
pip install yfinance
# Auto-refresh every 60 seconds
st_autorefresh(interval=60000, key="refresh")

# Define sectors/indices with tickers
NIFTY_IT = {
    "Tech Mahindra": "TECHM.NS",
    "Wipro": "WIPRO.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "TCS": "TCS.NS",
    "LTIMindtree": "LTIM.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Coforge": "COFORGE.NS",
    "Infosys": "INFY.NS",
    "Oracle Financial Services": "OFSS.NS",
    "Mphasis": "MPHASIS.NS"
}

NIFTY_AUTO = {
    "Uno Minda": "UNOMINDA.NS",
    "Ashok Leyland": "ASHOKLEY.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Tata Motors (PV)": "TMPV.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "TVS Motor": "TVSMOTOR.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Exide Industries": "EXIDEIND.NS",
    "Bharat Forge": "BHARATFORG.NS",
    "Motherson": "MOTHERSON.NS",
    "Sona Comstar": "SONACOMS.NS",
    "Bosch": "BOSCHLTD.NS",
    "Tube Investments": "TIINDIA.NS"
}

NIFTY_PSU_BANK = {
    "Bank of India": "BANKINDIA.NS",
    "State Bank of India": "SBIN.NS",
    "Canara Bank": "CANBK.NS",
    "Union Bank of India": "UNIONBANK.NS",
    "Punjab National Bank": "PNB.NS",
    "Indian Bank": "INDIANB.NS",
    "Bank of Baroda": "BANKBARODA.NS"
}

NIFTY_PHARMA = {
    "Divis Labs": "DIVISLAB.NS",
    "Lupin": "LUPIN.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Glenmark": "GLENMARK.NS",
    "Cipla": "CIPLA.NS",
    "Dr Reddy's": "DRREDDY.NS",
    "Alkem Labs": "ALKEM.NS",
    "Zydus Lifesciences": "ZYDUSLIFE.NS",
    "Mankind Pharma": "MANKIND.NS",
    "Biocon": "BIOCON.NS",
    "Torrent Pharma": "TORNTPHARM.NS",
    "Laurus Labs": "LAURUSLABS.NS",
    "Piramal Pharma": "PPLPHARMA.NS",
    "Aurobindo Pharma": "AUROPHARMA.NS"
}

# Helper function
def get_stock_percentage(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get("regularMarketPrice")
        previous_close = info.get("previousClose")
        if current_price and previous_close:
            return ((current_price - previous_close) / previous_close) * 100
    except Exception:
        return None

def sector_performance(sector_dict):
    changes = [get_stock_percentage(ticker) for ticker in sector_dict.values() if get_stock_percentage(ticker) is not None]
    if changes:
        return sum(changes) / len(changes)
    return None

# Streamlit UI
st.title("📊 NIFTY Sector Performance (Auto-refresh every 60s)")

sectors = {
    "NIFTY IT": NIFTY_IT,
    "NIFTY AUTO": NIFTY_AUTO,
    "NIFTY PSU BANK": NIFTY_PSU_BANK,
    "NIFTY PHARMA": NIFTY_PHARMA
}

summary = {sector: sector_performance(tickers) for sector, tickers in sectors.items()}

# Show only sector averages
st.subheader("📌 Sector Summary")
st.table({sector: f"{avg:.2f}%" if avg is not None else "No data" for sector, avg in summary.items()})