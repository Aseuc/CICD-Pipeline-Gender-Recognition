import torch
from torchvision import transforms
from model.ml_model_scripts.pytorch_train import SimpleCNN
import streamlit as st
import PIL as Image


def predict(image, model_path):
    # Define the transformation
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    # Apply the transformation and add an extra dimension
    image = transform(image)
    image = image.unsqueeze(0)

    # Load the model
    model = SimpleCNN()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # Make the prediction
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)

    return predicted.item()

# Streamlit code
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("Image successfully uploaded.")

    model_path = st.text_input("Enter the path to the trained model:")
    if model_path:
        prediction = predict(image, model_path)
        st.write(f"Prediction: {prediction}")