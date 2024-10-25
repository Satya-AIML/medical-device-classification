import streamlit as st
from Bio_Device_Classifier.pipeline.recomendation import query_similar_embeddings
from Bio_Device_Classifier.pipeline.prediction import prediction
from Bio_Device_Classifier.constants import SPECIFIED_TAGS
from PIL import Image
import os

image_directory = "/home/rajvs/Medical-Device-Classification/Generated_Images"

# Function to store text input and prediction result in session state
def store_input(content, predicted_class):
    st.session_state['input_text'] = content
    st.session_state['predicted_class'] = predicted_class

# Function to get image path
def get_image_path(index):
    image_path = os.path.join(image_directory, f"{index}.png")
    if os.path.exists(image_path):
        return image_path
    else:
        return None

# Function to display top results with images
def display_top_results(top_k_results, SPECIFIED_TAGS):
    
    results_with_images = []
    
    for res in top_k_results:
        res['index'] = int(res['index'])
        res['label'] = SPECIFIED_TAGS[int(res['label'])]
        image_path = get_image_path(res['index'])
        
        if image_path:
            results_with_images.append({
                'device_name': res['device_name'],
                'label': res['label'],
                'image': image_path
            })
    
    # Display the results
    st.write("### Top Results")
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.write("**Device Name**")
    with col2:
        st.write("**Label**")
    with col3:
        st.write("**Image**")

    # Populate the table rows
    for result in results_with_images:
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.write(result['device_name'])  # Display device name
        with col2:
            st.write(result['label'])  # Display label
        with col3:
            image = Image.open(result['image'])
            st.image(image, width=100)  # Display image

# Main function for the first page (Text Classification)
def page1():
    st.title("Get your device classified")
    
    input_option = st.radio("Choose your input method", ("Upload a file", "Enter text manually"))

    content = None
    if input_option == "Upload a file":
        uploaded_file = st.file_uploader("Upload a Text or PDF file", type=["txt", "pdf"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
    elif input_option == "Enter text manually":
        content = st.text_area("Enter your text here")

    if content:
        st.text_area("Input content", content, height=50)
        if st.button("Submit"):
            try:
                # Call the prediction function
                data = {"text": content}
                result = prediction(data)
                predicted_class = result.get("predicted_class", "No class predicted")
                
                # Store the content and predicted class in session state
                store_input(content, predicted_class)
                
                # Display the predicted class
                st.success(f"Predicted Class: {predicted_class}")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

# Main function for the second page (Top 10 Recommendations)
def page2():
   

    if 'input_text' in st.session_state:
        content = st.session_state['input_text']
        predicted_class = st.session_state.get('predicted_class', "Unknown")
        
        content = "This is a sample input text"
        predicted_class = "Class B"

# Display input with custom font size
        st.markdown(
            f"<p style='font-size:25px;'>Your input: {content}</p>", 
            unsafe_allow_html=True
        )

        # Display predicted class with custom font size
        st.markdown(
            f"<p style='font-size:25px; font-weight:bold;'>Predicted Class: {predicted_class}</p>", 
            unsafe_allow_html=True
        )

        # Display device description with custom font size
        st.markdown(
            "<p style='font-size:25px;'>Device Description</p>", 
            unsafe_allow_html=True
        )
        try:
            # Call the recommendation function to get top 10 similar embeddings
            st.markdown("---")
            st.title("Top 10 Recommendations")
            top_k_results = query_similar_embeddings(content)
            
            # Display the top results
            display_top_results(top_k_results, SPECIFIED_TAGS)
        except Exception as e:
            st.error(f"Error fetching recommendations: {e}")
    else:
        st.error("No input found. Please enter text on the first page.")

# Define the app navigation
pages = {
    "Text Classification": page1,
    "Top 10 Recommendations": page2
}

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
pages[page]()
