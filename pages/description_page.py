import streamlit as st
import base64
from io import BytesIO
from Bio_Device_Classifier.logging import logger

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

def navigate_to_page(page_name):
    """
    Navigate to a different page by updating the session state.

    Args:
        page_name (str): The name of the page to navigate to.
    """
    st.session_state.page = page_name

main_img = load_image("logos/MDC Flowchart.png")
card1=load_image("logos/1.png")
card2=load_image("logos/2.png")
card3=load_image("logos/3.png")
card4=load_image("logos/4.png")
    
def display_description():
    _, _, col3, _, col5 = st.columns([1, 3, 4, 2, 2])
    
    with col3:
            st.markdown("""
                    <h1 style="text-align: center; font-size: 3.5rem; color:white;">About</h1>    
                """, unsafe_allow_html=True)

    with col5:
        if st.button("Back to Home"):
            navigate_to_page('home')
            st.rerun()
    

    # Project Description Card
    with st.container():
      
      st.markdown("""
                  <style>
                        .project-description {
                            font-size: 26px; /* Increase font size for the paragraph */
                            line-height: 1.6; /* Optional: Adjust line height for better readability */
                            text-align: center; /* Center the text */
                            color: white; /* Change color to improve contrast if necessary */
                        }
                  </style>
                    
                    <p class="project-description">
                    This project focuses on automating the classification, generation, and recommendation of medical devices into distinct classes based on risk level and usage. It utilizes advanced machine learning models fine-tuned for the medical domain.</p>
                    """, unsafe_allow_html=True)

    # Device Classification Classes with Border
    st.markdown("""
                <style>
                .flip-card {
                    background-color: transparent;
                    width: 390px;
                    height: 450px;
                    perspective: 1000px;
                    margin: 13px;
                    display: inline-block;
                    border: 2px solid #23746f; /* Border color */
                    border-radius: 10px; /* Rounded corners */
                    box-shadow: 0 2px 3px #6db1ff; /* Shadow effect */
                    
                }

                .flip-card-inner {
                    position: relative;
                    width: 100%;
                    height: 100%;
                    text-align: center;
                    transition: transform 0.6s;
                    transform-style: preserve-3d;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    border-radius: 10px;
                }

                .flip-card:hover .flip-card-inner {
                    transform: rotateY(180deg);
                }

                .flip-card-front, .flip-card-back {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    -webkit-backface-visibility: hidden;
                    backface-visibility: hidden;
                    border-radius: 10px;
                    padding: 20px;
                    color: white;
                }

                .flip-card-front {
                    background-color: #02032f;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                }

                .flip-card-back {
                    background-color: #23746f;
                    transform: rotateY(180deg);
                    text-align: left;
                    font-size: 28px;
                }

                div.flip-card-back p {
                        font-size: 24px;
                        }
          /* Style for the horizontal line */
        .line {
            width: 100%;
            height: 2px; /* Adjust height for line thickness */
            background: linear-gradient(to right, 
                #0000FF, /* Blue (cooler color) */
                #00FFFF, /* Cyan */
                #FFFF00, /* Yellow */
                #FF7F00, /* Orange */
                #FF0000  /* Red (warmer color) */
            );
            margin-top: 20px; /* Space above the line */
            margin-bottom: 20px; /* Space below the line */
        }
        .card_wrapper
                {
                display:flex;
                flex-direction:column;
                justify-content:center;
                # border:2px solid white;
                width:100%;
                height:100%;
                }

    </style>
    <h1 style="font-size: 38px;color:white;">Device Classification Classes</h1>
    """, unsafe_allow_html=True)
  
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'''
        <div class="flip-card" style="border-color:#031B83;">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                <div class="card_wrapper">
                    <img src="data:image/jpeg;base64,{card1}" class="card-image" alt="Card Image"  style="max-width: 100%;"/>
                    <b  style="max-width: 100%;">Class A<br>Low Risk</b>
                </div>
                </div>
               <div class="flip-card-back" style="background-color:#031B83;">
                <p>Devices with minimal or no invasiveness, typically used on external body surfaces with low potential for harm.<br>
                <em>Examples:</em> Bandages, crutches, tongue depressors.</p>
            </div>
        </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
            <!-- Class B Card -->
            <div class="flip-card" style="border-color:#1F6600;">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                            <div class="card_wrapper">
                                <img src="data:image/jpeg;base64,{card2}" class="card-image" alt="Card Image"  style="max-width: 100%;"/>
                                <b  style="max-width: 100%;">Class B<br>Low to Moderate Risk</b>
                            </div>
                            </div>
                    <div class="flip-card-back" style="background-color:#1F6600;">
                        <p>Devices with limited invasiveness and typically short or intermittent contact, often for monitoring or diagnostic use.<br>
                        <em>Examples:</em> Blood pressure monitors, diagnostic devices, thermometers.</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <!-- Class C Card -->
            <div class="flip-card" style="border-color:#C18917;">
                <div class="flip-card-inner">
                <div class="flip-card-front">
                            <div class="card_wrapper">
                                <img src="data:image/jpeg;base64,{card3}" class="card-image" alt="Card Image"  style="max-width: 100%;"/>
                                <b  style="max-width: 100%;">Class C<br>Moderate to High Risk</b>
                            </div>
                            </div>
                    <div class="flip-card-back" style="background-color:#C18917;">
                        <p>Invasive devices that may contact sensitive tissues or remain for a prolonged duration, requiring regulatory oversight.<br>
                        <em>Examples:</em> Imaging devices, catheters, diagnostic ultrasound.</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col4:
        st.markdown(f'''
            <!-- Class D Card -->
            <div class="flip-card" style="border-color:#8F2702;">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                            <div class="card_wrapper">
                                <img src="data:image/jpeg;base64,{card4}" class="card-image" alt="Card Image"  style="max-width: 100%;"/>
                                <b  style="max-width: 100%;">Class D<br>High Risk</b>
                            </div>
                    </div>
                    <div class="flip-card-back" style="background-color:#8F2702;">
                        <p>Implantable or life-sustaining devices that support or replace essential body functions or deliver substances to critical areas.<br>
                        <em>Examples:</em> Cardiac implants, dialysis equipment, surgical devices.</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    with st.container():
       
       st.markdown("""
                <div class="line"></div> <!-- Single horizontal line covering all cards -->                

                <style>
                    .classification-border {
                        padding: 20px; /* Increased padding for better spacing */
                        margin-top: 20px; /* Increased margin for better separation */
                        
                    }
                    .classification-border h3 {
                        color: #ffffff; /* Light color for better contrast */
                        margin-bottom: 10px; /* Space below heading */
                    }
                    .classification-border ul {
                        list-style-type: none; /* Remove default list styling */
                        padding-left: 0; /* Remove default padding */
                    }
                    .classification-border ul li {
                        font-size: 18px;
                        color: #d0e7ff; /* Softer text color */
                        margin-bottom: 10px; /* Space between list items */
                        padding: 10px; /* Padding for each list item */
                        border: 2px solid #23746f; /* Border color */
                        border-radius: 10px; /* Rounded corners */
                        box-shadow: 0 2px 3px #6db1ff; /* Shadow effect */
                        border-radius: 5px; /* Rounded corners for list items */
                        background-color: #0a1f3b; /* Slightly different background for list items */
                    }
                    .classification-border ul li strong {
                        color: #6db1ff; /* Color for strong text */
                    }
                </style>
                        
                <div class="classification-border">
                    <h1 style="font-size: 38px; margin-top:-40px;color:white;">Project Models</h1>
                    <ul>
                        <li><strong>Classification Model</strong><br>
                            The fine-tuned <strong>BioBERT</strong> model classifies medical devices (Class A-D) with high accuracy by focusing on biomedical terminology and capturing subtle relationships within device descriptions.
                        </li>
                        <li><strong>Generation Models</strong><br> 
                            <strong>Stable Diffusion:</strong> Generates high-quality images for each classified medical device, providing visual support for better comprehension and decision-making.<br>
                            <strong>MedLLaMA:</strong> A medical-specific text generation model that produces detailed textual descriptions and supplementary information for each device, offering coherent and relevant information to support users. 
                        </li>
                        <li><strong>Recommendation Model</strong><br> 
                            This model leverages BioBERT to generate embeddings for medical devices, capturing their semantic essence. The embeddings are stored in a Pinecone database, enabling fast and precise similarity search through K-Nearest Neighbors (KNN). Based on embedding similarity, the model retrieves the top 10 device recommendations, aligned by function, risk, and other key characteristics, to assist users with relevant options for their needs.                 
                        </li>
                    </ul>
                </div>
                <div class="line"></div> <!-- Single horizontal line covering all cards -->
            """, unsafe_allow_html=True)

    # Displaying the main image
    with st.container():
      st.markdown(
          f"""
          <h1 style="font-size: 38px; margin-left:28px;color:white;">Flowchart</h1>
          <div style="display: flex; justify-content: center;">
              <img src="data:image/jpeg;base64,{main_img}" alt="Card Image" style="max-width: 70%; border-radius: 10px; padding: 5px;"/>
          </div>
          """,
          unsafe_allow_html=True)

