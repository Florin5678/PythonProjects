import openai
import time

openai.api_key="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"

def chatbot(query):
    try:
        # Make the API call
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' if you have access to it
            prompt=query,
            max_tokens=150,
            temperature=0.7,
        )
        return response['choices'][0]['text'].strip()

    except openai.RateLimitError:
        print("Rate limit reached. Retrying after a short delay...")
        time.sleep(10)  # Sleep for 10 seconds before retrying
        return chatbot(query)  # Retry the request

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit' or user_input.lower() == 'end':
            print("Goodbye!")
            break
        response = chatbot(user_input)
        print(f"Bot: {response}\n")

main()