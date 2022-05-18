import streamlit as st
import hydralit_components as hc
import text



def show_page():
    # Navigationbar
    over_theme = {'txc_inactive': '#00000','menu_background':'white','txc_active': 'red', }
    menu_id = hc.nav_bar(
    menu_definition=[{"label": ''}],
    first_select=int(10),
    override_theme=over_theme,
    home_name='Home',
    hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    )
    
    # informative text
    emptycol1, col,emptycol2 = st.columns([1,6,1])
    with col:
        text.intro()

    # go back to 'startscherm' when Home is selected
    if menu_id == "Home":
        return 3
    return 0