import io
import webbrowser

import streamlit as st
import requests
import json
import pickle
import shutil
import pandas as pd
import streamlit_theme

# List of valid credentials
users = {'admin': 'password', 'user1': 'pass1', 'user2': 'pass2'}
admin_accounts = {'admin': 'password'}
user_accounts = {'user1': 'pass1', 'user2': 'pass2'}
base_url = "http://localhost:3000"
headers = {"X-Metabase-Session": "8b9d9ed7-3bdb-4c53-998e-f08c802e5c3b"}
api_key = "8b9d9ed7-3bdb-4c53-998e-f08c802e5c3b"
admin = False

data = {"username": "lonaripratik6@gmail.com", "password": "Pratik123@99"}
st.set_page_config(page_title="Metabase Data Exploration and Analysis Tool", page_icon=":guardsman:",
                   initial_sidebar_state="auto")
st.title("Welcome to the Metabase API Explorer")
st.markdown("Our app addresses these concerns by providing a secure and user-friendly interface for managing access "
            "to tables and rows in a connected data"
            "source. With our app, administrators can easily create and manage user accounts, assign different levels "
            "of access to specific tables and rows, and monitor user activity to ensure compliance with data security "
            "policies."
            "The app's intuitive interface and powerful security features make it the ideal solution "
            "for organizations looking to protect sensitive data while still allowing authorized users to access the "
            "information they need."
            "Whether you're a small business or a large enterprise, our app is designed to meet your data security "
            "needs.")


def save_accounts():
    with open("admin_accounts.pkl", "wb") as f:
        pickle.dump(admin_accounts, f)
    with open("user_accounts.pkl", "wb") as f:
        pickle.dump(user_accounts, f)


def load_accounts():
    global admin_accounts, user_accounts
    try:
        with open("admin_accounts.pkl", "rb") as f:
            admin_accounts = pickle.load(f)
        with open("user_accounts.pkl", "rb") as f:
            user_accounts = pickle.load(f)
    except FileNotFoundError:
        pass


i = 1


def login():
    error = None
    username = st.text_input("Username", key="i+23")
    password = st.text_input("Password", type='password', key="i+1")
    logi = st.button("Submit", key='submit_btn1')
    if "log_state" not in st.session_state:
        st.session_state.log_state = False

    if logi or st.session_state.log_state:
        st.session_state.log_state = True
        if username in admin_accounts:
            if password == admin_accounts[username]:
                # Login successful
                global admin
                st.success("Welcome, " + username)
                admin = True
                return True
            else:
                error = 'Invalid password'
                st.error(error)
                return False
        elif username in user_accounts:
            if password == user_accounts[username]:
                # Login successful
                st.success("Welcome, " + username)

                return True
            else:
                error = 'Invalid password'
                st.error(error)
                return False
        else:
            error = 'Invalid username'
            st.error(error)
            return False


def register():
    username = st.text_input("Username", key="i+2")
    password = st.text_input("Password", type='password', key="i+3")
    account_type = st.selectbox("Select account type", ["admin", "user"])
    reg = st.button("Submit")
    if "reg_state" not in st.session_state:
        st.session_state.reg_state = False

    if reg or st.session_state.reg_state:
        st.session_state.reg_state = True
        if account_type == "admin" and username in admin_accounts:
            st.error("Username already taken.")
        elif account_type == "user" and username in user_accounts:
            st.error("Username already taken.")
        else:
            if account_type == "admin":
                admin_accounts[username] = password
                st.success("Successfully registered as an admin.")
            else:
                user_accounts[username] = password
                st.success("Successfully registered as a user.")
        save_accounts()


load_accounts()


def fetch_databases():
    response = requests.post("http://localhost:3000/api/session", data=json.dumps(data), headers=headers)

    params = {"include": "tables", "saved": "true", "include_editable_data_model": "false",
              "exclude_uneditable_details": "true"}
    response = requests.get("http://localhost:3000/api/database/", headers=headers, params=params)
    st.write(response.json())


def hide_tables(selected_tables):
    st.success("Successful")
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://localhost:3000/api/session", data=json.dumps(data), headers=headers)

    # Fetch a specific database
    database_id = 8
    headers = {"X-Metabase-Session": "8b9d9ed7-3bdb-4c53-998e-f08c802e5c3b"}

    if not selected_tables:
        st.warning("Please select at least one table to hide.")
        return
        # Get the IDs of the selected tables
    response = requests.get("{}/api/table/".format(base_url), headers=headers, auth=('api_key', api_key))
    tables = response.json()
    selected_table_ids = [table["id"] for table in tables if table["name"] in selected_tables]
    table_data = {"visibility_type": "hidden"}
    for i in selected_table_ids:
        response = requests.put("http://localhost:3000/api/table/{}".format(i), headers=headers,
                                json=table_data,
                                auth=('api_key', api_key))

    if response.status_code != 200:
        st.warning("An error occurred while hiding tables")
    else:
        st.success("Tables hidden successfully")


def metadata(table_id):
    params = {
        "include_sensitive_fields": "true",
        "include_hidden_fields": "true",
        "include_editable_data_model": "true"
    }

    if st.button('Fetch Table Metadata'):
        response = requests.get("{}/api/table/{}/query_metadata".format(base_url, table_id), headers=headers,
                                params=params,
                                auth=('api_key', api_key))
        if response.status_code != 200:
            st.error("Failed to retrieve query metadata for table {}. Error: {}".format(table_id, response.text))
        else:
            data = json.dumps(response.json())
            file_path = "table{}.json".format(table_id)

            with open(file_path, "w") as f:
                f.write(data)
            webbrowser.open(file_path)


def metadata_users(table_id):
    headers = {"X-Metabase-Session": "8b9d9ed7-3bdb-4c53-998e-f08c802e5c3b"}
    params = {
        "include_sensitive_fields": "false",
        "include_hidden_fields": "false",
        "include_editable_data_model": "false"
    }

    if st.button('Fetch Table Metadata'):
        response = requests.get("{}/api/table/{}/query_metadata".format(base_url, table_id), headers=headers,
                                params=params,
                                auth=('api_key', api_key))
        if response.status_code != 200:
            st.error("Failed to retrieve query metadata for table {}. Error: {}".format(table_id, response.text))
        else:
            data = json.dumps(response.json())
            file_path = "table{}{}.json".format(table_id, users)

            with open(file_path, "w") as f:
                f.write(data)
            webbrowser.open(file_path)


def test(card):
    export_format = "csv"
    query = {
        "database": 2,
        "type": "native",
        "native": {
            "query": "SELECT * FROM table",
            "limit": 100
        }
    }
    payload = json.dumps({"parameters": {"query": query}})

    response = requests.post("http://localhost:3000/api/card/{}/query/{}".format(card, export_format), headers=headers,
                             data=payload)
    if st.button('Fetch Dataset'):
        if response.status_code == 200:
            with open("export_{}.{}".format(card, export_format), 'wb') as f:
                f.write(response.content)
            # st.success(f"Data exported to export_{card}.{export_format}")
            df = pd.read_csv("export_{}.{}".format(card, export_format))

            # Limit number of rows to 100
            df = df.head(20)

            # Save the limited data to a new CSV file
            df.to_csv("export_{}_limited.{}".format(card, export_format), index=False)
            df = pd.read_csv("export_{}_limited.{}".format(card, export_format))

            # Display the DataFrame in a Streamlit table
            st.dataframe(df)

        else:
            st.error("Error occurred while exporting data")



def main():
    st.title("Login/Register")
    app_mode = st.selectbox("Select mode", ["Login", "Registration"])
    if app_mode == "Login":

        # if login():
        #     de = st.button("Delete")
        #     if "del_state" not in st.session_state:
        #         st.session_state.del_state = False
        #
        #     if de or st.session_state.del_state:
        #         st.session_state.del_state = True
        #         hide_tables(1)
        #         st.success("Done!!!!!!!!!")
        if login():
            if admin:
                response = requests.get("{}/api/table/".format(base_url), headers=headers, auth=('api_key', api_key))
                tables = response.json()
                table_names = [table["name"] for table in tables]
                st.write("If you want to hide specific tables, select from the multiselect option :")
                s1 = "Select tables to hide"
                selected_tables = st.multiselect("**{}**".format(s1), table_names)
                if "multi" not in st.session_state:
                    st.session_state.multi = False
                if selected_tables or st.session_state.multi:
                    st.session_state.multi = True
                    if st.button("Submit"):
                        if selected_tables:
                            hide_tables(selected_tables)
                    else:
                        st.warning("Please select at least one table to hide.")
                st.write("")
                st.write("")
                st.write("To fetch Meta Data of a specific table :")
                st.write("Meta Data")
                idx = st.number_input("Enter the table ID", min_value=1, max_value=8)
                if "idx_state" not in st.session_state:
                    st.session_state.idx_state = False
                if idx or st.session_state.idx_state:
                    st.session_state.idx_state = True
                    metadata(idx)
                st.write("")
                st.write("")
                st.write("To go the database (As visible to normal users)")
                button = st.button('Go to Database(Users)')
                if "but_state" not in st.session_state:
                    st.session_state.but_state = False

                if button or st.session_state.but_state:
                    st.session_state.but_state = True
                    st.markdown(
                        "<a href='http://localhost:3000/browse/1-sample-database' target='_blank'>Database Link</a>",
                        unsafe_allow_html=True)
                st.write("")
                st.write("")
                st.write("To go the admin dashboard for the Metabase :")
                button1 = st.button('Go to Admin Dashboard')
                if "but1_state" not in st.session_state:
                    st.session_state.but1_state = False

                if button1 or st.session_state.but1_state:
                    st.session_state.but1_state = True
                    st.markdown(
                        "<a href='http://localhost:3000/admin/settings/setup' target='_blank'>Admin Dashboard</a>",
                        unsafe_allow_html=True)
            else:
                st.write("To get the Data Table by table id :")
                st.write("Data Table")
                idx1 = st.number_input("Enter the table ID", min_value=1, max_value=8, key="124")
                if "idx_state1" not in st.session_state:
                    st.session_state.idx_state1 = False
                if idx1 or st.session_state.idx_state1:
                    st.session_state.idx_state1 = True
                    test(idx1)
                st.write("")
                st.write("")
                st.write("To get the meta data of the entire Database")
                button2 = st.button("Get Database Meta Data")
                if 'but2_state' not in st.session_state:
                    st.session_state.but2_state = False
                if button2 or st.session_state.but2_state:
                    st.session_state.but2_state = True
                    fetch_databases()
                st.write("")
                st.write("")
                st.write("To get the Metadata of a specific table")
                st.write("Meta Data")
                idx = st.number_input("Enter the table ID", min_value=1, max_value=8, key="1234")
                if "idx_state" not in st.session_state:
                    st.session_state.idx_state = False
                if idx or st.session_state.idx_state:
                    st.session_state.idx_state = True
                    metadata_users(idx)
                st.write("")
                st.write("")
                st.write("To go to the Metabase database :")
                button = st.button('Go to Database')
                if "but_state" not in st.session_state:
                    st.session_state.but_state = False

                if button or st.session_state.but_state:
                    st.session_state.but_state = True
                    st.markdown(
                        "<a href='http://localhost:3000/browse/1-sample-database' target='_blank'>Database Link</a>",
                        unsafe_allow_html=True)
    else:
        register()


if __name__ == '__main__':
    main()
   # fetch_databases()
# test()
