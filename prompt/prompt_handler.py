import ollama
import datetime

# Get the current date
current_date = datetime.datetime.now().date()
# target_date = datetime.date(2024, 6, 12)

# Set the model based on the date
# llm_name = "mistral" if current_date > target_date else "gemma"
# Set the model to always use Gemma:2B

llm_name = "gemma:2b"  # Removed Mistral

def get_greeting_response(user_prompt):
    # prompt = """
    #     I want you to greet how any first 
    #     computer science program usually greets the world, 
    #     followed with a smiley
    # """

    response = ollama.chat(
        model=llm_name,
        # messages=[{"role": "user", "content": prompt}]
        messages=[{"role": "user", "content": user_prompt}] #takes user input as prompt
    )

    return response['message']['content']  # Ollama's response format

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")  # Get user input
    response = get_greeting_response(user_prompt)
    print("\nLLM Response:", response)