import logging

def calculate_sqglp_score(revenue_growth, roic, earnings_growth, market_cap, pe_ratio, debt_to_equity):
    """Computes SQGLP Score."""
    if market_cap <= 0:
        market_cap = 1

    revenue_growth = max(revenue_growth, 0.01)
    roic = max(roic, 0.01)
    earnings_growth = max(earnings_growth, 0.01)
    pe_ratio = max(pe_ratio, 5)
    debt_to_equity = max(debt_to_equity, 0.1)

    score = round(
        (revenue_growth * 100 + roic * 50 + earnings_growth * 100) / (market_cap * pe_ratio * debt_to_equity), 2
    )

    logging.info(f"📊 Computed SQGLP Score: {score}")
    return score

def generate_recommendations(df):
    """Generate stock recommendations."""
    df["Recommendation"] = "Hold"
    df.loc[df["SQGLP_Score"] >= 80, "Recommendation"] = "Strong Buy ⭐⭐⭐"
    df.loc[(df["SQGLP_Score"] >= 60) & (df["SQGLP_Score"] < 80), "Recommendation"] = "Buy ⭐⭐"
    df.loc[df["SQGLP_Score"] < 60, "Recommendation"] = "Sell ❌"
    return df