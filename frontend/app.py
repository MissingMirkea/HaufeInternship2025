import streamlit as st
import requests
import time

st.set_page_config(page_title="Code Review AI", page_icon="💻", layout="centered")

st.markdown("""
<style>
textarea { height:250px!important; resize:none!important; font-family:monospace; font-size:14px; }
.output-box { border:1px solid #ddd; padding:15px; border-radius:8px; min-height:200px;
              font-family:monospace; background-color:#f9f9f9; overflow-y:auto; white-space:pre-wrap; }
</style>
""", unsafe_allow_html=True)

st.title("💻 Code Review AI")

# Input methods
col1, col2 = st.columns([2, 1])
with col1:
    code_text = st.text_area("Paste your code here",
                             placeholder="Paste your C++, Python, Java, JavaScript, Go, or Ruby code here...")
with col2:
    uploaded_file = st.file_uploader("or Upload a file", type=["py", "js", "java", "cpp", "go", "rb", "c", "h", "txt"])
    language = st.selectbox("Choose language",
                            ["Auto-detect", "C++", "Python", "JavaScript", "Java", "Go", "Ruby", "Other"])

if st.button("🚀 Review Code", type="primary"):
    if not code_text.strip() and uploaded_file is None:
        st.warning("Please provide code either by file upload or by pasting in the text area.")
    else:
        with st.spinner("🔍 Analyzing code and generating review..."):
            try:
                # Prepare request
                if uploaded_file:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    data = {"language": language if language != "Auto-detect" else ""}
                    response = requests.post("http://localhost:8000/review", files=files, data=data)
                else:
                    data = {"code_text": code_text, "language": language if language != "Auto-detect" else ""}
                    response = requests.post("http://localhost:8000/review", data=data)

                # Handle response
                if response.status_code == 200:
                    result = response.json()

                    if "error" in result:
                        st.error(f"❌ Error: {result['error']}")
                    else:
                        st.success("✅ Review completed!")

                        # Display metadata
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Language", result.get("language", "Unknown"))
                        with col2:
                            st.metric("Processing Time", f"{result.get('estimated_time', 0):.2f}s")
                        with col3:
                            status = "⚠️ Partial" if result.get("partial_review") else "✅ Complete"
                            st.metric("Review Status", status)

                        # Display review
                        st.subheader("📝 Code Review")
                        review_text = result.get("review", "No review generated.")
                        st.markdown(f"<div class='output-box'>{review_text}</div>", unsafe_allow_html=True)

                        # Display suggestions if available
                        refactor_suggestions = result.get("refactoring_suggestions", [])
                        if refactor_suggestions:
                            st.subheader("💡 Refactoring Suggestions")
                            for suggestion in refactor_suggestions:
                                st.write(f"- {suggestion}")

                else:
                    st.error(f"❌ Server error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to backend server. Make sure it's running on http://localhost:8000")
                st.info("To start the backend, run: `uvicorn main:app --reload` from the backend folder")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")