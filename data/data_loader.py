import yahooquery as yq
import pandas as pd
import logging

class DataLoader:
    """Loads stock data dynamically from Yahoo Finance"""

    def get_tickers(self, exchange="NSE", market_cap_limit=5000):
        """
        Fetch a list of stock tickers from Yahoo Finance for NSE India.
        Filters out small-cap companies based on market capitalization.
        """
        try:
            logging.info("🔄 Fetching stock tickers dynamically...")

            # ✅ Fetch tickers using Yahoo Finance's built-in indices
            indices = ["NIFTY50.NS", "NIFTY100.NS"]
            index_tickers = set()

            for index in indices:
                ticker_obj = yq.Ticker(index)
                tickers = ticker_obj.get("quotes", [])
                index_tickers.update([item["symbol"] for item in tickers])

            if not index_tickers:
                logging.warning("❌ No tickers retrieved from Yahoo Finance. Using fallback tickers.")
                return self.get_fallback_tickers()

            # ✅ Fetch market cap details for filtering
            stock_data = yq.Ticker(list(index_tickers))
            fundamentals = stock_data.summary_detail

            filtered_tickers = []
            for ticker in index_tickers:
                market_cap = fundamentals.get(ticker, {}).get("marketCap", 0) / 1e7  # Convert to crores
                if market_cap >= market_cap_limit:
                    filtered_tickers.append(ticker)

            if not filtered_tickers:
                logging.warning("⚠️ No valid tickers found based on market cap filter. Using fallback.")
                return self.get_fallback_tickers()

            logging.info(f"✅ Retrieved {len(filtered_tickers)} valid tickers")
            return filtered_tickers[:50]

        except Exception as e:
            logging.error(f"❌ Failed to fetch tickers: {e}")
            return self.get_fallback_tickers()

    def get_fallback_tickers(self):
        """Returns pre-selected fallback tickers from major sectors."""
        logging.info("🔄 Using fallback tickers from major sectors.")
        return [
            "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBIN.NS",
            "HINDUNILVR.NS", "TITAN.NS", "MARUTI.NS", "SUNPHARMA.NS", "ITC.NS"
        ]

    def get_fundamentals(self, ticker):
        """Fetch financial data dynamically for a given ticker"""
        try:
            stock = yq.Ticker(ticker)
            summary = stock.summary_detail.get(ticker, {})
            key_stats = stock.key_stats.get(ticker, {})

            if not summary:
                logging.warning(f"❌ No summary data found for {ticker}. Skipping.")
                return pd.DataFrame([])

            # ✅ Extracting Additional Relevant Financial Data
            data = {
                "Company Name": stock.quote_type.get(ticker, {}).get("longName", ticker),
                "Revenue Growth": key_stats.get("revenueGrowth", 0),
                "Earnings Growth": key_stats.get("earningsGrowth", 0),
                "ROIC": key_stats.get("returnOnEquity", 0),
                "Market Cap (Cr)": summary.get("marketCap", 0) / 1e7,
                "Debt-to-Equity": key_stats.get("debtToEquity", 0),
                "P/E Ratio": summary.get("trailingPE", 0),
                "Dividend Yield": summary.get("dividendYield", 0) * 100 if summary.get("dividendYield") else 0,
                "Price-to-Sales (P/S)": key_stats.get("priceToSalesTrailing12Months", 0),
                "Operating Margin (%)": key_stats.get("operatingMargins", 0) * 100 if key_stats.get("operatingMargins") else 0,
                "Book Value per Share (BVPS)": key_stats.get("bookValue", 0),
                "Free Cash Flow Yield": key_stats.get("freeCashflow", 0) / key_stats.get("marketCap", 1) * 100,
                "Beta (Volatility)": key_stats.get("beta", 1.0),
                "Sector": stock.asset_profile.get(ticker, {}).get("sector", "Unknown")
            }

            return pd.DataFrame([data])

        except Exception as e:
            logging.error(f"❌ Failed to fetch fundamentals for {ticker}: {e}")
            return pd.DataFrame([])