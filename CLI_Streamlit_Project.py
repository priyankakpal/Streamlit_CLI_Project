import streamlit as st
from io import StringIO
import os
import pandas as pd
import shutil

st.sidebar.title("Menu")
menu_options = ["Home", "About", "Contact"]
selection = st.sidebar.radio("Choose a page", menu_options)

if selection == "Home":
    st.title("Welcome to the Home Page")
    st.write("This is the home page of the app.")
elif selection == "About":
    st.title("About Us")
    st.write("This page provides information about the app.")
elif selection == "Contact":
    st.title("Contact Us")
    st.write("You can contact us at contact@example.com.")

def Onclick_delete(location, files_to_display, selected_files):
    for file_name in selected_files:
        if file_name in files_to_display:
            del files_to_display[file_name]
            st.success(f"Deleted {file_name} successfully!")
    return files_to_display

def render_data(location, files_to_display):
    if files_to_display:
        st.write(f"Files found in the selected location: {location}")

        file_names = list(files_to_display.keys()) 
        selected_files = []

        for file_name in file_names:
            if st.checkbox(file_name, key=f"checkbox_{location}_{file_name}"):
                selected_files.append(file_name)

        if selected_files:
            delete_button = st.button(f"Delete selected files from {location}")

            if delete_button:
                st.session_state.files_to_display[location] = Onclick_delete(location, files_to_display, selected_files)
                st.rerun()
    else:
        st.write("No files found in the selected location.")


options = st.sidebar.multiselect(
    "Please select your source location",
    [r"C:\Users\PriyankaPal\Pictures", r"C:\Users\PriyankaPal\Documents", r"C:\Users\PriyankaPal\Documents\Success log",
     r"C:\Users\PriyankaPal\Downloads"]
)

if 'files_to_display' not in st.session_state:
    st.session_state.files_to_display = {}

if 'loaded_locations' not in st.session_state:
    st.session_state.loaded_locations = []

if options:
    for location in options:
        if location not in st.session_state.loaded_locations:
            if os.path.exists(location) and os.path.isdir(location):
                files = os.listdir(location)
                location_files = {}

                for file in files:
                    if file.endswith(('.csv', '.xlsx')):  
                        location_files[file] = location  

                if location_files:
                    st.session_state.files_to_display[location] = location_files

            st.session_state.loaded_locations.append(location)

    for location in options:
        if location in st.session_state.files_to_display:
            render_data(location, st.session_state.files_to_display[location])
else:
    st.write("No location selected.")


destination = st.sidebar.multiselect(
    "Please select the destination location",
    [r"C:\Users\PriyankaPal\Documents\Data_Archieve\Archieve", r"C:\Users\PriyankaPal\Documents\Data_Archieve\Copy_Data"]
)

archive_data = st.sidebar.button("Archivist")

print(st.session_state.files_to_display)

if archive_data: 
    try:
        if destination:
            for path_location in options:
                if os.path.exists(path_location):
                    data = st.session_state.files_to_display.values()
                    for i in data:
                        for keys, values in i.items():
                            if os.path.isdir(destination[0]) and keys in os.listdir(destination[0]):
                                st.success("File already exist on the location")
                            else:
                                shutil.copy(os.path.join(values,keys), destination[0])
        else:
            st.success("Destination not selected... Please select the destination.")
    except Exception as e:
            print(f"Error occurred while moving file: {e}")