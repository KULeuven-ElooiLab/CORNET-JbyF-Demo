import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw,ImageFont
import pickle
import requests, os
import text


from copy import deepcopy
import base64

def show_page():

    def predict_strength(test):
        # A model for each output variable (TT= top tensile test, otherwise ST = shear test)
        if test=="TT":
            openFile = "docs/SVR_Max_top_tensile_force_TT.pkl"
        else:
            openFile = "docs/SVR_Max_shear_tensile_force_ST.pkl"
        loaded_model = pickle.load(open(openFile , 'rb')) 
        # Must be in the same order as when training the model   
        X = [[material_top,
                material_bottom,
                strength_top,
                strength_bottom,
                sheet_thickness1,
                sheet_thickness2,
                die_depth,
                die_angle_wall,
                die_angle_anvil,
                diameter_anvil,
                punch_angle_wall,
                punch_diameter,
                interlock,neck_thickness,
                bottom_thickness,
                min_topThickness,
                min_bottomThickness,
                joining_force]]
        predicted_force = loaded_model[0].predict(X)
        return float(predicted_force)
        

    # -- Set page config
    

    

    # __________________________________________Menu on the left__________________________________________
    with st.sidebar.form('input for ML'):
        # ----------------Material properties---------------------
        st.markdown("# Select the material properties")
        

        #           ***   Top sheet properties   ***
        st.markdown("### Properties for top sheet")

        #-- Set Steel or Aluminum 
        if st.selectbox('Select the material:',['Steel', 'Aluminium'])=="Steel":
            # trained model can not handle strings
            material_top = 1
        else:
            material_top = 2
        #-- Set tensile strength                                    
        strength_top = st.number_input('What is the tensile strength of the material [MPa]', value = 264.0982459)
        #-- Set sheet thickness
        sheet_thickness1 = st.slider('Set the sheet thickness [mm]', 0.0, 2.0, 1.7)

        #           ***   Buttom sheet properties   ***
        st.markdown("### Properties for bottom sheet")

        #-- Set Steel or Aluminum
        if st.selectbox('Select the material:',['Aluminium','Steel'])=="Steel":
            # trained model can not handle strings
            material_bottom = 1
        else:
            material_bottom = 2
        #-- Set tensile strength                                    
        strength_bottom = st.number_input('What is the tensile strength of the material [MPa] ', value = 277.1778877)
        #-- Set sheet thickness
        sheet_thickness2 = st.slider('Set the sheet thickness [mm] ', 0.0, 2.0, 1.5)


        # ----------------Material properties---------------------
        st.markdown("# Determine the tool geometrie")

        #           ***   Die properties   ***
        st.markdown("### Dimensions of the die")

        #-- Set die depth
        die_depth = st.slider('Set the depth of the die [mm]', 0.0, 10.0, 1.4)
        #-- Set anvil diameter
        diameter_anvil = st.slider('Set the diameter of the anvil [mm]', 0.0, 7.0, 4.9)
        #-- Set wall angle β
        die_angle_wall = st.slider('Set the angle of the wall [°]', 0.0, 10.0, 5.0)
        #-- Set anvil angle δ
        die_angle_anvil = st.slider('Set the angle between the anvil and the groove [°]', 0.0, 60.0, 21.8)

        #           ***   Punch properties   ***
        st.markdown("### Dimensions of the punch")

        #-- Set angle
        punch_angle_wall = st.slider('Set the angle of the wall [°] ', 0.0, 10.0, 2.5)
        #-- Set die depth
        punch_diameter = st.slider('Set the diameter of punch [mm]', 0.0, 7.0, 5.0)


        # ----------------Joining results---------------------
        st.markdown("# Fill in the joining results")

        #-- Set interlock 
        interlock = st.number_input('What is the interlock [mm]', value = 0.38)
        #-- Set neck thickness 
        neck_thickness = st.number_input('What is the neck thickness [mm]', value = 0.387)
        #-- Set bottom thickness 
        bottom_thickness = st.number_input('What is the bottom thickness [mm]', value = 0.673)
        #-- Set min bottom thickness top sheet 
        min_topThickness = st.number_input('What is the min bottom thickness top sheet [mm]', value = 0.43)
        #-- Set min bottom thickness bottom sheet 
        min_bottomThickness = st.number_input('What is the min bottom thickness bottom sheet [mm]', value = 0.193)
        #-- Set joining force
        joining_force = st.number_input('What is the max joining force [kN]', value = 54)
        st.form_submit_button('apply changes')


    # __________________________________________Main screen of the application__________________________________________

    # Title the app
    emptycol1,col,emptycol2 =st.columns([1,6,1])
    with col:
        st.markdown('## Strength prognosis based on machine learning')

        text.Machine_General()
        st.markdown("""
        * 	Use the menu on the left to alter the input parameters
        *   The corresponding dimensions will be illustrated on the figure below        
        * 	After changing a parameter, the strength is automatically recalculated
        """)


    # ----------------Make the prediction---------------------

    emptycol1,col1, col2,emptycol2 = st.columns([1,3,3,1])
    with col1:
        st.write('### Max top tensile strenth')
        st.metric('',"{:0.2f} kN".format(predict_strength("TT")))
    with col2:
        st.write('### Max shear strength')
        st.metric('',"{:0.2f} kN".format(predict_strength("ST")))


    # ----------------Display the image---------------------

    #-- Open the image
    image1 = Image.open('docs/InputML1.jpg')
    image2 = Image.open('docs/InputML2.jpg')
    #-- Make it posseble to overlay the image with text 
    colour = (50,50,50)
    font = ImageFont.FreeTypeFont("docs/Cambria Math.ttf", size=17)
    font1 = ImageFont.truetype("arial.ttf",15)

    #-- Write each parameter on the image based on the pixel coordinate
    # -----Tools-----
    draw = ImageDraw.Draw(image1)
    # die depth
    draw.text((305,60), str('{:0.2f}'.format(die_depth))+' mm', colour,font1)
    # diameter anvil
    draw.text((190,50), str('{:0.2f}'.format(diameter_anvil))+' mm', colour,font1)
    # die angle wall
    draw.text((100,80), str('{:0.2f}'.format(die_angle_wall))+' °', colour,font1)
    # die angle anvil
    draw.text((190,95), str('{:0.2f}'.format(die_angle_anvil))+' °', colour,font1)
    # punch angle wall
    draw.text((555,170), str('{:0.2f}'.format(punch_angle_wall))+' °', colour,font1)
    # punch diameter
    draw.text((540,210), str('{:0.2f}'.format(punch_diameter))+' mm', colour,font1)
    # punch diameter
    draw.text((190,130),'8.00 mm', colour,font1)

    draw = ImageDraw.Draw(image2)
    # -----Geometrical parameters-----
    # tickness 1
    draw.text((20,100), str(sheet_thickness1)+' mm', colour,font)
    # tickness 2
    draw.text((20,150), str(sheet_thickness2)+' mm', colour,font)
    # interlock
    draw.text((168,50), str('{:0.3f}'.format(interlock))+' mm', colour,font)
    # neck tickness
    draw.text((380,50), str('{:0.3f}'.format(neck_thickness))+' mm', colour,font)
    # bottom thickness
    draw.text((100,215), str('{:0.3f}'.format(bottom_thickness))+' mm', colour,font)
    # min bottom thickness top sheet
    draw.text((130,260), str('{:0.3f}'.format(min_topThickness))+' mm', colour,font)
    # min bottom thickness bottom sheet 
    draw.text((555,240), str('{:0.3f}'.format(min_bottomThickness))+' mm', colour,font)

    #-- Display the image in Streamlit webApp
    emptycol1,col2,emptycol2 =st.columns([1.5,4,1])
    emptycol1,col1,emptycol2 =st.columns([1.1,3,1])
    with col1:
        st.image(image1)
    with col2:
        st.image(image2)

    return
