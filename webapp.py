import streamlit as st
import requests
import pandas as pd
import json
import os

API_URL = "http://127.0.0.1:8000/extract"
st.set_page_config(page_title="Marksheet Extractor", page_icon="📄")

st.title("📄 AI Marksheet Extractor")
st.markdown("Upload a marksheet (PDF/Image) to extract student details and marks.")

uploaded_file = st.file_uploader("Choose a file...", type=["pdf", "jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    if uploaded_file.type in ["image/jpeg", "image/png", "image/webp"]:
        st.image(uploaded_file, caption="Uploaded Marksheet", width='stretch')
    elif uploaded_file.type == "application/pdf":
        st.info("PDF Uploaded. (Preview not available for PDFs in this demo)")

    if st.button("🚀 Extract Data", type="primary"):
        with st.spinner("AI is analyzing the document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Extraction Complete!")
                    
                    json_string = json.dumps(data, indent=4)
                    
                    st.download_button(
                        label="📥 Download JSON",
                        data=json_string,
                        file_name="extracted_marksheet.json",
                        mime="application/json"
                    )

                    st.subheader("👤 Candidate Details")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input("Name", value=data['candidate'].get('name', 'N/A'), disabled=True)
                        st.text_input("Roll No", value=data['candidate'].get('roll_no', 'N/A'), disabled=True)
                    with col2:
                        st.text_input("Institute", value=data['candidate'].get('institute_name', 'N/A'), disabled=True)
                        confidence = data['candidate'].get('confidence', 0)
                        st.metric("Confidence Score", f"{confidence * 100:.1f}%")

                    st.subheader("📚 Subject Performance")
                    if data.get('subjects'):
                        df = pd.DataFrame(data['subjects'])
                        cols = ['subject_name', 'obtained_marks', 'max_marks', 'grade', 'confidence']
                        final_cols = [c for c in cols if c in df.columns]
                        st.dataframe(df[final_cols], width='stretch')
                    else:
                        st.warning("No subjects found.")

                    st.subheader("🏆 Overall Result")
                    r_col1, r_col2 = st.columns(2)
                    r_col1.info(f"Result: **{data.get('overall_result', 'N/A')}**")
                    r_col2.info(f"Issue Date: **{data.get('issue_date', 'N/A')}**")

                    with st.expander("View Raw JSON Response"):
                        st.json(data)

                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Is FastAPI running on port 8000?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")