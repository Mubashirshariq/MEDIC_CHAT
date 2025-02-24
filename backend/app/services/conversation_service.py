from typing import Optional, Dict, Any
from app.core.constants import CONVERSATION_PATTERNS, GENERAL_RESPONSES
from app.models.schema import QAResponse, Source

class ConversationService:
    @staticmethod
    def detect_conversation_type(text: str) -> Optional[str]:
        text = text.lower().strip()
        
        for pattern_type, patterns in CONVERSATION_PATTERNS.items():
            if any(pattern in text for pattern in patterns):
                return pattern_type
        return None

    @staticmethod
    def get_conversation_response(conv_type: str) -> QAResponse:
        response_data = GENERAL_RESPONSES.get(conv_type, GENERAL_RESPONSES["general_chat"])
        
        return QAResponse(
            answer=response_data["answer"],
            citations=[Source(**citation) for citation in response_data.get("citations", [])],
            follow_up_questions=[
                "What medical topic would you like to learn about?",
                "Do you have any specific health-related questions?",
                "Would you like information about any particular medical condition?"
            ],
            disclaimer="",  # No medical disclaimer needed for general conversation
            confidence_level=response_data["confidence_level"]
        )