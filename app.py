import streamlit as st

# Override sqlite3 with pysqlite3 to fix sqlite version issues on Streamlit Cloud
import sys
import pysqlite3
sys.modules['sqlite3'] = pysqlite3

from crew.crew import run_pipeline

st.set_page_config(page_title="MarketBridge | Intelligent Market Matching", layout="wide")

st.title("🔍 MarketBridge — Insights That Connect")
st.markdown("Enter a company name to extract their offerings and find matching services from your company.")

company_name = st.text_input("🏢 Company Name", placeholder="e.g., Infosys, Salesforce, TCS")

if st.button("Run Analysis") and company_name.strip():
    with st.spinner("🔎 Running company analysis and matching..."):
        try:
            result = run_pipeline(company_name.strip())

            st.success("✅ Match report generated successfully!")

            st.subheader("📘 Company Introduction & Offerings")
            st.markdown(result["company_intro"])

            st.subheader("📊 Match Report: Services You Can Offer")
            st.markdown(result["matching_report"])

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
else:
    st.info("Please enter a valid company name to proceed.")
