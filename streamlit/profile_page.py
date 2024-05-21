# profile_page.py
import streamlit as st
from db_management import get_user_data, get_latest_weight

def show_profile_page():
    if 'username' in st.session_state:
        username = st.session_state['username']
        user_data = get_user_data(username)
        latest_weight = get_latest_weight(username)
        
        if user_data:
            st.subheader("Profile Page")
            if user_data[7]:
                st.image(user_data[7], width=150, caption=username, use_column_width='auto', output_format='auto')
            else:
                st.write("No profile image available.")
            
            st.write(f"**Username:** {user_data[1]}")
            st.write(f"**First Name:** {user_data[3]}")
            st.write(f"**Last Name:** {user_data[4]}")
            st.write(f"**Age:** {user_data[5]}")
            st.write(f"**Sex:** {user_data[6]}")
            if latest_weight:
                st.write(f"**Current Weight:** {latest_weight} kg")
            else:
                st.write("**Current Weight:** Not available")
        else:
            st.warning("User data not found.")
    else:
        st.warning("You need to log in to view the profile.")
