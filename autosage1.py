import google.generativeai as genai
import streamlit as st
import os

# --- Setup ---
# API Key - Replace with your Gemini API key or set as an environment variable
GOOGLE_API_KEY = os.environ.get("AIzaSyDvoNgCyhTkLn0Pnx-Vmx9fdqtJkObLJpI") 

genai.configure(api_key=GOOGLE_API_KEY)

# Choose the Gemini Flash model
MODEL_NAME = 'gemini-1.5-flash-001'  # Or another available Gemini model

# --- Function to Generate Content ---
def generate_text(prompt, model=MODEL_NAME, max_output_tokens=2048, temperature=0.7):
    """Generates text using the Gemini model.

    Args:
        prompt: The text prompt to send to the model.
        model: The name of the Gemini model to use.
        max_output_tokens:  Maximum number of tokens in the generated output.
        temperature: Controls the randomness of the output (0.0 - 1.0).

    Returns:
        The generated text. Returns an error message if there's an issue.
    """
    try:
        model = genai.GenerativeModel(model)  #Explicitly create model instance
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- Streamlit UI ---
st.title("AutoSage with Gemini Flash")
st.subheader("A Text Generation App powered by Google's Gemini Models")

# User input
prompt_text = st.text_area("Enter your prompt:", height=200)

# Model parameters (sliders/inputs)
temperature = st.slider("Temperature (randomness):", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
max_tokens = st.slider("Max Output Tokens:", min_value=50, max_value=4096, value=1024, step=50)


# Generate button
if st.button("Generate Text"):
    if prompt_text:
        with st.spinner("Generating..."):
            generated_text = generate_text(prompt_text, temperature=temperature, max_output_tokens=max_tokens)
        st.subheader("Generated Output:")
        st.write(generated_text)
    else:
        st.warning("Please enter a prompt.")

# --- Example Prompts (optional) ---
st.sidebar.header("Example Prompts:")
example_prompts = [
    "Write a short story about a robot who falls in love with a human.",
    "Summarize the key points of quantum physics.",
    "Generate a Python function that calculates the factorial of a number.",
    "Compose a haiku about a sunset.",
    "Explain the concept of blockchain in simple terms."
]

selected_prompt = st.sidebar.selectbox("Select an example:", example_prompts)

if st.sidebar.button("Use Example Prompt"):
    st.session_state['example_prompt'] = selected_prompt  # Use session_state
    st.session_state['prompt_text'] = selected_prompt     # to persist prompt.

if 'prompt_text' in st.session_state:  #Load back in
    prompt_text = st.session_state['prompt_text']
    st.text_area("Enter your prompt:", value=prompt_text, height=200)


# --- Info and Usage Tips ---
st.sidebar.header("Usage Tips")
st.sidebar.markdown("""
*   **Prompt Engineering:**  The quality of the output depends heavily on the prompt. Be clear and specific.
*   **Temperature:**  A higher temperature (closer to 1.0) results in more random and creative outputs. Lower temperatures (closer to 0.0) lead to more predictable and focused responses.
*   **Max Tokens:** Controls the length of the generated text.s
*   **API Key:** Make sure you have a valid Google Gemini API key. You can get one from the Google AI Studio.
*   **Error Handling:**  If you get an error, check your API key and prompt.  Sometimes the model might have temporary issues.
""")

st.sidebar.header("About")
st.sidebar.markdown("""
This app uses Google's Gemini models via the `google.generativeai` library and Streamlit for the user interface.  It's a simple example of how to interact with the Gemini API.
""")

# --- End of Script ---