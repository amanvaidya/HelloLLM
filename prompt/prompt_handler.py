import ollama
import datetime

# Get the current date
current_date = datetime.datetime.now().date()

# Set the model to always use Gemma:2B
llm_name = "gemma:2b"

def get_greeting_response(user_prompt):
    """
    Generates a greeting response based on the user's prompt using the LLM.
    """
    response = ollama.chat(
        model=llm_name,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response['message']['content']  # Ollama's response format

def generate_test(method_code):
    """
    Generates a JUnit test case for the given Java method using the LLM.
    """
    prompt = f"Generate a JUnit test case for the following Java method:\n{method_code}"
    
    response = ollama.generate(model=llm_name, prompt=prompt)

    return {"status": "success", "unit_test": response["response"]}  # Extract response content

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")  # Get user input
    response = get_greeting_response(user_prompt)
    print("\nLLM Response:", response)