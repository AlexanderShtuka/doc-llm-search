import streamlit as st
from main import qa_chain, ask_with_tavily

st.set_page_config(page_title="Perplexity Clone", layout="wide")
st.title("Perplexity-style AI Search")

query = st.text_input("Ask me anything:")

if query:
    st.write("Searching documents...")
    response = qa_chain(query)

    if response["result"]:
        st.subheader("Answer")
        st.write(response["result"])

        st.subheader("Sources")
        seen = set()
        for doc in response["source_documents"]:
            src = doc.metadata.get("source", "Unknown")
            if src not in seen:
                st.markdown(f"- {src}")
                seen.add(src)

    if not response["result"] or len(response["source_documents"]) == 0:
        st.write("Not enough info in local docs. Searching the web...")
        web_answer = ask_with_tavily(query)
        st.subheader("Web Answer")
        st.write(web_answer)
