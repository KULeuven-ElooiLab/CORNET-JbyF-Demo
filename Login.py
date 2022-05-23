import streamlit as st


def show_page():
    emptycol1, col, emptycol2 =st.columns([1,0.5,1])
    
    username = col.text_input('Username')
    password = col.text_input('Password',type='password')
    if col.button("Log in"):
        if username =='JbyF' and password == "Cornet":
            return 3
        else:
            col.warning("Username or password is not correct.")
    col.write('''username: JbyF 
    \n password: Cornet''')
    return 4
