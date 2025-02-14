import logging
import numpy as np
import pandas as pd

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FundamentalAnalyzer:
    """Analyzes fundamental financial metrics for stocks"""

    def analyze_company(self, ticker, fundamentals):
        """Perform SQGLP analysis on a given stock"""

        if fundamentals.empty:
            logging.warning(f"⚠️ No data available for {ticker}. Skipping analysis.")
            return None

        try:
            revenue_growth = fundamentals.get("Revenue Growth", [0])[0]
            earnings_growth = fundamentals.get("Earnings Growth", [0])[0]
            roic = fundamentals.get("ROIC", [0])[0]
            market_cap = fundamentals.get("Market Cap (Cr)", [0])[0]
            debt_to_equity = fundamentals.get("Debt-to-Equity", [0])[0]
            pe_ratio = fundamentals.get("P/E Ratio", [0])[0]
            dividend_yield = fundamentals.get("Dividend Yield", [0])[0]
            price_to_sales = fundamentals.get("Price-to-Sales (P/S)", [0])[0]
            operating_margin = fundamentals.get("Operating Margin (%)", [0])[0]
            free_cash_flow_yield = fundamentals.get("Free Cash Flow Yield", [0])[0]
            beta = fundamentals.get("Beta (Volatility)", [1.0])[0]
            sector = fundamentals.get("Sector", ["Unknown"])[0]
            company_name = fundamentals.get("Company Name", [ticker])[0]

            # ✅ Dynamic Calculation of SQGLP Score (Based on Weighted Factors)
            sqglp_score = round(
                (revenue_growth * 25) +
                (earnings_growth * 25) +
                (roic * 20) +
                (market_cap * 10) +
                (debt_to_equity * -5) +
                (pe_ratio * -5) +
                (dividend_yield * 5) +
                (price_to_sales * 5), 2
            )

            # ✅ Predictive Growth Score (PGS) Placeholder (Can be enhanced with ML)
            predictive_growth_score = round(np.mean([revenue_growth, earnings_growth, roic]) * 100, 2)

            # Final results dictionary
            analysis_result = {
                "Company Name": company_name,
                "Ticker": ticker,
                "SQGLP_Score": sqglp_score,
                "Revenue Growth": revenue_growth,
                "Earnings Growth": earnings_growth,
                "ROIC": roic,
                "Market Cap (Cr)": market_cap,
                "Debt-to-Equity": debt_to_equity,
                "P/E Ratio": pe_ratio,
                "Dividend Yield": dividend_yield,
                "Price-to-Sales (P/S)": price_to_sales,
                "Operating Margin (%)": operating_margin,
                "Free Cash Flow Yield": free_cash_flow_yield,
                "Beta (Volatility)": beta,
                "Sector": sector,
                "Predictive Growth Score (PGS)": predictive_growth_score
            }

            logging.info(f"✅ Analysis completed for {ticker}: SQGLP Score {sqglp_score}, PGS {predictive_growth_score}")
            return analysis_result

        except Exception as e:
            logging.error(f"❌ Error analyzing {ticker}: {e}")
            return None