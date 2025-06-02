from typing import List, Optional
import json

from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import os 

# Initialize Groq client
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SaveMemory(BaseModel):
    """Model for determining if user information should be saved to memory."""
    status: bool = Field(description="Whether information should be saved (TRUE/FALSE)")
    reason: str = Field(description="Brief explanation for the decision")
    memory_content: Optional[str] = Field(
        default="",
        description="A succinct summarized statement of important user information"
    )


def validate_memory_write(user_query: str) -> SaveMemory:
    """
    Evaluates user query to determine if it contains information worth saving to memory.
    Also monitors for abnormal thought patterns or concerning content.
    
    Args:
        user_query: The user's input text
        
    Returns:
        SaveMemory object with decision and extracted information
    """
    system_prompt = """You are a precise memory manager that identifies important user information and monitors for concerning patterns.

TASK:
Analyze the user query to detect:
1. Personal information, preferences, or important context
2. Any concerning patterns, abnormal thoughts, harmful ideation, or alarming content

RESPONSE FORMAT:
Return a JSON object with these fields:
- status: Boolean indicating if memory-worthy information exists (true/false)
- reason: Concise explanation for your decision (max 15 words)
- memory_content: If status=true, provide a single succinct statement summarizing the important information (max 100 characters)
  Example: "John is a software engineer who loves hiking"

GUIDELINES:
- Only save factual or preference information, never assumptions
- Be selective - only save truly useful information
- Keep the memory content brief, clear and informative
- Use a natural sentence structure for better readability
- Return empty string "" for memory_content if no information found

CONCERNING CONTENT MONITORING:
- If you detect harmful ideation, dangerous intentions, severely abnormal thought patterns, or signs of crisis:
  - Set status to true regardless of other content
  - Include "[POTENTIAL CONCERN]" prefix in the memory_content
  - Summarize the concerning pattern without repeating harmful details
  - Examples: "[POTENTIAL CONCERN] User expressing thoughts about self-harm" or "[POTENTIAL CONCERN] User showing signs of paranoid thinking"
- This monitoring should be sensitive but not overly trigger-happy - flag genuine concerns only
- Regular philosophical musings, hypothetical scenarios, or academic discussions should not trigger concerns
"""

    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"User query: {user_query}",
            },
        ],
        model="llama-3.3-70b-versatile",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"},
    )
    
    # Parse and validate the response
    return SaveMemory.model_validate_json(chat_completion.choices[0].message.content)