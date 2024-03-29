# Instructions for using the Metabase API Explorer web app

1. Install all the dependencies given in the requirements.txt file and run the streamlit app
2. Make sure your Metabase app is running on http://localhost:3000/
3. To log in, enter your username and password in the designated fields and click the "Submit" button.
   - If you do not have an account, click the "Register" button to create a new account.
   - In the registration form, enter your desired username and password, select your account type (admin or user), and click the "Submit" button.

# Admin
1. Admin can remove various tables in the dataset by selecting them from the multi-select box.
2. Admins can analyse the Metadata of various tables without any restriction.
   - To get Metadata for a particular data, You can select table ID and press "Fetch Metadata" 
3. Admins can see what tables are the users seeing, by going to the Database(User)
4. Admin can go to the admin dashboard.

# User
1. Users can view the database by clicking on the "Go the database" button.
2. Users can also Fetch the Metadata, but cannot access sensitive, hidden and editable data model.

# Metabase Login

- (If you want to use your credentials, update the keys and values accordingly!)

![Web-application](https://github.com/ptk-39005/Metabase-API-Explorer-Team-title-/blob/0a2da4e5062ea4cfbb2c0e1ec38a2d6b7fc6a32d/Screenshot%20from%202023-01-21%2022-09-38.png)

