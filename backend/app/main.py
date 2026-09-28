from src.Tools.Chat.send_user_prompt import send_user_prompt

if __name__ == "__main__":
    user_prompt = input("Quel est votre prompt ?\n")
    context = {}
    response = send_user_prompt(user_prompt, context)
