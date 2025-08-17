import streamlit as st
import mysql.connector

# Function to establish connection to MySQL database
def establish_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "aparna7024",
        "database": "loginconn",
        "port": 3306,
    }
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Function to fetch user information
def fetch_user_info(connection):
    user_info_query = "SELECT id, urname FROM users LIMIT 1"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(user_info_query)
        user_info = cursor.fetchone()
        return user_info
    except mysql.connector.Error as e:
        st.error(f"Error fetching user information: {e}")
        return None
    finally:
        cursor.close()


def close_connection(connection):
    if connection.is_connected():
        connection.close()


def fetch_questions(connection, table_name):
    fetch_query = f"SELECT * FROM {table_name}"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(fetch_query)
        questions = cursor.fetchall()
        return questions
    except mysql.connector.Error as e:
        st.error(f"Error fetching questions from table {table_name}: {e}")
        return None
    finally:
        cursor.close()


# Function to display the quiz page for a selected subject
def display_quiz(subject, username, user_id):
    st.title(f"Quiz for {subject}")
    st.write(f"Welcome {username} (ID: {user_id}) to the {subject} quiz!")
    st.write("Here you can attend the quiz for the selected subject.")

    # Establish connection to the database
    connection = establish_connection()
    if connection:
        # Fetch questions from the corresponding table based on the subject
        table_name = subject.lower()  # Assuming table names are lowercase and correspond to subject names
        questions = fetch_questions(connection, table_name)
        if questions:
            # Initialize session state for each question
            for q in questions:
                if f"question_{q['id']}" not in st.session_state:
                    st.session_state[f"question_{q['id']}"] = None

            question_index = st.session_state.get("question_index", 0)  # Get the question index from session state
            num_questions = len(questions)
            score = st.session_state.get("score", 0)  # Get the current score from session state

            if question_index < num_questions:
                q = questions[question_index]

                # Displaying the question and options as MCQ
                options = q['options'].split(',')
                user_answer = st.radio(
                    label=q['question_text'],
                    options=options,
                    key=f"question_{q['id']}"  # Use question ID as part of the key
                )

                # Add a button to navigate to the next question
                if st.button("Next"):
                    # Check if the user's answer is correct and update the score accordingly
                    if user_answer == q['correct_answer']:
                        score += 1
                        st.session_state["score"] = score  # Update the score in session state
                    question_index += 1  # Move to the next question
                    st.session_state["question_index"] = question_index  # Update the question index in session state
                    st.experimental_rerun()  # Rerun the script to display the next question

            else:
                # Show submit button after answering all questions
                if st.button("Submit"):
                    st.write(f"Your score: {score}/{num_questions}")

        else:
            st.error(f"No questions found for {subject}.")
        
        # Close the database connection
        close_connection(connection)
    else:
        st.error("Connection to database failed.")


# Function to calculate the score
def calculate_score(questions):
    score = 0
    for q in questions:
        user_answer = st.session_state[f"question_{q['id']}"]
        if user_answer == q['correct_answer']:
            score += 1
    return score

# Main function
def main():
    # Establish connection to the database
    connection = establish_connection()
    if connection:
        # Fetch user information
        user_info = fetch_user_info(connection)
        if user_info:
            username = user_info['urname']
            user_id = user_info['id']
            # Display the sidebar with username and ID
            st.sidebar.title("User Information")
            st.sidebar.write(f"Username: {username}")
            st.sidebar.write(f"User ID: {user_id}")

            # Display different subjects in the sidebar
            st.sidebar.title("Select Subject")
            subjects = ["Mathematics", "Python"]
            selected_subject = st.sidebar.selectbox("Choose the subject", subjects)

            # Reset session state when a new subject is selected
            if st.session_state.get("selected_subject") != selected_subject:
                st.session_state["selected_subject"] = selected_subject
                st.session_state["question_index"] = 0
                st.session_state["score"] = 0

            # Check if the user has selected a subject
            if selected_subject:
                display_quiz(selected_subject, username, user_id)  # Display the quiz page for the selected subject

        else:
            st.error("User information not found.")
        
        # Close the database connection
        close_connection(connection)
    else:
        st.error("Connection to database failed.")


if __name__ == "__main__":
    main()