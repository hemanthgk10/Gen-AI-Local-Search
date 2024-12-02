import streamlit as st
from app.search import LocalSearch
from app.generate import GenerativeAI

# Initialize tools
search_tool = LocalSearch()
gen_ai = GenerativeAI()

# Build the index for the first time (remove this after setup)
search_tool.build_index("resources/")

st.title("Local Search with Generative AI")
query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        # Perform search
        results = search_tool.search(query)
        # st.write("Search Results:")
        # for i, result in enumerate(results):
        #     st.markdown(f"{i + 1}. {result}")

        # Generate AI response with context from search results
        st.write("\n**Generating AI insights...**")
        ai_response = gen_ai.generate_response(query, results)
        st.write(f"**AI Response:** {ai_response}")
    else:
        st.warning("Please enter a query.")
