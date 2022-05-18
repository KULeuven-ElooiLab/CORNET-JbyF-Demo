from st_clickable_images import clickable_images
import base64
import streamlit as st
from PIL import Image


def show_page():
    
    # code to make pictures clickable
    images = []
    listOfImages = ["docs/Tab1.jpg","docs/Tab2.jpg","docs/Tab3.jpg"]
    for file in listOfImages:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    clicked = clickable_images(
        images,
        titles=['doel','sterkte','workflow'],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={ "width":"33%",'border':'1px'},
    )
    return clicked
    
    
