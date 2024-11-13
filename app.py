import streamlit as st
st.set_page_config(page_title="MeDeSense App", 
                   page_icon="logos/app-icon.png", 
                   layout="wide",
                   initial_sidebar_state="collapsed")
import os
import requests
from PyPDF2 import PdfReader
from PIL import Image
import base64
from io import BytesIO
import requests
import asyncio
from pages.recommendations_page import display_recommendations
from pages.description_page import display_description 
from Bio_Device_Classifier.constants import IMAGES_DIR
from Bio_Device_Classifier.logging import logger


merai_logo = "logos/Merai_logo_white 2.png"
stream_vision_logo = "logos/StreamVision-removebg-preview.png"
app_logo = "logos/app_logo.png"

# Inject custom CSS directly
st.markdown("""
    <style>
    .st-emotion-cache-1jicfl2 {
        padding: 0 2rem !important;
        /* Or specify any padding you prefer, e.g., padding: 2rem 0; */
    }
    </style>
    """, unsafe_allow_html=True)

def call_api(data):
    url = 'http://10.11.6.51:4001/predict'  # Your local API URL
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API call failed with status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error calling the API: {e}")
        return None

def image_to_base64(image):
    """
    Convert a PIL Image to a base64 encoded string.
 
    Args:
        image (PIL.Image.Image): The image to convert.
 
    Returns:
        str: Base64 encoded string of the image.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def load_image(image_path):
    """
    Load an image from a file path and encode it in base64.
 
    Args:
        image_path (str): The file path of the image.
 
    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    
# Helper function to encode an image in base64
def get_base64_image(image_path):
    image = Image.open(image_path)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Helper function to display images in columns with specified width
def display_logo(image_path, width, alignment="center"):
    base64_image = get_base64_image(image_path)
    st.markdown(
        f"""
        <div style='display: flex; justify-content: {alignment};'>
            <img src="data:image/png;base64,{base64_image}" width="{width}px">
        </div>
        """, 
        unsafe_allow_html=True
    )
 
# Header with logos in separate columns
# Adjust column layout
# Layout with defined column widths for images
col1, _, col3, _, col6 = st.columns([1, 1, 1, 1, 1])
# Apply CSS to add a top margin to the entire page body
# Display logos with the adjusted column layout

# Display images in specified columns
with col1:
    display_logo(merai_logo, width=250, alignment="flex-start")

with col3:
    display_logo(app_logo, width=250)

with col6:
    display_logo(stream_vision_logo, width=220, alignment="flex-end")

# Add a styled horizontal line with margin adjustments
st.markdown(
    "<hr style='border: 1px solid #ffffff; margin-top: -1px; margin-bottom: 2px;'>",
    unsafe_allow_html=True
)

 
# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'


def navigate_to_page(page_name):
     
     """
    Navigate to a different page by updating the session state.
 
    Args:
        page_name (str): The name of the page to navigate to.
    """
     st.session_state.page = page_name
     st.rerun()
    
# Set background color, text color, and title alignment using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom,
            #012D59,  /* Dark blue color at the top */
            #012243,  /* Dark blue color at the top */
            #000000   /* Black color at the bottom */
        );
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white !important;
    }
        background-image: load_image("logos/MDC.webp");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .rounded-image {
        border-radius: 20px;  /* Adjust the radius as needed */
        width: 100%;  /* Make sure the image scales to the desired width */
        object-fit: cover;  /* Ensure the image fits within the rounded corners */
    }
    .centered-title {
        text-align: center;
        color: white;
        font-size: 58px;  /* Increased font size for title */
        font-weight: bold;
    }
    .instructions-container {
            width:50vw;
            padding: 20px;
            color:#fffff;
            border: 2px solid #23746f; /* Border color */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0 2px 3px #6db1ff; /* Shadow effect */
            text-align: center;
        }
    /* Main button styling */
    .stButton > button  {                      
        margin-top: 20px !important;
        background: linear-gradient(45deg, #000000, #333333) !important;;
        color: white !important;
        box-shadow: 0px 2px 8px rgba(37, 177, 206, 0.6) !important;
        padding: 10px 20px;
        font-weight: 800;
        font-size: 2rem;
        border: none;
        transition: all 0.3s ease;
        cursor: pointer;
        }

    /* Hover effect */
    .stButton > button:hover {
        background: linear-gradient(45deg, #25b1ce, #1a8ca1) !important; /* Gradient for hover state */
        box-shadow: 0px 2px 16px rgba(37, 177, 206, 0.8) !important; /* Larger shadow on hover */
        transform: translateY(-2px); /* Slight lift effect */
    }

    .instructions-container h2 {
        margin-top: 0;
        color: #fffff;
        }
        .instructions-container ul{
            padding: 0;
            color:#fffff;
        }

    .file-upload-area {
        border: 2px dashed #555;
        padding: 20px;
        text-align: center;
        color:#00000;
        margin: 20px auto;
        max-width: 600px;
        border-radius: 10px;
    }
    .styled-image
    {
      border-radius: 20px;  /* Adjust the radius as needed */
        width: 92%;  /* Make sure the image scales to the desired width */
        object-fit: cover;  /* Ensure the image fits within the rounded corners */
        margin-bottom:30px;
        # height:500px;
    }
    
    /* Ensure all input labels, radio button text, and file upload label are white */
    label, .stRadio > label, .stRadio div {
        color: white !important;
    }
    
    .blue { color: #185875; }
    .yellow { color: #FFF842; }
    .container th
    {
      background-color:00008B;
    }
    .container th h1 {
        font-weight: bold;
        font-size: 1.8em;
    text-align: center;
    color: #ffffff;
    }
    
    .container td {
        font-weight: normal;
        font-size: 1.3em;
        text-align: center;
    -webkit-box-shadow: 0 2px 2px -2px #0E1119;
        -moz-box-shadow: 0 2px 2px -2px #0E1119;
                box-shadow: 0 2px 2px -2px #0E1119;
    }
 
    .container {
        text-align: left;
        overflow: hidden;
        width: 95vw;
        border: 2px solid #25b1ce;
        border-radius: 10px;
        background-color: #F5F5F5;
        
    display: table;
    padding: 0 0 8em 0;
 
    
    }
 
    .container td, .container th {
        padding-bottom: 2%;
        padding-top: 2%;
    padding-left:2%;  
        border: 2px solid #F5F5F5;
    }
 
    /* Background-color of the odd rows */
    .container tr:nth-child(odd) {
        background-color: #213C50;
    }
 
    /* Background-color of the even rows */
    .container tr:nth-child(even) {
        background-color: #223446;
    }
 
    .container th {
        background-color: #1F2739;
    }
 
    .container td:first-child {
      width:20%;  }
   
    .container td:last-child { 
    backround-color:white;
    overflow-y:hidden;
     width:55%; }
 
    .container tr:hover {   
     /* Table Hoverin color*/
    background-color: rgb(137,196,244); 
    color:#000000 !important;
    -webkit-box-shadow: 0 6px 6px -6px #0E1119;
        -moz-box-shadow: 0 6px 6px -6px #0E1119;
                box-shadow: 0 6px 6px -6px #0E1119;
    }
 
    @media (max-width: 800px) {
    .container td:nth-child(4),
    .container th:nth-child(4) { display: none; }
    }
    
 .prediction-card {
  
    color: #FFFFFF;  /* White text for readability */
    border: 2px solid #2196F3;  /* Bright blue border for emphasis */
    border-radius: 10px;  /* Rounded corners */
    padding: 20px;
    width: 95.9%;  /* Card width */
    text-align: center;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4), 0 0 10px rgba(33, 150, 243, 0.2);  /* Multi-layered shadow for depth */
    margin: 20px auto;  /* Center alignment */
    
    /* Adding gradient shadow */
    background: linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(0, 82, 155, 0.4));  /* Gradient shadow effect */
    
}

    .prediction-card h3 {
        font-size: 24px;
        color: #ffffff;
        margin-bottom: 10px;
    }
 
    .class-value {
        font-size: 36px;  /* Larger font for emphasis */
        font-weight: bold;
        color: #25b1ce;  /* Highlight color for the class */
        margin-bottom: 10px;
    }
 
    .prediction-card p {
        font-size: 20px;
        color: #f5f5f5;  /* Slightly muted text for the description */
    }
    .flip-card {
        width: 47vw;
        height: 300px;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        position: relative;
        border: 2px solid #4DC3FA; /* Example color */
        border-radius: 10px;
        background-color: #1F2739;
        margin-bottom:30px;
        margin-top:30px;
    }
 
    .flip-container:hover .flip-card {
        transform: rotateY(180deg);
    }
 
    /* Front and Back Card Styles */
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 10px;
    }
 
    .flip-card-front {
         background-color:#033666;
           
        
        color: black;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
 
    .flip-card-back {
         background-color:#033666;
        color: white;
        transform: rotateY(180deg);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size:24px;
        overflow-y:hidden;
        padding: 20px;
    }
        h2 {
        font-size:1em;
        font-weight: 300;
        text-align: center;
        display: block;
        line-height:1em;
        padding-bottom: 2em;
        color: #FB667A;
        }
        .wrapper
        {
        display:flex;
        flex-direction:row;
        width:95vw;
 
 
        margin-bottom:20px;
        gap:10px;
 
        
 
        }
        .subheader
        {
        color:white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#Header remover style
st.markdown('''
<style>
.stApp [data-testid="stToolbar"] {
    display: none;
}
 
header {
    visibility: hidden;
}
 
#MainMenu {
    visibility: hidden;
}
 
# footer {
#     visibility: hidden;
# }
 
/* Remove top padding of the content */
.css-hi6a2p {
    padding-top: 0rem;
}
 
/* Adjust margin and padding for the main content area to remove empty space */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
    margin-top: -2rem;  /* You can adjust this value if needed */
    margin-right: 1rem;
}
.custom-subheader {
        color: white; /* Custom color */
        font-size: 24px; /* Custom font size */
        font-weight: bold; /* Make it bold */
        text-align: left; /* Align text to left */
        margin-bottom: 3px; /* Add some space below */
    }
            
</style>
''', unsafe_allow_html=True)
 
def read_pdf(file):
    """Reads and extracts text from a PDF file."""
    pdf_reader = PdfReader(file)
    text = ''.join([page.extract_text() for page in pdf_reader.pages])
    return text
 
def get_content(input_option):
    """Gets content from the user input, either through file upload or manual input."""
    content = None
   
    
    if input_option == "Upload a file":
        # st.markdown('<p class="custom-subheader">Upload a Text or PDF file</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a Text or PDF file", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                content = read_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                content = uploaded_file.read().decode("utf-8")
            else:
                st.error("Unsupported file type")
    elif input_option == "Enter text manually":
    #    st.markdown('<p class="custom-subheader">Enter text manually</p>', unsafe_allow_html=True)
       content = st.text_area("Enter text manually")
    
    if content and input_option=="Upload a file":
        st.text_area("Input content", content, height=250)
    
    return content
  
def get_image_path(index):
    image_path = os.path.join(IMAGES_DIR, f"{index}.png")
    if os.path.exists(image_path):
        return image_path
    else:
        return None  # If the image doesn't exist
 
def check_image_path_exists(image_path):
    return os.path.exists(image_path)

def display_back_button():
    """
    Display a back button that navigates the user back to the home page.
    """
    if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False
            # CSS styles for different button states
    if st.button("Back", use_container_width=False):
        st.session_state.button_clicked = not st.session_state.button_clicked
        navigate_to_page('home')
        st.rerun()
       
def home_page():
        with st.container():
            
            st.markdown("""

            <h1 style="text-align: center; font-size: 3.5rem; margin-bottom: 1.5rem; color: white;">
                <span style="color: white;">Welcome to the </span>
                <span style="color: #5ac6d5;">Me</span><span style="color: white;">dical</span>
                <span style="color: #5ac6d5;">De</span><span style="color: white;">vice</span>
                <span style="color: #5ac6d5;">Sense</span>
                <span style="color: white;"> App</span>
            </h1> 
            """, unsafe_allow_html=True)

             # Set page layout to wide
        
        col1, col2 = st.columns([3, 2.2])
        with col1:
            main_img=load_image("logos/background.jpeg")
            # Center-aligned image in st.markdown
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <img src="data:image/jpeg;base64,{main_img}" class="styled-image" alt="Card Image"/>
                </div>
                """,
                unsafe_allow_html=True)
            
            st.markdown(f"""
                <p style="text-align: center; padding: 0 2rem; font-size: 1.75em; line-height: 2rem;">
                    This application allows you to classify medical devices using Advanced Deep Learning Techniques.</p>
                <p style="text-align: center; padding: 0 2rem; color: yellow; font-size: 1rem; line-height:25px;">
                    You can upload a PDF or text file, or enter text manually to receive predictions about medical device classifications.
                </p>""", unsafe_allow_html=True)
            if st.button("Know More"):
                navigate_to_page("description")
        st.session_state.setdefault('show_recommendations', False)
        content = None
        with col2:
            with st.container():
                n_col1, n_col2, n_col3 = st.columns(3)
          
            # Display an input field for the user's name
            st.markdown('<p class="custom-subheader">Enter Your Device Name</p>', unsafe_allow_html=True)
            device_name = st.text_input(" ")
            st.write("")
            st.markdown('<p class="custom-subheader">Enter Device Description</p>', unsafe_allow_html=True)
            st.write("")
  
            input_option = st.radio("Choose your input method", ("Upload a file", "Enter text manually"))
            content = get_content(input_option)
            st.session_state['content'] = content
            
            if st.button("Submit"):
                if content:
                    result = call_api({"text": content})
                    predicted_class = result.get("predicted_class")
                    # print(predicted_class)
                    if device_name:
                        st.session_state['device_name']=device_name
                    else:
                        st.error("Please enter device name.")
                    
 
                    st.session_state['predicted_class']=predicted_class
                    result = st.session_state['predicted_class']  # Placeholder result for testing
                    # predicted_class = result.get("predicted_class", "No class predicted")
                    # st.snow()
                    if predicted_class.split()[-1]=="A":
                        card_img=load_image("logos/A.png")
                    elif predicted_class.split()[-1]=="B":
                        card_img=load_image("logos/B.png")
                    elif predicted_class.split()[-1]=="C":
                        card_img=load_image("logos/C.png")
                    elif predicted_class.split()[-1]=="D":
                        card_img=load_image("logos/D.png")
                    if device_name:
                        st.markdown(f"""
                                <div class="prediction-card" style="width: 100%; height: 100%;overflow: auto; ">
                                    <div class="class-value">
                                        <img src="data:image/jpeg;base64,{card_img}" class="card-image" alt="Card Image"  style=" width:80px;"/>
                                        <span style="color:#efbf04;">Predicted Class:{predicted_class.split()[-1]}</span> 
                                    </div>
                                    <div style="color:#E0B0FF;font-size:36px;font-weight:bold;">
                                        {device_name}
                                </div>
                                    <p>{content}</p>
                                    """,unsafe_allow_html=True)
                   
                    st.session_state['show_recommendations'] = True       
                else:
                    st.session_state['show_recommendations'] = False
        
            if content:
            
                if st.session_state['show_recommendations']:
                    if st.button("Get Recommendation"):
                        st.session_state['show_recommendations'] = False
                    
                        navigate_to_page('recommendations')
                        st.rerun()

# Wrap the call in a function that creates the async task
def load_recommendations_page():
    # Schedule display_recommendations without blocking
    asyncio.run(display_recommendations())

# Main logic to display pages based on session statehere
if st.session_state.page == 'home':
    home_page()
    
elif st.session_state.page == 'recommendations':
    with st.spinner("Loading..."):
      
        load_recommendations_page()
 
elif st.session_state.page == 'description':
  
    display_description()
    
st.markdown("""
    <footer style='text-align: center; padding: 2rem 0;'>
        <p style='color: #888;'>v1.0 | © 2024 Stream Vision - Merai. All rights reserved. </p>
    </footer>
""", unsafe_allow_html=True)

