import mysql.connector
from mysql.connector import Error
from datetime import datetime
import streamlit as st
from loginstream import LoginPage  # Make sure you import the correct module

global admin_id
admin_id = LoginPage.admin_id
global quiz_id


def establish_connection():
    # Establish connection to MySQL database
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "loginconn",
        "port": 3306,
    }

    connection = mysql.connector.connect(**db_config)
    return connection


def close_connection(connection):
    # Close the MySQL connection
    if connection.is_connected():
        connection.close()


def admin_login(username, password):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)

        # Check if the provided credentials match an admin in the database
        query = "SELECT id, admin_name FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        close_connection(connection)


def insert_quiz(quiz_name, start_time, end_time, admin_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Insert quiz into the quiz table
        cursor.execute("""
        INSERT INTO quiz (quiz_name, start_time, end_time, admin_id)
        VALUES (%s, %s, %s, %s)
        """, (quiz_name, start_time, end_time, admin_id))

        connection.commit()

        # Fetch the quiz_id after inserting the quiz
        query = "SELECT LAST_INSERT_ID() as quiz_id"
        cursor.execute(query)
        quiz_id_result = cursor.fetchone()
        quiz_id = quiz_id_result['quiz_id'] if quiz_id_result else None
        return quiz_id

    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)


def get_latest_quiz_id(admin_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch the latest quiz_id for the given admin_id
        query = "SELECT MAX(quiz_id) AS latest_quiz_id FROM quiz WHERE admin_id = %s"
        cursor.execute(query, (admin_id,))
        result = cursor.fetchone()

        latest_quiz_id = result["latest_quiz_id"] if result and result["latest_quiz_id"] is not None else 0

        return latest_quiz_id + 1  # Increment to get the next available quiz_id

    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)

def insert_question(question_text, options, correct_answer, duration, quiz_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Insert question into the questions table
        cursor.execute("""
        INSERT INTO questions (question_text, options, correct_answer, duration, quiz_id)
        VALUES (%s, %s, %s, %s, %s)
        """, (question_text, options, correct_answer, duration, quiz_id))

        connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)

def start_quiz(quiz_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Update the quiz status or record the start time
        cursor.execute("""
        UPDATE quiz
        SET status = 'started', start_time = NOW()
        WHERE quiz_id = %s
        """, (quiz_id,))

        # Fetch the end_time separately using a SELECT statement
        cursor.execute("""
        SELECT end_time FROM quiz
        WHERE quiz_id = %s
        """, (quiz_id,))
        
        end_time_result = cursor.fetchone()

        if end_time_result is not None:
            end_time = end_time_result[0]
        else:
        # Handle the case where end_time is not available
            end_time = None  # or raise an exception, print a warning, etc. 
            current_time = datetime.now()

        if current_time > end_time:
            # Update the quiz status to indicate it has ended
            cursor.execute("""
            UPDATE quiz
            SET status = 'ended'
            WHERE quiz_id = %s
            """, (quiz_id,))

            connection.commit()
            print("Quiz has ended!")
    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)

def view_questions(quiz_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch questions for a specific quiz_id
        query = "SELECT * FROM questions WHERE quiz_id = %s"
        cursor.execute(query, (quiz_id,))
        questions = cursor.fetchall()

        if questions:
            st.table(questions)
        else:
            st.warning("No questions found for the selected quiz.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)

def delete_question(question_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor()

        # Delete question with a specific question_id
        query = "DELETE FROM questions WHERE question_id = %s"
        cursor.execute(query, (question_id,))
        connection.commit()

        st.success("Question deleted successfully!")

    except Error as e:
        print(f"Error: {e}")
        st.error("Error deleting question.")

    finally:
        close_connection(connection)

def get_all_quizzes(admin_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all quizzes from the quiz table
        query = "SELECT * FROM quiz"
        cursor.execute(query)
        result = cursor.fetchall()

        return result

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        close_connection(connection)

def view_quiz(quiz_id):
    try:
        connection = establish_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch information about a specific quiz based on quiz_id
        query = "SELECT * FROM quiz WHERE quiz_id = %s"
        cursor.execute(query, (quiz_id,))
        result = cursor.fetchone()

        if result:
            st.write(f"Quiz ID: {result['quiz_id']}")
            st.write(f"Quiz Name: {result['quiz_name']}")
            st.write(f"Start Time: {result['start_time']}")
            st.write(f"End Time: {result['end_time']}")
            st.write(f"Admin ID: {result['admin_id']}")
            st.write(f"Status: {result['status']}")

        else:
            st.write(f"No quiz found with quiz_id: {quiz_id}")

    except Error as e:
        print(f"Error: {e}")

    finally:
        close_connection(connection)
