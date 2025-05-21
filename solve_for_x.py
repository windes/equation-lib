import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

# Set up Streamlit app
st.markdown("### Solve for X")

# Instructions
st.markdown("""
- Enter an algebraic equation (e.g., 'u_nu = ((8 pi h nu^3)/(c^3))(1/(exp((h nu)/(k_B T))-1))') using Latin or Greek letters (e.g., x, y, Re, rho, mu) and constants (e.g., 2, pi, e).
- Use '=' for equality (e.g., 'x = exp(y) + z'); use either \* or a single space for multiplication; use either ^ or \*\* for exponentiation
- Supports normal math functions such as exp(x) sin(x), cos(x), log(x), sqrt(x).
""")

equation_input = st.text_input("Equation string:", "")

# Initialize variables
variables = []
solution_latex = None
selected_var = None

if equation_input:
    try:
        # Preprocess: replace '^' with '**' for powers
        equations_input = equation_input.replace('^', '**')

        # Identify potential multi-letter variables using regex
        # Match alphabetic sequences (e.g., Re, rho, mu) but exclude known constants and functions
        potential_vars = set(re.findall(r'\b[a-zA-Z]+\b', equations_input))
        known_constants = {'pi', 'e'}
        known_functions = {'exp', 'sin', 'cos', 'tan', 'log', 'sqrt'}  # Common SymPy functions
        var_names = [v for v in potential_vars if v not in known_constants and v not in known_functions]

        # Create SymPy symbols for each variable and functions
        local_dict = {var: sp.Symbol(var) for var in var_names}
        # Add SymPy functions to local_dict (only if not used as variables)
        for func in known_functions:
            if func not in var_names:
                local_dict[func] = getattr(sp, func, None)
                if local_dict[func] is None:
                    del local_dict[func]  # Remove if function doesn't exist in SymPy

        # Split the equation at '=' and form the expression to solve (move all terms to one side)
        if '=' in equations_input:
            left, right = equations_input.split('=')
            equation_to_parse = f"({left}) - ({right})"
        else:
            equation_to_parse = equations_input

        # Parse the equation with SymPy
        transformations = (standard_transformations + (implicit_multiplication_application,))
        eq = parse_expr(equation_to_parse, transformations=transformations, local_dict=local_dict)

        # Identify variables (symbols excluding constants like pi)
        variables = sorted([str(var) for var in eq.free_symbols if not var.is_constant()])

        # Dropdown for selecting a variable
        if variables:
            selected_var = st.selectbox("Select a variable to solve for:", variables)
            
            # Solve the equation for the selected variable
            if selected_var:
                var_symbol = local_dict.get(selected_var, sp.Symbol(selected_var))
                solutions = sp.solve(eq, var_symbol)
                
                if solutions:
                    # Convert solution to LaTeX
                    solution = solutions[0]  # Take first solution
                    solution_latex = sp.latex(sp.Eq(var_symbol, solution))
                    st.markdown(f"**Solution for {selected_var}:**")
                    st.latex(solution_latex)
                    
                    # Generate the solved equation (e.g., x = exp(y) + z)
                    solved_expr = sp.Eq(var_symbol, solution)
                    original_eq_latex = sp.latex(solved_expr)
                    python_syntax = str(solved_expr.rhs)
                    python_syntax = python_syntax.replace('**', '^')  # Use ^ for display
                    cpp_syntax = str(solved_expr.rhs)
                    cpp_syntax = cpp_syntax.replace('**', '^').replace('*', ' * ').replace('+', ' + ').replace('-', ' - ')
                    excel_syntax = str(solved_expr.rhs)
                    excel_syntax = excel_syntax.replace('**', '^').replace('*', '*').replace('/', '/')
                    
                    # Display equation in different formats
                    st.markdown("#### Formatted for code")
                    
                    st.markdown("**LaTeX:**")
                    st.code(original_eq_latex, language='latex')
                    
                    st.markdown("**Right hand side (Python)**")
                    st.code(python_syntax, language='python')
                    
                    st.markdown("**Right hand side (C/C++)**")
                    # Convert to C++ style with pow() and spacing
                    cpp_display = cpp_syntax
                    for var in variables:
                        cpp_display = re.sub(rf'\b{var}\^(\d+)\b', rf'pow({var}, \1)', cpp_display)
                    cpp_display = cpp_display.replace('pi', 'M_PI')
                    st.code(cpp_display, language='cpp')
                    
                    st.markdown("**Right hand side (Excel)**")
                    # Keep variables as letters
                    excel_display = excel_syntax
                    st.code(excel_display, language='excel')
                else:
                    st.error("No solution found for the selected variable.")
        else:
            st.error("No variables found in the equation.")
    except Exception as e:
        st.error(f"Error parsing equation: {str(e)}")
