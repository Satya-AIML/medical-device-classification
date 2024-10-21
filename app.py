import pandas as pd
import streamlit as st
import os
from PyPDF2 import PdfReader
from PIL import Image
import matplotlib.pyplot as plt
from Bio_Device_Classifier.pipeline.recomendation import query_similar_embeddings
from Bio_Device_Classifier.pipeline.prediction import prediction
from Bio_Device_Classifier.constants import SPECIFIED_TAGS
from Bio_Device_Classifier.logging import logger


# Set page layout to wide
st.set_page_config(layout="wide")

image_directory = "/home/rajvs/Medical-Device-Classification/Generated_Images"


def read_pdf(file):
    """Reads and extracts text from a PDF file."""
    pdf_reader = PdfReader(file)
    text = ''.join([page.extract_text() for page in pdf_reader.pages])
    return text


def get_content(input_option):
    """Gets content from the user input, either through file upload or manual input."""
    content = None

    if input_option == "Upload a file":
        uploaded_file = st.file_uploader("Upload a Text or PDF file", type=["txt", "pdf"])
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                content = read_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                content = uploaded_file.read().decode("utf-8")
            else:
                st.error("Unsupported file type")

    elif input_option == "Enter text manually":
        content = st.text_area("Enter your text here")
    
    if content:
        st.text_area("Input content", content, height=50)
    
    return content


def display_prediction_result(content):
    """Submits the content for prediction and displays the result."""
    if content and st.button("Submit for prediction"):
        try:
            data = {"text": content}
            logger.info(f"Calling prediction with data: {data}")
            result = prediction(data)
            predicted_class = result.get("predicted_class", "No class predicted")
            st.success(f"Predicted Class: {predicted_class}")
            
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            logger.error(f"Prediction error: {e}")
            

# Function to display images for each index
def get_image_path(index):
    image_path = os.path.join(image_directory, f"{index}.png")
    if os.path.exists(image_path):
        return image_path
    else:
        return None  # If the image doesn't exist

# Function to display a specific image from the DataFrame
def show_image_from_dataframe(df, index):
    """Displays an image from the DataFrame at the specified index."""
    if index < len(df):
        image_path = df.loc[index, 'image_path']
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Create a figure and axis
            plt.figure(figsize=(6, 6))  # Adjust size as needed
            plt.imshow(image)  # Display the image
            plt.axis('off')  # Hide axes
            plt.title(df.loc[index, 'device_name'])  # Set the title from the DataFrame
            plt.show()  # Show the plot
        except Exception as e:
            print(f"Error displaying image: {e}")
    else:
        print("Index out of range")
 
# Function to check if the image path exists
def check_image_path_exists(image_path):
    return os.path.exists(image_path)

def transform_dataframe(df):
    """Displays the queried embeddings dataframe."""
    if df is not None and not df.empty:
        try:
            df['label'] = df['label'].apply(lambda x: SPECIFIED_TAGS[int(x)])

            df['index'] = df['index'].apply(lambda z: int(z))

            df['image_path'] = df['index'].apply(get_image_path)

            df['image_exists'] = df['image_path'].apply(check_image_path_exists)

            print(df)
        except Exception as e:
            st.error(f"Error transforming dataframe: {e}")
            logger.error(f"Dataframe transforming error: {e}")


def display_dataframe(df):
    """Displays the queried embeddings dataframe."""
    transform_dataframe(df)
    # Filter the DataFrame to include only the necessary columns
    # filtered_df = df[['device_name','image_path','label']]
    filtered_df = df[['image_path']]
    print(filtered_df)
    # print(type(filtered_df["image_path"][0]))
    # print(filtered_df["image_path"][0])
    if df is not None and not df.empty:
        try:
            col = filtered_df.columns
            print(col)
            st.data_editor(
                filtered_df,
                column_config={
                    'image_path': st.column_config.ImageColumn(
                        "Device Picture",
                        help="Generated Image from Stable Diffusion",
                    )

                },
                hide_index=True,
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error displaying dataframe: {e}")
            logger.error(f"Dataframe display error: {e}")
    else:
        st.warning("No similar embeddings found. The dataframe is empty.")


def main():
    """Main function to run the Streamlit app."""
    st.title("Medical Device Classification App")
    
    with st.container():
        # Create two columns (panes)
        col1, col2 = st.columns([1, 2])

        # Pane 1 (Input options and Submit button)
        with col1:
            input_option = st.radio("Choose your input method", ("Upload a file", "Enter text manually"))
            content = get_content(input_option)

            # If content is available, display the prediction result
            display_prediction_result(content)


        # Pane 2 (Dataframe display)
        with col2:
            top_k_results = query_similar_embeddings(content)
            print(top_k_results)


            for res in top_k_results:
                res['index'] = int(res['index'])
                res['label'] = int(res['label'])
                res['label'] = SPECIFIED_TAGS[res['label']]
            
            results_with_images = []

            for res in top_k_results:
                image_path = get_image_path(res['index'])
                if image_path:  # If the image exists, add it to the results
                    results_with_images.append({
                        'device_name': res['device_name'],
                        'label': res['label'],
                        'image': image_path
                    })
                
            st.write("### Top Results")
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.write("**Device Name**")
            with col2:
                st.write("**Label**")
            with col3:
                st.write("**Image**")
            
            # Populating the table rows
            for result in results_with_images:
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.write(result['device_name'])
                with col2:
                    st.write(result['label'])
                with col3:
                    image = Image.open(result['image'])
                    st.image(image, width=100)



if __name__ == "__main__":
    main()
