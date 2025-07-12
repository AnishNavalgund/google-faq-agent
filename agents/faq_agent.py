from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, messages
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.providers.google_vertex import GoogleVertexProvider
from pydantic_ai.models import ModelRequestParameters
from services.search import search_faq

# Initialize the Gemini model via Vertex AI
model = GeminiModel(
    model_name="gemini-2.5-flash",
    provider=GoogleVertexProvider(region="us-central1")
)

class FAQSearchResult(BaseModel):
    question: str
    answer: str
    score: float
    source: str  # "search" or "llm"

faq_agent = Agent(
    model,
    deps_type=None,
    output_type=FAQSearchResult,
    system_prompt="You are an FAQ assistant. Use the search_from_faq tool when possible."
)

@faq_agent.tool
async def search_from_faq(ctx: RunContext[None], query: str) -> FAQSearchResult:
    results = search_faq(query=query, top_k=1, threshold=0.5)
    if not results or results[0]["score"] < 0.7:
        # fallback: use LLM to generate answer
        user_text = f"User asked: '{query}'. Provide a helpful answer based on support tone."
        response = await ctx.model.request(
            messages=[messages.ModelRequest(parts=[messages.UserPromptPart(content=user_text)])],
            model_settings=GeminiModelSettings(),
            model_request_parameters=ModelRequestParameters()
        )
        
        # Extract content from response parts
        content = ""
        for part in response.parts:
            if hasattr(part, 'content'):
                content += part.content
        
        return FAQSearchResult(
            question=query,
            answer=content.strip(),
            score=0.0,
            source="llm"
        )

    best = results[0]
    return FAQSearchResult(
        question=best["question"],
        answer=best["answer"],
        score=best["score"],
        source="search"
    )
