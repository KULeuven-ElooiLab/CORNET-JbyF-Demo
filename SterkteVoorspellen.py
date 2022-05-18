import streamlit as st
import hydralit_components as hc

import ML_clinch
import Analytical_clinch




def show_page():
    # Navigationbar
    menu_data = [
    {'label':"Machine learning"},
    {'label':"Analytical formulas"}]

    over_theme = {'txc_inactive': '#00000','menu_background':'white','txc_active': 'red', }
    menu_id = hc.nav_bar(
    menu_definition=menu_data,
    first_select= int(10),
    override_theme=over_theme,
    home_name='Home',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    )


    
    # start a file based on the selected tab in the navigationbar
    if menu_id == "Machine learning":
        ML_clinch.show_page()
    if menu_id == "Analytical formulas":
        Analytical_clinch.show_page()
    # go back to 'startscherm' when Home is selected
    if menu_id=='Home':
        return 3
    return 1