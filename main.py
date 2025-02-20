from prompt.prompt_handler import get_greeting_response
from db.database import create_database
from db.insert_data import insert_sample_data
from embeddings.generate_embedding import store_embeddings

# Ensure database and initial data are set up before running the app
create_database()
insert_sample_data()
store_embeddings()  # Runs only if new data is found

# Get user input for the prompt
flag = True
while flag:
    user_prompt = input("Enter your prompt: ")
    if user_prompt.lower() == "exit":
        flag = False
        break
    response = get_greeting_response(user_prompt)
    print(response)