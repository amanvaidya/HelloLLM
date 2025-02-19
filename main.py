from prompt.prompt_handler import get_greeting_response

# Get user input for the prompt
user_prompt = input("Enter your prompt: ")
response = get_greeting_response(user_prompt)
print(response)