import streamlit as st
import json
from fuzzywuzzy import process

# Load equations from JSON file
with open('equations.json') as f:
    equations = json.load(f)

# Search box
query = st.text_input("Search for an equation:")

if query:
    # Create search strings from name and tags
    search_strings = [eq['name'] + " " + " ".join(eq['tags']) for eq in equations]
    
    # Perform fuzzy search and get top 3 matches
    matches = process.extract(query, search_strings, limit=3)
    
    # Extract names of the top 3 matches
    match_names = [equations[search_strings.index(match[0])]['name'] for match in matches]
    
    # Let the user select one from the dropdown
    selected_name = st.selectbox("Closest matches:", match_names)
    
    # Find the selected equation
    selected_eq = next(eq for eq in equations if eq['name'] == selected_name)
    
    # Display the selected equation details
    st.subheader(selected_eq['name'])
    st.markdown(selected_eq['description'])
    st.markdown(f"$$ {selected_eq['latex_equation']} $$")
    
    # Render nomenclature
    st.write("where,")
    for var, desc in selected_eq['nomenclature']:
        st.markdown(f"$$ {var} $$, {desc}")
    
    # Show equation in code blocks for easy copy-paste
    st.write("##### LaTeX code:")
    st.code(selected_eq['latex_equation'])
    st.write("##### Python code:")
    st.code(selected_eq['code_equation'], language="python")

else:
    st.write("Enter a search query to find an equation.")
    if st.button("Show all equations"):
        for eq in equations:
            st.markdown(f"#### {eq['name']}")
            st.markdown(f"$$ {eq['latex_equation']} $$")