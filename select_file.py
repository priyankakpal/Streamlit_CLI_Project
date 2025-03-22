import streamlit as st
import os
import shutil
import pandas as pd

# Create a placeholder for top messages
message_placeholder = st.empty()

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

if 'updated_files_to_display' not in st.session_state:
    st.session_state.updated_files_to_display = {}

def Onclick_select(location, files_to_display, selected_files):
    location_files = {}
    for file_name in selected_files:
        if file_name not in st.session_state.updated_files_to_display:
            try:
                location_files[file_name] = location
            except Exception as e:
                st.error(f"Error deleting {file_name}: {e}")

    if location_files:
        st.session_state.updated_files_to_display[location] = location_files

    return st.session_state.updated_files_to_display


def render_data(location, files_to_display):
    file_name_list = list(files_to_display.keys())

    data = {'file_name': file_name_list}
    df = pd.DataFrame(data)

    df['Select'] = False  

    cols = ['Select'] + list(df.columns[:-1])
    df = df[cols]

    st.write(f"file from {location}")
    
    select_all = st.checkbox("Select All", key="select_all")

    if select_all:
        df['Select'] = True
    else:
        df['Select'] = False
    
    edited_df = st.data_editor(df, hide_index=True) 

    if edited_df is not None:  
        selected_files = edited_df[edited_df['Select']]['file_name'].tolist()

        if selected_files:
            selected_button = st.button(f"Submit the selected files")
            if selected_button:
                st.session_state.updated_files_to_display = Onclick_select(location, files_to_display, selected_files)
                st.session_state.files_to_display.update(st.session_state.updated_files_to_display)


options = st.sidebar.selectbox(
    "Please select your source location",
    [r"C:\Users\PriyankaPal\Pictures", r"C:\Users\PriyankaPal\Documents", r"C:\Users\PriyankaPal\Documents\Success log",
     r"C:\Users\PriyankaPal\Downloads"]
)


if 'files_to_display' not in st.session_state:
    st.session_state.files_to_display = {}

if 'loaded_locations' not in st.session_state:
    st.session_state.loaded_locations = []

if options:
    if options not in st.session_state.loaded_locations:
        if os.path.exists(options) and os.path.isdir(options):
            files = os.listdir(options)
            if len(files)>0:
                location_files = {}

                for file in files:
                    if file.endswith(('.csv', '.xlsx')):
                        location_files[file] = options  

                if location_files:
                    st.session_state.files_to_display[options] = location_files
            else:
                message_placeholder.error("File not present at the location")
                
        st.session_state.loaded_locations.append(options)
    
    if options in st.session_state.files_to_display:
        render_data(options, st.session_state.files_to_display[options])

else:
    st.write("No location selected.")


destination = st.sidebar.selectbox(
    "Please select the destination location",
    [r"C:\Users\PriyankaPal\Documents\Data_Archieve\Archieve", r"C:\Users\PriyankaPal\Documents\Data_Archieve\Copy_Data"]
)

archive_data = st.sidebar.button("Archivist")

# Show success or warning at the top based on actions
if archive_data:
    try:
        if destination:
            if options:
                if os.path.exists(options):
                    for file_name, location in st.session_state.files_to_display.get(options, {}).items():
                        dest_path = destination
                        if os.path.isdir(dest_path) and file_name in os.listdir(dest_path):
                            # Use the placeholder to show the warning message at the top
                            message_placeholder.warning(f"File already exists at the destination.")
                        else:
                            shutil.copy(os.path.join(location, file_name), dest_path)
                            # Show success message at the top
                            message_placeholder.success(f"File archived successfully!")

        else:
            message_placeholder.warning("No destination selected... Please select the destination.")
    except Exception as e:
        message_placeholder.error(f"Error occurred while archiving files: {e}")