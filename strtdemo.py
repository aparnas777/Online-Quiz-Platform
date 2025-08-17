import streamlit as st
import mysql.connector
import sys
import subprocess
import time

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

def display_quiz(subject):
    st.title(f"Quiz for {subject}")
    connection = establish_connection()
    if connection:
        table_name = subject.lower()
        questions = fetch_questions(connection, table_name)
        if questions:
            for q in questions:
                if f"question_{q['id']}" not in st.session_state:
                    st.session_state[f"question_{q['id']}"] = None

            question_index = st.session_state.get("question_index", 0)
            num_questions = len(questions)
            score = st.session_state.get("score", 0)

            if question_index < num_questions:
                q = questions[question_index]
                options = q['options'].split(',')
                user_answer = st.radio(
                    label=q['question_text'],
                    options=options,
                    key=f"question_{q['id']}"
                )
                start_time = time.time()  # Start the timer
                next_button_key = f"next_button_{question_index}"  # Unique key for the "Next" button
                if st.button("Next", key=next_button_key):  # Assign unique key to the "Next" button
                    if user_answer == q['correct_answer']:
                        score += 1
                        st.session_state["score"] = score
                    question_index += 1
                    st.session_state["question_index"] = question_index
                    st.experimental_rerun()
                    time.sleep(2)  # Delay to give time for the page to rerender
                else:
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 60:
                        st.warning("Time's up! Moving to the next question.")
                        question_index += 1
                        st.session_state["question_index"] = question_index
                        st.experimental_rerun()

            else:
                if st.button("Submit"):
                    st.write(f"Your score: {score}/{num_questions}")
                    
                    # Fetch past scores
                    past_scores = [70, 80, 90]  # Replace with actual past scores fetched from the database
                    avg_past_score = sum(past_scores) / len(past_scores)

                    # Compare current score with past scores
                    if score > avg_past_score:
                        st.success("Congratulations! You've beaten your average score.")
                    elif score == avg_past_score:
                        st.info("You've matched your average score.")
                    else:
                        st.warning("You've scored below your average score. Keep practicing!")

                    # Display leaderboard and statistics
                    st.subheader("Leaderboard")
                    st.write("Past Scores:")
                    for past_score in past_scores:
                        st.write(past_score)
                    st.write("Current Score:", score)
                    st.write("Average Past Score:", avg_past_score)
                    time.sleep(5)
                    subprocess.run(["streamlit", "run", "usdemo.py"])
                    st.experimental_rerun()

                    

        else:
            st.error(f"No questions found for {subject}.")

        close_connection(connection)
    else:
        st.error("Connection to database failed.")

def main():
    subject_index = sys.argv.index("subject") + 1
    subject=sys.argv[subject_index]
    display_quiz(subject)

if __name__ == "__main__":
    main()
