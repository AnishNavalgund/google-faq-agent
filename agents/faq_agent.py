from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.tools import RunContext
from datetime import datetime

from services.search import search_faq

class FAQSearchInput(BaseModel):
    query: str

class FAQSearchResult(BaseModel):
    question: str
    answer: str
    score: float

faq_agent = Agent[None, str](
    "google-vertex:gemini-2.5-flash",
    output_type=FAQSearchResult,
    system_prompt="You are an FAQ assistant. Use the search_from_faq tool to find answers from the knowledge base."
)

@faq_agent.tool
async def search_from_faq(
    ctx: RunContext[None],
    query: str
) -> FAQSearchResult:
    results = search_faq(query=query, top_k=1, threshold=0.75)
    
    if not results:
        return FAQSearchResult(
            question="",
            answer="Sorry, I couldn't find a matching FAQ.",
            score=0.0
        )
    
    return FAQSearchResult(**results[0])

