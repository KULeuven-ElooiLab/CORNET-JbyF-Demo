from ast import For
from cmath import sqrt, tan
import imp
from math import pi
import text


from ssl import ALERT_DESCRIPTION_UNSUPPORTED_EXTENSION
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw,ImageOps
from st_clickable_images import clickable_images
import base64


#-- Make a dictionary of all variables
values = {'neck_thickness':[],'inner_diameter':[],'radius_disc': [],'wall_thickness': [],'yield_tube': [],
    'yield_disc': [],'coulomb': [],'angle': [],'UTS':[],'t1':[],'interlock':[],'bottom_thickness':[],'AFS':[]
    }
def centerImage(pathImage,width,underscript):
    images = []
    
    with open(pathImage, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    clicked = clickable_images(
                images,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={'width':f'{width}'},
            )
    if underscript!='':
        st.markdown(f"<p style='text-align: center; color: grey;'>{underscript}</p>", unsafe_allow_html=True)
    return clicked

def getForce(v,variant):
        list_strength = []
        for i in range(len(list(v.values())[0])):
            # Formula coppieters
            A = pi/4*((v['inner_diameter'][i]+2*v['neck_thickness'][i])**2-v['inner_diameter'][i]**2)
            B = v['coulomb'][i]/np.tan(np.radians(v['angle'][i]))
            ExitRod =v['inner_diameter'][i]+2*v['wall_thickness'][i]
            if v['interlock'][i]/np.tan(np.radians(v['angle'][i]))<v['bottom_thickness'][i]:
                ExitRod1 = v['inner_diameter'][i]+2*v['neck_thickness'][i]
            else:
                ExitRod1 = v['inner_diameter'][i]+2*(v['neck_thickness'][i]+v['interlock'][i]-v['bottom_thickness'][i]*np.tan(np.radians(v['angle'][i])))
            EntryRod1 = v['inner_diameter'][i]+2*(v['neck_thickness'][i]+v['interlock'][i])
            Q = (ExitRod1**2*v['yield_disc'][i]*((1+B)/B)*(1-(ExitRod1/EntryRod1)**(2*B)))/(ExitRod1**2-v['inner_diameter'][i]**2)
            H = ((4*pi)/np.sqrt(3))*v['yield_tube'][i]*((1+B)/(2*pi-(1+B)))
            P = ((ExitRod1**2-v['inner_diameter'][i]**2)/((v['inner_diameter'][i]+2*v['neck_thickness'][i])**2-v['inner_diameter'][i]**2))**((2*pi-(1+B))/(2*pi))
            
            if variant == 'TT_def':
                # if bottom thickness is greater then the interlock height
                if v['interlock'][i]/np.tan(np.radians(v['angle'][i]))<v['bottom_thickness'][i]:
                    TT_def = (pi/4*ExitRod1**2*v['yield_disc'][i]*((1+B)/B)*(1-(ExitRod1/EntryRod1)**(2*B)))/1000
                # if bottom thickness is smaller then the interlock height
                else:
                    TT_def = A*(-H+(Q+H)*P)/1000
                list_strength.append(TT_def)
            elif variant == 'TT_def_original':
                TT_def_original =((A*(-(((4*pi)/np.sqrt(3))*v['yield_tube'][i]*((1+B)/(2*pi-(1+B))))+(((ExitRod**2*v['yield_disc'][i]*((1+B)/B)*(1-(ExitRod/v['radius_disc'][i])**(2*B)))
                /(ExitRod**2-v['inner_diameter'][i]**2))+(((4*pi)/np.sqrt(3))*v['yield_tube'][i]*((1+B)/(2*pi-(1+B)))))*
                (((v['inner_diameter'][i]+2*v['wall_thickness'][i])**2-v['inner_diameter'][i]**2)/((v['inner_diameter'][i]+2*v['neck_thickness'][i])**2-v['inner_diameter'][i]**2))**((2*pi-(1+B))/(2*pi))))/1000)*0.63
                list_strength.append(TT_def_original)
            elif variant == 'TT_frac':
                TT_frac = A * v['UTS'][i]/1000
                list_strength.append(TT_frac)
            elif variant == 'ST_def':
                ST_def = A * v['AFS'][i]/np.sqrt(3)/1000
                list_strength.append(ST_def)
            elif variant == 'ST_frac':
                ST_frac = 0.25*0.4*v['t1'][i]*(2*v['inner_diameter'][i]+0.4*v['t1'][i])*pi*v['UTS'][i]/1000
                list_strength.append(ST_frac)
        return list_strength


    
def show_page():

    # _______________Side bar_______________
    input_methode = st.sidebar.selectbox('Select input methode', ['Manual','Excel'])
    if 'Manual' == input_methode:
        with st.sidebar.form('input for the formulas'):
            # _______________Variables displayed on the sidebar_______________

            #-- Set neck thickness 
            values['neck_thickness']=[st.number_input('What is the neck thickness tn [mm]', value = 0.375)]
            #-- Set inner diameter clinch 
            values['inner_diameter']=[st.number_input('What is the inner diameter of the clinch d [mm]', value = 5.84)]
            #-- Set max radius disc
            values['radius_disc']=[st.number_input('What is the max radius of the disc [mm]', value = 7.77)]
            #-- Set max wall thickness 
            values['wall_thickness']=[st.number_input('What is the max wall thickness [mm]', value = 0.883)]
            #-- Set ultimate tensile stress  
            values['UTS']=[st.number_input('What is the UTS of the top sheet [MPa]', value = 260)]
            #-- Set average yield stress tube 
            values['yield_tube']=[st.number_input('What is the average yield stress in the tube part [MPa]', value = 370.18)]
            #-- Set average yield stress disc 
            values['yield_disc']=[st.number_input('What is the average yield stress in the disc part [MPa]', value = 237.07)]
            #-- Set average yield stress tube (Chan-Joo lee) 
            values['AFS']=[st.number_input('What is the average yield stress in the extended tube part (AFS) [MPa] ', value = 369.8)]
            #-- Set average coulomb friction
            values['coulomb']=[st.number_input('What is the average coulomb friction [-]', value = 0.1)]
            #-- Set angle of interlock
            values['angle']=[st.number_input('What is the angle of the interlock α [°]', value = 16.79)]
            #-- Set thickness of top sheet
            values['t1']=[st.number_input(r"What is the thickness of the top sheet t1 [mm]", value = 1.7)]
            #-- Set interlock
            values['interlock']=[st.number_input('What is the interlock of the joint f [mm]', value = 0.224)]
            #-- Set minimum bottom thickness of top sheet
            values['bottom_thickness']=[st.number_input('What is the minimum bottom thickness of the top sheet tb,p-min [mm]', value = 0.379)]
            st.form_submit_button('apply changes')
    else:
        # Download the template based on the value dictionary
        st.sidebar.download_button("Download template", pd.DataFrame([values.keys()]).to_csv(sep = ';',header = False ,index=False), file_name="template.csv")
        # Element to upload a file
        uploadedFile  = st.sidebar.file_uploader("Import the excel with all your data",type=["xlsx"])
        
        
    # _______________Main screen_______________
    emptycol1,col,emptycol2 =st.columns([1,6,1])
    
    with col:
        st.markdown("## Strength prognosis based on analytical formulas")

        # -- print a discription of the formulas
        text.analytical_General()

        

            
        text.analytical_howItWorks()
        
        with st.expander("Discription of the calculation parameter"):
            centerImage(pathImage='docs/Parameter1.jpg',width='70%',
            underscript='Basic parameters that can be measured during a cross section analysis')
            centerImage(pathImage='docs/Parameters2.png',width='100%',
            underscript='These are the average stresses taken from the FE-software. Left: Simplification based on tube drawing process. Right: Combination of tube and rod drawing ')
            

        with st.expander("Discription of the formulas"):
            
            text.analytical_TT()
            text.analytical_ST()
        st.write('### Results')
        if 'Manual' == input_methode:
            
            
            TT_def = "{:0.2f} kN".format(float(getForce(values,"TT_def")[0]))
            TT_frac = "{:0.2f} kN".format(float(getForce(values,"TT_frac")[0]))
            ST_def = "{:0.2f} kN".format(float(getForce(values,"ST_def")[0]))
            ST_frac = "{:0.2f} kN".format(float(getForce(values,"ST_frac")[0]))
            TT_def_original = "{:0.2f} kN".format(float(getForce(values,"TT_def_original")[0]))

            if TT_def<TT_frac:
                TT = TT_def
                modeTT = "deformation"
            else:
                TT = TT_frac
                modeTT = "fracture"

            if ST_def<ST_frac:
                ST = ST_def
                modeST = "deformation"
            else:
                ST = ST_frac
                modeST = "fracture"
            text.results(TT, modeTT, ST, modeST)
    # -- Based on the selectbox, the strength will be calculated for 1 or multiple joints 
        if 'Excel' == input_methode:
            try:
                # read the uploaded file
                df = pd.read_excel(uploadedFile) # it is important that the titles in the excel are indentical to those used in def 'getForce'
                # display the database
                st.dataframe(df)
                # import al the data into de dictionary 'val'
                val={}
                for i in df:
                    val[i]=list(df[i].to_numpy())
                    print(val.keys())
                try:
                    # add the results to the dataframe
                    df['TT_def']=getForce(val,'TT_def')
                    df['TT_frac']=getForce(val,'TT_frac')
                    df['ST_def']=getForce(val,'ST_def')
                    df['ST_frac']=getForce(val,'ST_frac')
                    file_name = st.text_input('Name the file', "Strength_predictions")
                    # Make it posible to download the results as csv file
                    st.download_button('Download strength predictions', df.to_csv(sep = ';',index=False,decimal=','), file_name = file_name + ".csv")
                except:
                    st.error('The column names are not correct or there is data missing.')
            except:
                st.warning('You must first upload a file at the sidebar on the left.')
            
        
    if 'Manual' == input_methode:  
        # with st.expander("see all results"):
            emptycol1,col1, col2,col3,emptycol2 = st.columns([1,2,2,2,1])
            with col1:
                new_title = '<p style="font-family:sans-serif; color:White; font-size: 30px;">New image</p>'
                st.markdown(new_title, unsafe_allow_html=True)
                st.header(r"$$F_{def}$$")
                st.header(r"$$F_{frac}$$")

            with col2:
                st.write('### Top tensile')
                st.metric('',TT_def)
                st.metric('',TT_frac)
                st.metric('',TT_def_original)

            with col3:
                st.write('### Shear lap')
                st.metric('',ST_def)
                st.metric('',ST_frac)   
    
    return