# Equation Search

This Streamlit app provides a way to search and view a library of mathematical and engineering equations stored in a json file.

## How to Run

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```
2. **Launch the app**:
   ```
   streamlit run app.py
   ```

## Adding New Equations

Modify `equations.json` to include additional equations with these fields:
- `name`: Equation name.
- `tags`: List of relevant tags.
- `nomenclature`: List of `[variable, description]` pairs, with variables in LaTeX.
- `description`: Equation description, supporting LaTeX.
- `latex_equation`: LaTeX-formatted equation.
- `code_equation`: Python string representation.

Ensure proper JSON formatting.

## Usage

- Enter a query (e.g., "circle", "triangle", "regression") in the search box.
- Top match equation will display, and the next two closest will be listed in a dropdown menu.