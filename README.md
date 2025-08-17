This Python-based quiz application, built using the **Streamlit** framework, provides a comprehensive system for administering and managing quizzes. It features distinct interfaces for both **users** and **admins**, and integrates with a **MySQL database** to store and retrieve quiz questions and user data. The application is composed of several Python scripts, each handling a specific part of the functionality.

***

### Key Features and Functionality

* **User Authentication**: The `loginstream.py` script handles user and admin logins. It validates passwords based on a predefined set of rules, including checks for length, and the presence of uppercase, lowercase, special characters, and digits. After successful authentication, it redirects the user to the appropriate page (`usdemo.py` for users or `admin.py` for admins) using `subprocess.run` to execute another Streamlit script.

* **User Interface (`home.py`, `usdemo.py`, `user.py`)**:
    * The `home.py` file serves as the landing page, welcoming users and providing instructions before they log in.
    * The `usdemo.py` script allows users to select a quiz subject, such as **Mathematics** or **Python**.
    * The `user.py` script displays the quiz questions for the selected subject. It retrieves questions from the MySQL database and presents them as multiple-choice questions. It keeps track of the user's score and provides navigation to the next question.

* **Admin Interface (`admin.py`, `questions.py`)**:
    * The `admin.py` script, accessible only after a successful admin login, provides options to manage quiz subjects. It allows an administrator to select a subject to add, view, or delete questions.
    * The `questions.py` script is the core of the admin management system. It provides a user interface for:
        * **Adding Questions**: Admins can input a question, a list of comma-separated options, the correct answer, and a time duration. This data is then inserted into the corresponding subject's table in the database.
        * **Viewing Questions**: Admins can view all the questions stored for a particular subject.
        * **Deleting Questions**: Admins can delete a question by its ID.

***

### Database Interaction

The application uses the `mysql.connector` library to interact with a MySQL database named `loginconn`. The `establish_connection()` function, present in several scripts, handles the connection setup using a configuration that includes the host, user, password, database name, and port. This allows different parts of the application to perform database operations, such as inserting, deleting, and fetching questions, as well as authenticating users and admins.

### Inter-Script Communication

The application uses subprocess.run to call and run other Streamlit scripts, effectively navigating between different pages (e.g., from the login page to the admin page). It passes information, such as the username, admin_id, and subject, as command-line arguments, which the receiving script then parses using sys.argv. This method allows for a modular design where each script handles a specific task, while maintaining state and context across different pages.
The application uses `subprocess.run` to call and run other Streamlit scripts, effectively navigating between different pages (e.g., from the login page to the admin page). It passes information, such as the `username`, `admin_id`, and `subject`, as command-line arguments, which the receiving script then parses using `sys.argv`. This method allows for a modular design where each script handles a specific task, while maintaining state and context across different pages.
