import streamlit as st
import numpy as np
import imageio
import scipy.ndimage
import cv2
from PIL import Image

# Function to convert image into sketch
def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

def dodge(front, back):
    final_sketch = front * 255 / (255 - back)
    final_sketch[final_sketch > 255] = 255
    final_sketch[back == 255] = 255
    return final_sketch.astype('uint8')

# Streamlit app
st.title("Image to Sketch Converter")

# Upload image file
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Convert and display the sketch
    if st.button("Convert to Sketch"):
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        gray = rgb2gray(img_array)
        inverted_gray = 255 - gray
        blurred = scipy.ndimage.filters.gaussian_filter(inverted_gray, sigma=13)
        sketch = dodge(blurred, gray)
        st.image(sketch, caption="Sketch", use_column_width=True)

        # Allow the user to download the sketch
        if st.button("Download Sketch"):
            cv2.imwrite('sketch.png', sketch)
            st.success("Sketch downloaded successfully as 'sketch.png'")
