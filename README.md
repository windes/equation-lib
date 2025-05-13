# Equation Search App

This Streamlit app enables fuzzy searching of mathematical and engineering equations.

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
- `code_equation`: Code-friendly string representation.

Ensure proper JSON formatting.

## Usage

- Enter a query (e.g., "circle", "triangle", "regression") in the search box.
- View the top three matching equations, including their LaTeX equations, nomenclature, and descriptions.
- Click "Copy to clipboard" to copy the code-friendly version for use in an IDE.

## Deployment

For Streamlit Cloud, upload `app.py`, `requirements.txt`, and `equations.json` to your repository.