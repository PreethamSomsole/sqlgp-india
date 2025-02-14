import os
import sys
import logging
import warnings
import pandas as pd
from datetime import datetime

# Get the project root dynamically
project_root = os.path.abspath(os.getcwd())

# Ensure the script can find modules
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "data"))
sys.path.append(os.path.join(project_root, "analysis"))
sys.path.append(os.path.join(project_root, "visualization"))
sys.path.append(os.path.join(project_root, "models"))

# Debugging paths
print("🔍 sys.path:", sys.path)

try:
    from data.data_loader import DataLoader
    from analysis.fundamental import FundamentalAnalyzer
    from analysis.analysis_engine import generate_recommendations
    from models.predictive_model import compute_predictive_growth
    print("✅ Successfully imported all required modules!")
except ModuleNotFoundError as e:
    logging.error(f"❌ ImportError: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    """Main analysis workflow"""
    try:
        logging.info("🔄 Initializing DataLoader and FundamentalAnalyzer...")
        data_loader = DataLoader()
        analyzer = FundamentalAnalyzer()
    except Exception as e:
        logging.error(f"🔥 Critical error during initialization: {str(e)}")
        sys.exit(1)

    try:
        tickers = data_loader.get_tickers()
        if not tickers:
            logging.error("❌ No valid tickers retrieved!")
            sys.exit(1)

        results = []
        for ticker in tickers:
            try:
                logging.info(f"📈 Processing {ticker}...")
                fundamentals = data_loader.get_fundamentals(ticker)

                if fundamentals.empty:
                    logging.warning(f"⚠️ Skipping {ticker} due to missing fundamentals")
                    continue

                analysis = analyzer.analyze_company(ticker, fundamentals)
                analysis["PGS"] = compute_predictive_growth(analysis)

                if analysis:
                    results.append(analysis)
                    logging.info(f"✅ Successfully analyzed {ticker}")
                else:
                    logging.warning(f"⚠️ Incomplete or empty analysis for {ticker}")
            except Exception as e:
                logging.error(f"❌ Failed to process {ticker}: {str(e)}")

        if results:
            df = pd.DataFrame(results)
            df = generate_recommendations(df)
            df.to_csv(os.path.join(project_root, "sqglp_results.csv"), index=False)
            logging.info("✅ Analysis saved successfully")
            print("✅ Analysis completed! Check sqglp_results.csv")
        else:
            logging.error("❌ No valid data found for any tickers")
            print("❌ Analysis failed! Check logs for details")
    except Exception as e:
        logging.error(f"🔥 Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()