import ollama
import datetime

current_date = datetime.datetime.now().date()
llm_name = "gemma:2b"

def get_greeting_response(user_prompt):
    try:
        response = ollama.chat(
            model=llm_name,
            messages=[{"role": "user", "content": f"Current date: {current_date}. {user_prompt}"}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def generate_test(language, method_code):
    prompt = f"Generate a test case for the following {language} method:\n{method_code}"
    try:
        response = ollama.generate(model=llm_name, prompt=prompt)
        return {"status": "success", "response": response["response"]}
    except Exception as e:
        return {"status": "error", "response": str(e)}

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    response = get_greeting_response(user_prompt)
    print("\nLLM Response:", response)