import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("User Story & Use Case Generator🤖")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Welcome to Lyzr's User Story and Use Case Generator! Revolutionize your project development process with our intuitive tool powered by Lyzr's SDK. Upload your document, and witness Lyzr's AI crafting tailored user stories and use cases in seconds, empowering your team with unmatched precision and efficiency.")

# Function to remove existing files
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# File upload widget
uploaded_file = st.file_uploader("Choose Word file", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded Word file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved")

def get_files_in_directory(directory="data"):
    # This function helps us get the file path along with the filename.
    files_list = []

    # Ensure the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if the path points to a file (not a directory)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

# Function to implement RAG Lyzr Chatbot
def rag_implementation():
    # Get the file path
    file_path = get_files_in_directory()[0]

    # Initialize the RAG Lyzr ChatBot
    rag = ChatBot.docx_chat(
        input_files=[file_path],
        llm_params={"model": "gpt-3.5-turbo"},
    )

    return rag



# Function to get Lyzr response
def resume_response():
    file_path = get_files_in_directory()[0]
    rag = rag_implementation()
    prompt = f"""To generate user stories and use cases for your project/product based on the uploaded document, please follow the instructions below:
                     - Product Vision and Goals: Identify and describe the overarching vision and goals of the product. What specific problem is the product aiming to solve?
                     - Target Audience and User Personas: Identify the primary users of the product and describe their demographics, behaviors, and needs to create user personas.
                     - Functional Requirements: Identify and specify the functionalities and features the product should have, highlighting both primary features and any additional capabilities required.
                     - Non-functional Requirements: Identify and specify non-functional requirements such as performance, scalability, security, and usability.
                     - User Flows and Workflows: Identify and illustrate typical user flows and workflows within the product.
                     - Acceptance Criteria: Identify and clarify the conditions that must be met for a user story to be considered complete and accepted by stakeholders.
                     - Constraints and Limitations: Identify any constraints or limitations that may impact feature development and implementation.
                     - Use Cases: Based on above information give multiple use cases that can used for by the user.
                     - User Stories: Based on the provided information, craft multiple user stories that represent specific user needs and actions within the product.
                     - Ensure that the information provided for Product Vision and Goals, Target Audience and User Personas, Functional Requirements, Non-Functional Requirements, User Flows and Workflows, Acceptance Criteria, and Constraints and Limitations is precise and comprehensive not more than 3 bullet points.
                     - The generated Use Cases and User Stories should be clearly explained individually with relevance to the product's context and objectives."""

    response = rag.chat(prompt)
    return response.response
if uploaded_file is not None:
    automatice_response = resume_response()
    st.markdown(f"""{automatice_response}""")


# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease.For any inquiries or issues, please contact Lyzr.

    """
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
    
