MEDICAL_DISCLAIMER = """
IMPORTANT: This system provides general medical information for educational purposes only. 
It is not a substitute for professional medical advice, diagnosis, or treatment. 
Always seek the advice of your physician or other qualified health provider with any questions 
you may have regarding a medical condition.
"""

GENERAL_RESPONSES = {
    "greeting": {
        "answer": "Hello! I'm your medical information assistant. I can help you with medical questions based on clinical guidelines and patient education materials. How can I assist you today?",
        "confidence_level": "High - Standard Response",
        "citations": []
    },
    "farewell": {
        "answer": "Goodbye! Remember to consult healthcare professionals for specific medical advice. Take care!",
        "confidence_level": "High - Standard Response",
        "citations": []
    },
    "general_chat": {
        "answer": "I'm a medical information assistant focused on providing information from medical guidelines and patient education materials. While I'm happy to chat, I can be most helpful with specific medical questions. What medical topic would you like to learn about?",
        "confidence_level": "High - Standard Response",
        "citations": []
    }
}

CONVERSATION_PATTERNS = {
    "greetings": [
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening", "howdy"
    ],
    "farewells": [
        "bye", "goodbye", "see you", "farewell", "good night", "take care"
    ],
    "general_chat": [
        "how are you", "what's up", "what do you do", "who are you", "tell me about yourself"
    ]
}