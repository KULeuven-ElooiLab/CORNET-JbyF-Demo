import streamlit as st
import streamlit as st
from htbuilder import HtmlElement, div, hr, a, p, img, styles
from htbuilder.units import percent, px

import Startscherm,DoelVanHetProject,SterkteVoorspellen,WorkflowVoorML,Login

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 65px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, -10, 0),
        width=percent(100),
        color="black",
        text_align="left",
        height="bottom",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(1, 1, 5, 1),
        border_style="inset",
        border_width=px(0.5)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        
        link("https://www.mtm.kuleuven.be/english/research/elooi", image('https://www.kuleuven.be/internationaal/thinktank/fotos-en-logos/ku-leuven-logo.png',
        height=px(40), marginLeft= "20px")),
        
        link("https://www.vlaio.be/nl",image('https://repairshare.be/wp-content/uploads/2022/01/vlaiologo.png',
        	 height=px(40), marginLeft= "20px")),

        link("https://www.fraunhofer.de/en.html",image('https://www.eitfood.eu/media/partners-startups/fraunhofer_fhg.png',
        	 height=px(40), marginLeft= "20px", marginRight= "20px")),

        "📝 <strong>Contact info:</strong> sam.coppieters@kuleuven.be ",
    ]
    layout(*myargs)

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# All python codes for each tab
pages = [
        DoelVanHetProject,
        SterkteVoorspellen,
        WorkflowVoorML,
        Startscherm,
        Login
    ]

# when the aplication reruns, the variable 'nr' will not be saved
# with experimental_get_query_params is it possible to get the value of a saved variable
if "nr" in st.experimental_get_query_params():
    nr = int(st.experimental_get_query_params()["nr"][0])
else:
    nr = 4 # at the first run of the program, 'nr' does not exist yet (initialistaion step)
    
# the def show_page returns a number to indicate which tab we want to navigate to.
# when no pictures are clicked, 'Stratscherm.py' will return -1. This needs to be 3
number = pages[nr].show_page()
if  number==-1:
    number = 3
  
# save the variable whit name 'nr' and value number
st.experimental_set_query_params(nr=number)

# We want to rerun the code is a tab was selected that is not active yet.
if nr != number:
    st.experimental_rerun()

# add the logo's in the bottom of the app
footer()