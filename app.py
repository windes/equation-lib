import streamlit as st
import json
from fuzzywuzzy import process

# Load equations from JSON file
with open('equations.json') as f:
    equations = json.load(f)

# Search box
query = st.text_input("Search for an equation")

if query:
    # Create search strings from name and tags
    search_strings = [eq['name'] + " " + " ".join(eq['tags']) for eq in equations]
    
    # Perform fuzzy search and get top 3 matches
    matches = process.extract(query, search_strings, limit=3)
    
    for match in matches:
        matched_string, score = match
        index = search_strings.index(matched_string)
        eq = equations[index]
        
        # Display equation details
        st.subheader(eq['name'])
        st.markdown(f"$$ {eq['latex_equation']} $$")
        st.write("Nomenclature:")
        for var, desc in eq['nomenclature']:
            st.markdown(f"- \\( {var} \\): {desc}")
        st.markdown(eq['description'])
        
        # Escape single quotes for JavaScript clipboard functionality
        escaped_code = eq['code_equation'].replace("'", "\\'")
        copy_button = f"""
        <button onclick="navigator.clipboard.writeText('{escaped_code}')">
            Copy to clipboard
        </button>
        """
        st.markdown(copy_button, unsafe_allow_html=True)
else:
    st.write("Enter a search query.")