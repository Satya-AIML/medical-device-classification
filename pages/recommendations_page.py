import streamlit as st
import os
import json
from PIL import Image
import base64
from io import BytesIO
from Bio_Device_Classifier.pipeline.predict_details import generate_response
from Bio_Device_Classifier.pipeline.recomendation import query_similar_embeddings
from Bio_Device_Classifier.constants import SPECIFIED_TAGS, IMAGES_DIR, GENERATED_RESPONSE
from Bio_Device_Classifier.logging import logger
 

# Function to display images for each index
def get_image_path(index):
    image_path = os.path.join(IMAGES_DIR, f"{index}.png")
    if os.path.exists(image_path):
        return image_path
    else:
        return None  # If the image doesn't exist

# Function to load descriptions from JSON
def load_descriptions():
    with open(GENERATED_RESPONSE, 'r') as file:
        descriptions = json.load(file)
    return descriptions
 
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
 
def load_image(image_path, size=(100, 100)):
    image = Image.open(image_path)
    image.thumbnail(size)  # Resize to the thumbnail
    return image_to_base64(image)
 
 
def navigate_to_page(page_name):
     
     """
    Navigate to a different page by updating the session state.
 
    Args:
        page_name (str): The name of the page to navigate to.
    """
     st.session_state.page = page_name
     st.rerun()
 
async def why_class(device_name,predicted_class,content):
    response_text = await generate_response(device_name, content, predicted_class)
    return response_text
    
# CSS styling
st.markdown("""
            <style>
                .stApp {
                    background-color: #012243;
                    color: white !important;
                }
                @charset "UTF-8";
            @import url(https://fonts.googleapis.com/css?family=Open+Sans:300,400,700);
            
            body {
            font-family: 'Open Sans', sans-serif;
            font-weight: 300;
            line-height: 1.42em;
            color: #02032f;;
            background-color:#1F2739;
                border: 2px solid #23746f; /* Border color */
                        border-radius: 10px; /* Rounded corners */
                        box-shadow: 0 2px 3px #6db1ff; /* Shadow effect */
            }
            
            h1 {
            font-size:3em;
            font-weight: 300;
            line-height:1em;
            text-align: center;
            color: #4DC3FA;
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
            
            h2 a {
            font-weight: 700;
            text-transform: uppercase;
            color: #FB667A;
            text-decoration: none;
            }
            
            .blue { color: #185875; }
            .yellow { color: #FFF842; }
            
            .container th h1 {
                font-weight: bold;
                font-size: 1em;
            text-align: left;
            color: #ffffff;
            }
            
            .container td {
                font-weight: normal;
                font-size: 1em;
            -webkit-box-shadow: 0 2px 2px -2px #0E1119;
                -moz-box-shadow: 0 2px 2px -2px #0E1119;
                        box-shadow: 0 2px 2px -2px #0E1119;
            }
            
            
            .container td, .container th {
                padding-bottom: 2%;
                padding-top: 2%;
            padding-left:2%;  
            }
            
            /* Background-color of the odd rows */
            .container tr:nth-child(odd) {
                background-color: #323C50;
            }
            
            /* Background-color of the even rows */
            .container tr:nth-child(even) {
                background-color: #2C3446;
            }
            
            .container th {
                background-color: #1F2739;
            }
            
            .container td:first-child { color: #FB667A; }
            
            .container tr:hover {
            background-color: #4f82c0;
            -webkit-box-shadow: 0 6px 6px -6px #0E1119;
                -moz-box-shadow: 0 6px 6px -6px #0E1119;
                        box-shadow: 0 6px 6px -6px #0E1119;
            }
            
            
            @media (max-width: 800px) {
            .container td:nth-child(4),
            .container th:nth-child(4) { display: none; }
            
            
            }
            
            
            </style>
        """, unsafe_allow_html=True)
  
# Page 2: Top 10 Recommendations
 
async def display_recommendations():
    device_name = st.session_state['device_name']
    predicted_class = st.session_state['predicted_class']
    content = st.session_state['content']
    
    why = await why_class(device_name,predicted_class,content)
    # top_k_results = [{'index': 1, 'label': 0, 'description': "This is a medical device.", 'image': 'medical_device.jpg', 'device_name': "A"}]
    top_k_results = query_similar_embeddings(content)  # Adjust arguments as needed

    descriptions = load_descriptions()  # Load descriptions from the JSON file
    if top_k_results:

        for res in top_k_results:
            res['index'] = int(res['index'])
            res['label'] = int(res['label'])
            res['label'] = SPECIFIED_TAGS[res['label']]
            res['description'] = descriptions.get(str(res['index']), "No description available")  # Add description
        
        results_with_images = []

        for res in top_k_results:
            image_path = get_image_path(res['index'])
            if image_path:  # If the image exists, add it to the results
                results_with_images.append({
                    'device_name': res['device_name'],
                    'label': res['label'],
                    'image': image_path,
                    'description': res['description']
                })


    col1, col2,col3,col4,col5 = st.columns([1,3,4,2,2])
    with col3:
        
        st.markdown("""                    
                    <h1 style="text-align: center; font-size: 3.5rem; color:white;">Top 10 Recommendations</h1>
                """, unsafe_allow_html=True)
    with col5:
        if st.button("Back to Home"):
            navigate_to_page('home')
            st.rerun()
    # print("---------------------------------------")
    # print(predicted_class)
    if predicted_class=="Class A":
        card_img=load_image("logos/A.png")
    elif predicted_class=="Class B":
        card_img=load_image("logos/B.png")
    elif predicted_class=="Class C":
        card_img=load_image("logos/C.png")
    elif predicted_class=="Class D":
        card_img=load_image("logos/D.png")


    st.markdown(f"""
    <div class="wrapper">
    <div class="flip-container">
        <div class="flip-card" style="transform: rotateY(0deg);border:None;background:transparent;">
            <div class="flip-card-front" style="padding:0px;background:none;" >
                <div class="prediction-card" style="width: 100%; height: 100%;overflow: auto; ">
                    <div class="class-value">
                        <img src="data:image/jpeg;base64,{card_img}" class="card-image" alt="Card Image"  style=" width:80px;"/>
                        <span style="color:#efbf04;">Predicted Class:{predicted_class} </span> <!-- Replace 'A' with the actual predicted class dynamically -->
                    </div>
                    <div style="color:#E0B0FF;font-size:36px;font-weight:bold;">{device_name}</div>
                    <p>{content}</p>
                    <div class="class-value" style="display:none;">
                        <img src="data:image/jpeg;base64,{card_img}" class="card-image" alt="Card Image"  style=" width:80px;"/>
                        <span style="color:#efbf04;">Predicted Class:{predicted_class} </span> <!-- Replace 'A' with the actual predicted class dynamically -->
                    </div>
                </div>
            </div>
            <div class="flip-card-back">
                <p>Back of Card</p>
            </div>
        </div>
    </div>
        <div class="flip-container" >
        <div class="flip-card">
            <div class="flip-card-front" >
                <h2 style="font-size:36px;font-weight:bold;color:#E0B0FF;">Why this device is classified in <span style="color:#efbf04;">{predicted_class} </span>?</h2>
            </div>
            <div class="flip-card-back" style="overflow-y:auto;">
                <p style="font-size:1.3rem;">{why}</p>
            </div>
        </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
   
        
    st.markdown(f"""
    <table class="container">
        <thead>
            <tr>
                <th><h1>Device Name</h1></th>
                <th><h1>Label</h1></th>
                <th><h1>Image</h1></th>
                <th><h1>Description</h1></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{results_with_images[0]['device_name']}</td>
                <td>{results_with_images[0]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[0]['image'])}' width='120'/></td>
                <td>{results_with_images[0]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[1]['device_name']}</td>
                <td>{results_with_images[1]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[1]['image'])}' width='120'/></td>
                <td>{results_with_images[1]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[2]['device_name']}</td>
                <td>{results_with_images[2]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[2]['image'])}' width='120'/></td>
                <td>{results_with_images[2]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[3]['device_name']}</td>
                <td>{results_with_images[3]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[3]['image'])}' width='120'/></td>
                <td>{results_with_images[3]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[4]['device_name']}</td>
                <td>{results_with_images[4]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[4]['image'])}' width='120'/></td>
                <td>{results_with_images[4]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[5]['device_name']}</td>
                <td>{results_with_images[5]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[5]['image'])}' width='120'/></td>
                <td>{results_with_images[5]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[6]['device_name']}</td>
                <td>{results_with_images[6]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[6]['image'])}' width='120'/></td>
                <td>{results_with_images[6]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[7]['device_name']}</td>
                <td>{results_with_images[7]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[7]['image'])}' width='120'/></td>
                <td>{results_with_images[7]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[8]['device_name']}</td>
                <td>{results_with_images[8]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[8]['image'])}' width='120'/></td>
                <td>{results_with_images[8]['description']}</td>
            </tr>
            <tr>
                <td>{results_with_images[9]['device_name']}</td>
                <td>{results_with_images[9]['label']}</td>
                <td><img src='data:image/jpeg;base64,{load_image(results_with_images[9]['image'])}' width='120'/></td>
                <td>{results_with_images[9]['description']}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
 
