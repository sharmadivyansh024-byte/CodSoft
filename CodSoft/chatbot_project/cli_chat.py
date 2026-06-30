
from chatbot_logic import get_response

def main():
    print("Nova: Hi! I'm a rule-based chatbot. Type 'bye' to exit.")
    user_name = None
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        reply, user_name = get_response(user_input, user_name)
        print(f"Nova: {reply}")
        if any(word in user_input.lower() for word in ["bye", "goodbye", "exit", "quit"]):
            break

if __name__ == "__main__":
    main()
