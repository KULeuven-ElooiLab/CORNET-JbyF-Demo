import streamlit as st
import Startscherm,DoelVanHetProject,SterkteVoorspellen,WorkflowVoorML

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# All python codes for each tab
pages = [
        DoelVanHetProject,
        SterkteVoorspellen,
        WorkflowVoorML,
        Startscherm
    ]

# when the aplication reruns, the variable 'nr' will not be saved
# with experimental_get_query_params is it possible to get the value of a saved variable
if "nr" in st.experimental_get_query_params():
    nr = int(st.experimental_get_query_params()["nr"][0])
else:
    nr = 3 # at the first run of the program, 'nr' does not exist yet (initialistaion step)
    
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


