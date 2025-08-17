# import streamlit as st
# import mysql.connector
# import re
# import subprocess  # Import the subprocess module

# class LoginPage:
#     admin_id = None
#     username= None
#     def __init__(self):
#         st.title("Login Page")
#         self.username = st.text_input("Username:")
#         self.password = st.text_input("Password:", type="password")
#         self.login_type = st.radio("Login as:", ["User", "Admin"])

#         login_button = st.button("Login")
#         if login_button:
#             self.login()

#     def validate_password(self):
#         if not re.search(r'[a-z]', self.password):
#             st.error("Password must contain at least one lowercase letter.")
#             return False
#         if not re.search(r'[A-Z]', self.password):
#             st.error("Password must contain at least one uppercase letter.")
#             return False     
#         if not re.search(r'\d', self.password):
#             st.error("Password must contain at least one digit.")
#             return False
#         if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
#             st.error("Password must contain at least one special character.")
#             return False
#         if len(self.password) < 8:
#             st.error("Password must be at least 8 characters long.")
#             return False
#         return True

#     def login(self):
#         if self.validate_password():
#             username = self.username
#             password = self.password
#             login_type = "user" if self.login_type == "User" else "admin"

#             try:
#                 db_config = {
#                     "host": "localhost",
#                     "user": "root",
#                     "password": "root",
#                     "database": "loginconn",
#                     "port": 3306,
#                 }

#                 connection = mysql.connector.connect(**db_config)
#                 cursor = connection.cursor()

#                 if login_type == 'user':
#                     # Assuming user_credentials is a predefined dictionary
#                     user_credentials = {'user1': 'Password1@', 'user2': 'password2'}
#                     if username in user_credentials and user_credentials[username] == password:
#                         query = "SELECT id FROM user WHERE username = %s"
#                         cursor.execute(query, (username,))
#                         user_id = cursor.fetchone()
#                         st.success(f"Login Successful! Welcome, {username} (User)!")
#                         ####self.load_admin_page()
#                     else:
#                         st.error("Login Failed. Invalid username or password.")

#                 elif login_type == 'admin':
#                     # Assuming admin_credentials is a predefined dictionary
#                     admin_credentials = {'admin': 'Adminpassword12@@'}
#                     if username in admin_credentials and admin_credentials[username] == password:
#                         query = "SELECT id FROM admin WHERE username = %s AND password = %s"
#                         cursor.execute(query, (username, password))
#                         result = cursor.fetchone()
#                         if result:
#                             self.admin_id = result[0]
#                             st.success(f"Admin Login Successful! Welcome, {username} (Admin)!")
#                             self.load_admin_page(LoginPage.username,self.admin_id)
#                         else:
#                             st.error("Admin Login Failed. Invalid username or password.")

#             except mysql.connector.Error as err:
#                 st.error(f"Error: {err}")

#             finally:
#                 if 'cursor' in locals():
#                     cursor.close()
#                 if 'connection' in locals():
#                     connection.close()
#         self.perform_database_operations(username,password,login_type)
#     def perform_database_operations(self, username, password, login_type):
#         db_config = {
#             "host": "localhost",
#             "user": "root",
#             "password": "root",
#             "database": "loginconn",
#             "port": 3306,
#         }

#         try:
           
#             connection = mysql.connector.connect(**db_config)
#             cursor = connection.cursor()

#             if login_type == "user":
#                 #user exists in the database
#                 query = "SELECT * FROM user WHERE username = %s AND password = %s"
#                 cursor.execute(query, (username, password))
#                 result = cursor.fetchone()
#             else:
#                 #admin exists in the database
#                 query = "SELECT * FROM admin WHERE username = %s AND password = %s"
#                 cursor.execute(query, (username, password))
#                 result = cursor.fetchone()
#                 st.write("admin username",result[0])
#                 st.write("admin username",result[1])
                
#         except mysql.connector.Error as err:
#             st.error(f"Error: {err}")

#         finally:
#             if 'cursor' in locals():
#                 cursor.close()
#             if 'connection' in locals():
#                 connection.close()
#     def load_admin_page(self, username, admin_id):
#         LoginPage.username = username
#         self.admin_id = admin_id  
#         subprocess.run(["streamlit", "run", "admin.py"])
#         # Exit the current Streamlit app
#         st.experimental_rerun()

# def main():
#     login_page = LoginPage()

# if __name__ == "__main__":
#     main()
import streamlit as st
import mysql.connector
import re

class LoginPage:
    username = None
    admin_id = None
    
    def __init__(self):
        st.title("Login Page")
        self.username = st.text_input("Username:")
        self.password = st.text_input("Password:", type="password")
        self.login_type = st.radio("Login as:", ["User", "Admin"])

        login_button = st.button("Login")
        if login_button:
            self.login()

    def validate_password(self):
        if not re.search(r'[a-z]', self.password):
            st.error("Password must contain at least one lowercase letter.")
            return False
        if not re.search(r'[A-Z]', self.password):
            st.error("Password must contain at least one uppercase letter.")
            return False     
        if not re.search(r'\d', self.password):
            st.error("Password must contain at least one digit.")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
            st.error("Password must contain at least one special character.")
            return False
        if len(self.password) < 8:
            st.error("Password must be at least 8 characters long.")
            return False
        return True

    def login(self):
        if self.validate_password():
            username = self.username
            password = self.password
            login_type = "user" if self.login_type == "User" else "admin"

            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "aparna7024",
                    "database": "loginconn",
                    "port": 3306,
                }

                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                if login_type == 'user':
                    query = "SELECT id FROM user WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    result = cursor.fetchone()
                    if result:
                        st.success(f"Login Successful! Welcome, {username} (User)!")
                    else:
                        st.error("Login Failed. Invalid username or password.")

                elif login_type == 'admin':
                    query = "SELECT id FROM admin WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    result = cursor.fetchone()
                    if result:
                        self.admin_id = result[0]
                        st.success(f"Admin Login Successful! Welcome, {username} (Admin)!")
                        # Call method to load admin page here
                    else:
                        st.error("Admin Login Failed. Invalid username or password.")

            except mysql.connector.Error as err:
                st.error(f"Error: {err}")

            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'connection' in locals():
                    connection.close()

    def perform_database_operations(self, username, password, login_type):
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "aparna7024",
            "database": "loginconn",
            "port": 3306,
        }

        try:
           
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            if login_type == "user":
                #user exists in the database
                query = "SELECT * FROM user WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
            else:
                #admin exists in the database
                query = "SELECT * FROM admin WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                st.write("admin username",result[0])
                st.write("admin username",result[1])
                
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


def main():
    login_page = LoginPage()

if __name__ == "__main__":
    main()
