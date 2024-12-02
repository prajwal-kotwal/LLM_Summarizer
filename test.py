import streamlit as st
import google.generativeai as genai
import google_api_key as GG
import PyPDF2

# Set up the Google Gemini API
genai.configure(api_key=GG.Google_api_key)

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(
        max_output_tokens=20000,
        temperature=0.9,
    ))

# Define the summarization prompt template
PROMPT_TEMPLATE = """
Summarize the following text in a clear, concise, and informative manner. Be sure to generate the summary in the language in which the input is provided.
{text}
"""

def summarize_text(input_text):
    # Format the prompt
    prompt = PROMPT_TEMPLATE.format(text=input_text)
    # Generate summary using the Gemini model
    response = model.generate_content(prompt)
    return response.text

# Function to read text from a PDF file (adjusted for BytesIO)
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.title("Text Summarizer")
st.write("Upload a PDF file or manually input text to summarize its content.")

# Option to input text manually or upload a PDF
input_method = st.radio("Choose input method", ("Upload PDF", "Input Text"))

# Handling "Upload PDF"
if input_method == "Upload PDF":
    # PDF File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Read PDF text
        input_text = read_pdf(uploaded_file)

        if input_text:
            # Generate and display the summary
            if st.button("Generate Summary"):
                summary = summarize_text(input_text)
                st.subheader("Summary")
                st.write(summary)

                # Save the summary to a text file with UTF-8 encoding
                with open('summary.txt', 'w', encoding='utf-8') as file:
                    file.write(summary)
                # Read the file with UTF-8 encoding and allow downloading
                with open('summary.txt', 'r', encoding='utf-8') as file:
                    st.download_button("Download Summary", data=file.read(), file_name='summary.txt')
        else:
            st.warning("Unable to extract text from the PDF.")

# Handling "Input Text"
elif input_method == "Input Text":
    # Text input section
    input_text = st.text_area("Enter text to summarize", height=300)

    if input_text:
        # Generate and display the summary
        if st.button("Generate Summary"):
            summary = summarize_text(input_text)
            st.subheader("Summary")
            st.write(summary)

            # Save the summary to a text file with UTF-8 encoding
            with open('summary.txt', 'w', encoding='utf-8') as file:
                file.write(summary)
            # Read the file with UTF-8 encoding and allow downloading
            with open('summary.txt', 'r', encoding='utf-8') as file:
                st.download_button("Download Summary", data=file.read(), file_name='summary.txt')
