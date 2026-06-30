
import random
import re
from datetime import datetime

RULES = [
    (["hello", "hi", "hey", "greetings"], 3, [
        "Hey there! I'm Nova. What's on your mind?",
        "Hello! Good to see you.",
        "Hi! How can I help you today?",
    ]),
    (["bye", "goodbye", "see you", "exit", "quit"], 3, [
        "Goodbye! Take care.",
        "See you later!",
        "Bye! Come back anytime.",
    ]),
    (["name"], 2, [
        "I'm Nova, your rule-based chat companion.",
        "You can call me Nova.",
    ]),
    (["how are you", "how're you", "how you doing"], 3, [
        "I'm running smoothly, thanks for asking! How about you?",
        "Doing great, just waiting to chat with you.",
    ]),
    (["time"], 2, [
        "It's currently {time}.",
    ]),
    (["date", "today"], 2, [
        "Today's date is {date}.",
    ]),
    (["weather"], 2, [
        "I can't check live weather, but I hope it's nice outside!",
    ]),
    (["joke", "funny"], 2, [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
    ]),
    (["thank", "thanks"], 2, [
        "You're welcome!",
        "Anytime!",
    ]),
    (["help", "support"], 2, [
        "I can chat about greetings, time, jokes, and more. Try saying 'hi' or 'tell me a joke'.",
    ]),
]

FALLBACKS = [
    "I'm not quite sure what you mean. Could you rephrase that?",
    "Hmm, that one's outside my rule set. Try asking something else!",
    "I didn't catch that. Can you try different words?",
]

NAME_PATTERN = re.compile(r"my name is (\w+)", re.IGNORECASE)


def _score_message(message):
    message_lower = message.lower()
    best_score = 0
    best_replies = None
    for keywords, weight, replies in RULES:
        score = sum(weight for kw in keywords if kw in message_lower)
        if score > best_score:
            best_score = score
            best_replies = replies
    return best_replies


def get_response(message, user_name=None):
    """
    Returns (reply_text, updated_user_name).
    user_name may be None; pass back whatever the function returns to
    keep conversation state between calls (the frontend stores this in a
    JS variable, no server-side session needed).
    """
    name_match = NAME_PATTERN.search(message)
    if name_match:
        new_name = name_match.group(1)
        return f"Nice to meet you, {new_name}!", new_name

    replies = _score_message(message)
    if replies:
        reply = random.choice(replies)
    else:
        reply = random.choice(FALLBACKS)

    reply = reply.format(
        time=datetime.now().strftime("%H:%M:%S"),
        date=datetime.now().strftime("%B %d, %Y"),
    )

    if user_name and random.random() < 0.3:
        reply = f"{reply} ({user_name})"

    return reply, user_name
