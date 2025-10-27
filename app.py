import streamlit as st

# Function to generate Fibonacci sequence
def fibonacci(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# Streamlit UI
st.title("Fibonacci Sequence Generator")

# Input from user
n_terms = st.number_input("Enter the number of terms you want in the Fibonacci sequence:", min_value=1, value=10, step=1)

# Generate the Fibonacci sequence
if st.button("Generate Sequence"):
    fib_sequence = fibonacci(n_terms)
    st.write(f"First {n_terms} terms of Fibonacci sequence:")
    st.write(fib_sequence)