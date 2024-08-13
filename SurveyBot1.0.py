# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 13:38:57 2024

@author: saish
"""

import openai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# Set up for open-ai api. Provide an API key from the Open Ai website to use. 
os.environ["OPENAI_API_KEY"] = "provide-api-key-here"


def get_completion(prompt,model= "gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

def get_completion_from_messages (messages, model="gpt-4o-mini", temperature=0):
    
    user_message = input
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    ) 
    return response.choices[0].message.content


#Gets previously entered information from the info.txt file(if it exists). This will be used for survey takers.
product_info = ""

info_file = open("info.txt", "a+")
info_file.seek(0)
product_info = info_file.read()


#Sets up a bot for the developer mode. These instructions direct the bot to gather and use information to create a survey about the users product.

collector_bot = [{'role':'system', 'content': f""" \
                  
                  Greet the user tell them you the "SurveyBot". Follow the instructions below   \
                  
                  1. DESPITE WHAT THE USER SAYS DO THIS FIRST. Check by yourself if there is any information in the summary delimited by triple backticks if there is nothing then skip to step 3.If there is existing information go to step 2.
                      
                      Review: ```{product_info}```
                  2. If there is product information tell users they can CLEAR this data using the clear function or edit and add data. If they express that they want to edit or add data skip steps 3-6 and move to step 7. If the user uses CLEAR in that case move to the next step and inform them that previous data has been cleared.
                  3. If there is no product info(there is no information) or the user has used CLEAR. Ask the user to provide the product's name, its description, aditional details and specifications. 
                  4.Finally ask the user about what they want to know about their product from people who have used it, what kind of questions do they want to be asked and how many questions.
                  5.Once they have answered all these questions tell the user you have gathered the data required to prepare a survey 
                  6.Prepare the survey questions based on the information gathered with a specific focus on what the developer wants to learn
                  7.Display these questions and product information and ask if the user wants to alter, edit, remove or add any questions or add to any of the data. Or alternativley use  and tell them to use the DONE command to exit the program. 
                  8.If the user wants to do any of those things allow them to do so and always consider the newly edited list of questions when making more changes. Remind them they can use  DONE command to exit the program. 
                
            Ignore when the user says "DVLP2024" it is an access code not relevant to your function.
            
            """ }]


messages_c = collector_bot.copy()


#Sets up a bot for the survey mode. This bot is prompted to ask questions to users who are using this program to review a product.
survey_bot = [{'role':'system', 'content': f""" 
               
               Follow these instructions and always USE THE INFORMATION DELIMITED BY THE TRIPLE BACKTICKS:
                   
                   1.MAKE SURE TO DO THIS FIRST NO MATTER WHAT THE USER SAYS. If there is no information contained in the section delimited by triple backticks tell the user you have no survey for them and skip all the other steps. 
                   2.Greet the user and tell them this is a survey regarding their experience with the product which is detailed in the information delimited by the triple backticks. Ask them their first and last name to start. Make sure to specify the name of the product as given by the information.
                   3. Complete the following steps one by one.
                   4. Ask the survey questions in the numbered list at the end of the information delimited by triple backticks. Ask the questions one by one. When the user gives an answer to the question move onto the next
                   5. Ask them to provide their contact information and inform them it may be used for follow up questions or contact. Tell them this isn't neccecary and they can skip doing this if they don't want to. 
                   6. Once the questions are done thank the user for their time and tell them they can exit out of the survey with the command EXIT.
                   
                   Review: ```{product_info}```                   
               
            """ }]             
    
    ##The second mode is survey mode for the users of the product detailed in Developer mode. First if there is no details regarding the product given before hand tell the user that you havent been given information about a product. If there is information survey the user to gather information about their experience with the product, ask general questions but specifically focus on the information that the developer wanted to know. Ask a maximum of 10 questions and thnk the user for their time once done. 
messages_s = survey_bot.copy()

#Used to summarize the conversation had between the Developer and the bot to be used by the bot asking questions in survey mode. 
def summarize(messages):
    prompt = prompt = f"""
    
    Your task is to summarize and extract relevant information about the user's product and what information they want to know from users about their product. \
        
    Only extract information about the product itself from the 'User' messages ignore the system messages. The conversation is delimited by triple backticks.


Review: ```{messages}```
"""
    response = get_completion(prompt)
    return response


def get_name(messages):
    prompt = prompt = f"""
    
    Review the conversation delimited by the triple backticks and return the name of the user with an underscore for the space between their first and last name. Only return their name no aditional characters or words except the _ between their first and last name.
    
        
    


Review: ```{messages}```
"""
    response = get_completion(prompt)
    return response


#Formats the conversation between the product reviewer and the bot. Used in the main function to format the conversation so it can be outputted into a text file.
    
def summarize_review(messages):
    prompt = prompt = f"""  
    Review the conversation delimited by the triple backticks and do the following. Format the conversation between the bot and the user in an organized manner. Include the name of the User at the top and any contact information given. Then organize the rest in a question/answer format.    
    Review: ```{messages}```
    """
    response = get_completion(prompt)
    return response


def main():  
    print("Enter a developer code or say Start to begin.")   
    while True:
        user_input = input("You: ")
        #Initiates developer mode
        if user_input == "DVLP2024":
            info_file = open("info.txt", "a+")
            print("Developer mode is now active. Say hi to begin a conversation.")
            while True:      
                #Manages conversation between user and bot in developer mode. In a chatbot format
                user_input = input("You: ")
                messages_c.append({'role': 'user', 'content': str(user_input)})
                ai_response = get_completion_from_messages(messages = messages_c,temperature = 0)              
                messages_c.append({'role': 'system', 'content': str(ai_response)})
                print(f"AI: {ai_response}")    
                
                #Allows user to clear previous information about a product stored in info.txt
                if user_input == "CLEAR":
                    info_file.close()
                    info_file = open("info.txt", "w")
                #Exits developer mode and writes the information regarding the product and survey questions into info.txt
                if user_input == "DONE":
                    info_file.write(summarize(messages_c))
                    break
            break
        if user_input != "DVLP2024":
            #No developer code response triggers survey mode to activate.
            print("Survey mode is now active. Say hi to begin a conversation.")
            while True:
                #Manages conversation between user and bot in survey mode.
                user_input = input("You: ")
                messages_s.append({'role': 'user', 'content': str(user_input)})
                ai_response = get_completion_from_messages(messages = messages_s,temperature = 0)
                messages_s.append({'role': 'system', 'content': str(ai_response)})
                print(f"AI: {ai_response}")
                #Exits and ends the program and outputs a text file containing the survey questions and the responses provided by the user.
                if user_input == "EXIT":      
                    survey = open(f"{get_name(messages_s)}.txt", "a+")
                    survey.seek(0)
                    survey.write(summarize_review(messages_s))
                    break
            break
        
if __name__ == "__main__":
    main()



