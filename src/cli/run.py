from src.llm.prompt_handler import get_greeting_response
from src.db.database import create_database
from src.generators.sample_data import insert_sample_data
from src.embeddings.train_embedding import store_embeddings

def run_cli():
    create_database()
    insert_sample_data()
    store_embeddings()  # Runs only if new data is found

    flag = True
    while flag:
        user_prompt = input("Enter your prompt: ")
        if user_prompt.lower() == "exit":
            flag = False
            break
        response = get_greeting_response(user_prompt)
        print(response)

if __name__ == "__main__":
    run_cli()