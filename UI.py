import streamlit as st
import pandas as pd
import openai
import random
import json
from PIL import Image
import toml
import os

st.set_page_config(layout="wide", page_title="Chegg IntelliPlay", page_icon="🎮")

openai.api_key = st.secrets.KEY.api_key

subject_mappings = {2: "Physics",
3: "Computer Science",
4: "Electrical Engineering",
5: "Mechanical Engineering",
6: "Chemistry",
7: "Algebra",
8: "Calculus",
9: "Statistics and Probability",
10: "Advanced Math",
12: "Other Math",
13: "Biology",
14: "Civil Engineering",
18: "Finance",
19: "Economics",
20: "Accounting",
26: "Poetry",
27: "Literature",
33: "American History",
34: "European History",
35: "World History",
39: "Psychology",
40: "Sociology",
41: "Anthropology",
42: "Political Science",
43: "International Relations",
45: "Other",
46: "Prewriting",
47: "Postwriting",
48: "Geometry",
49: "Trigonometry",
50: "Prealgebra",
51: "Precalculus",
52: "Philosophy",
53: "Operations Management",
54: "Communications",
55: "Earth Sciences",
56: "Advanced Physics",
57: "Chemical Engineering",
58: "Nursing",
59: "Anatomy and Physiology"}

def chatWithGPT(prompt):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
  {"role": "user", "content": prompt}
  ]
  )
  return completion.choices[0].message.content

def generate_question():
    response = chatWithGPT(
        "Generate 10 different multiple-choice questions, each with 4 options. The questions should cover various topics from the selected subjects: "
        + str(st.session_state['subject_list'])
        + ". Set the difficulty level to "
        + st.session_state['difficulty']
        + ". Return the output in a dictionary format, where each question is a key, and the corresponding value is a tuple containing the options and the correct answer."
        + "Return only the dictionary in the output and nothing else."
        + "Do not return a sample output. Generate real questions."
    )
    return response
    

def page_name_input():
    st.title("Welcome to Chegg IntelliPlay!")
    st.header("Enter Your Name", anchor="center")
    name = st.text_input("Name")
    # Ask whether the user is a member or not
    member_sub = st.subheader("Are you a member or a subscriber?")
    member = member_sub.radio("", ["Member", "Subscriber"])

    if member == "Subscriber":
        subscription_code = st.text_input("Enter your Subscription email ID")
        # If the subscription code is correct, welcome the user
        if subscription_code == "aabrol@chegg.com":
            st.write("Welcome", name)
            if st.button("Next"):
                st.session_state['name'] = name
                st.session_state['subscription_code'] = subscription_code
                st.session_state['member'] = member
                st.experimental_rerun()
        # If the subscription code is incorrect, tell the user that the code is incorrect
        else:
            st.write("Incorrect Subscription email. Please try again with a valid Subscription email ID or subscribe to Chegg to play as a Subscriber.")
            if st.button("Subscribe"):
                st.session_state.clear()
                st.experimental_rerun()
    elif member == "Member":
        st.write("Welcome", name)
        if st.button("Next"):
            st.session_state['name'] = name
            st.session_state['member'] = member
            st.experimental_rerun()

def page_subject_difficulty():
    st.title("Chegg IntelliPlay")
    st.header("Select Subject and Difficulty", anchor="center")
    subject_list = st.multiselect("Pick your favourite subjects (Maximum: 5)", list(subject_mappings.values()), max_selections=5)
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    if st.button("Start Quiz"):
        st.session_state['subject_list'] = subject_list
        st.session_state['difficulty'] = difficulty
        st.experimental_rerun()

def page_quiz_question():
    # Generate question using OpenAI GPT-3.5 Turbo and display it
    questions_and_options_dict = generate_question()    
    
    # Convert the string to a dictionary
    try:
        questions_and_options_dict = eval(questions_and_options_dict)
        print(questions_and_options_dict)
    except:
        st.write("Please wait!! We are generating the questions for you.")
        st.experimental_rerun()

    st.session_state['questions_and_options_dict'] = questions_and_options_dict
    st.session_state['score'] = 0
    st.session_state['total_questions'] = 0
    st.experimental_rerun()
    
def page_question_change():
    st.title("Chegg IntelliPlay")
    st.header(f"Welcome, {st.session_state['name']}!")
    st.write("Instructions: Answer the following multiple-choice questions and earn rewards after finishing the quiz.")
    if st.session_state['total_questions'] == 0:
        if st.session_state['member'] == "Member":
            st.info("Showing Question 1 of 3")
        elif st.session_state['member'] == "Subscriber":
            st.info("Showing Question 1 of 5")
        question1 = st.subheader("Question 1")
        question1.write(list(st.session_state['questions_and_options_dict'].keys())[0])
        # options1 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[0][0])
        options1 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[0][0])
        if st.button("Next"):
            st.session_state['total_questions'] += 1
            if options1 == list(st.session_state['questions_and_options_dict'].values())[0][1]:
                st.session_state['score'] += 1
            st.session_state['options1'] = options1
            st.experimental_rerun()

    if st.session_state['total_questions'] == 1:
        if st.session_state['member'] == "Member":
            st.info("Showing Question 2 of 3")
        elif st.session_state['member'] == "Subscriber":
            st.info("Showing Question 2 of 5")
        question2 = st.subheader("Question 2")
        question2.write(list(st.session_state['questions_and_options_dict'].keys())[1])
        # options2 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[1][0])
        options2 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[1][0])
        if st.button("Next"):
            st.session_state['total_questions'] += 1
            if options2 == list(st.session_state['questions_and_options_dict'].values())[1][1]:
                st.session_state['score'] += 1
            st.session_state['options2'] = options2
            st.experimental_rerun()

    elif st.session_state['total_questions'] == 2:
        if st.session_state['member'] == "Member":
            st.info("Showing Question 3 of 3")
        elif st.session_state['member'] == "Subscriber":
            st.info("Showing Question 3 of 5")
        question3 = st.subheader("Question 3")
        question3.write(list(st.session_state['questions_and_options_dict'].keys())[2])
        # options3 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[2][0])
        options3 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[2][0])
        if st.button("Next"):
            st.session_state['total_questions'] += 1
            if options3 == list(st.session_state['questions_and_options_dict'].values())[2][1]:
                st.session_state['score'] += 1
            st.session_state['options3'] = options3
            st.experimental_rerun()

    elif st.session_state['total_questions'] == 3:
        st.info("Showing Question 4 of 5")
        question4 = st.subheader("Question 4")
        question4.write(list(st.session_state['questions_and_options_dict'].keys())[3])
        # options4 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[3][0])
        options4 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[3][0])
        if st.button("Next"):
            st.session_state['total_questions'] += 1
            if options4 == list(st.session_state['questions_and_options_dict'].values())[3][1]:
                st.session_state['score'] += 1
            st.session_state['options4'] = options4
            st.experimental_rerun()

    elif st.session_state['total_questions'] == 4:
        st.info("Showing Question 5 of 5")
        question5 = st.subheader("Question 5")
        question5.write(list(st.session_state['questions_and_options_dict'].keys())[4])
        # options5 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[4][0])
        options5 = st.radio("Options", list(st.session_state['questions_and_options_dict'].values())[4][0])
        if st.button("Submit Quiz"):
            st.session_state['total_questions'] += 1
            if options5 == list(st.session_state['questions_and_options_dict'].values())[4][1]:
                st.session_state['score'] += 1
            st.session_state['options5'] = options5
            st.experimental_rerun()

def page_question_details():
    st.header(f"Welcome, {st.session_state['name']}!")
    st.write("Your score is:", st.session_state['score'])
    st.write("The questions with their options and correct answers are:")

    st.markdown("1. " + list(st.session_state['questions_and_options_dict'].keys())[0])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[0][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[0][1]))
    st.markdown("Your Answer: " + st.session_state['options1'])

    st.markdown("2. " + list(st.session_state['questions_and_options_dict'].keys())[1])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[1][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[1][1]))
    st.markdown("Your Answer: " + st.session_state['options2'])

    st.markdown("3. " + list(st.session_state['questions_and_options_dict'].keys())[2])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[2][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[2][1]))
    st.markdown("Your Answer: " + st.session_state['options3'])

    st.markdown("4. " + list(st.session_state['questions_and_options_dict'].keys())[3])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[3][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[3][1]))
    st.markdown("Your Answer: " + st.session_state['options4'])

    st.markdown("5. " + list(st.session_state['questions_and_options_dict'].keys())[4])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[4][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[4][1]))
    st.markdown("Your Answer: " + st.session_state['options5'])

    if st.button("View earned rewards"):
        st.session_state['visited'] = True
        st.experimental_rerun()
    

def page_question_details_member():
    st.header(f"Welcome, {st.session_state['name']}!")
    st.write("Your score is:", st.session_state['score'])
    st.write("The questions with their options and correct answers are:")

    st.markdown("1. " + list(st.session_state['questions_and_options_dict'].keys())[0])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[0][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[0][1]))
    st.markdown("Your Answer: " + st.session_state['options1'])

    st.markdown("2. " + list(st.session_state['questions_and_options_dict'].keys())[1])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[1][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[1][1]))
    st.markdown("Your Answer: " + st.session_state['options2'])

    st.markdown("3. " + list(st.session_state['questions_and_options_dict'].keys())[2])
    st.markdown("Options: " + str(list(st.session_state['questions_and_options_dict'].values())[2][0]))
    st.markdown("Correct Answer: " + str(list(st.session_state['questions_and_options_dict'].values())[2][1]))
    st.markdown("Your Answer: " + st.session_state['options3'])

    st.write("To view more questions, please subscribe to Chegg.")

    if st.button("View earned rewards"):
        st.session_state['visited'] = True
        st.experimental_rerun()
    if st.button("Subscribe"):
        st.session_state.clear()
        st.stop()
    
def page_rewards():
    st.session_state['reward_points'] = st.session_state['score'] * 20
    reward_points = st.session_state['score'] * 20
    if st.session_state['score'] > 0:
        st.balloons()
        st.header(f"Congratulations, {st.session_state['name']}!")
        st.write("You have earned", reward_points, "reward points for correctly answering", st.session_state['score'], "questions.")
    else:
        st.write("Thanks for playing, ", st.session_state['name'], "!")
        st.write("Play again and earn reward points for correctly answering questions.")
    if st.button("Play Again"):
        st.session_state.clear()
        st.experimental_rerun()
    if st.button("Quit"):
        st.session_state.clear()
        st.stop()
    
    if st.session_state['member'] == "Subscriber":
        st.info("As a valued User, we appreciate your active participation \n This is designed to help you with prepration and award you with rewards!")
    else:
        st.info("Not interested in playing again? \n Explore Chegg's vast educational resources on our website \n [Visit Chegg](https://www.chegg.com)")


    if st.session_state['member'] == 'Subscriber':
        st.info("Explore Chegg's vast collection of eTextbooks related to the topic of the question asked in the quiz \n [Chegg Textbooks Link](https://www.chegg.com/etextbooks)")
        st.info("Feeling down or need mental health support? Chegg cares about your well-being. Find helpful resources and information in our Mental Health section: \n [Mental Health Resources](https://www.chegg.com/life)")
    else:
        st.info("After joining us , you can explore vast categories of resources availiable related to the topics asked in the quiz: \n [Chegg Textbooks](https://www.chegg.com/etextbooks)\n If you have any questions or need assistance, our support team is here to help: \n [Contact Support](mailto:support@example.com)")
        st.info("Feeling down or need mental health support? Chegg cares about your well-being. Find helpful resources and information in our Mental Health section: \n [Mental Health Resources](https://www.chegg.com/life)")

def main():

    st.markdown(
    """
    <style>
    body {
        background-color: #ffffff; /* Set the background color to white */
        color: #eb7100; /* Set the text color to Chegg's orange color */
    }
    .stButton button {
        background-color: #ff8a00; /* Set the button background color to Chegg's orange color */
        color: #ffffff; /* Set the button text color to white */
    }
    </style>
    """,
    unsafe_allow_html=True)

    image = Image.open('assets/header.png')
    st.image(image, use_column_width=True)
    if 'name' not in st.session_state:
        page_name_input()
    elif 'subject_list' not in st.session_state:
        page_subject_difficulty()
    elif 'total_questions' not in st.session_state:
        page_quiz_question()
    elif (st.session_state['total_questions'] >= 0 and st.session_state['total_questions'] < 5 and 'visited' not in st.session_state):
        if st.session_state['member'] == "Member" and st.session_state['total_questions'] == 3:
            page_question_details_member()
        else:
            page_question_change()
    elif st.session_state['total_questions'] == 5 and 'visited' not in st.session_state:
        page_question_details()
    elif 'reward_points' not in st.session_state:
        page_rewards()

if __name__ == '__main__':
    main()








