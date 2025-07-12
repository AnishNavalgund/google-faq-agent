import asyncio
from agents.faq_agent import faq_agent, FAQSearchInput

async def main():
    result = await faq_agent.run("what is my name?")
    print(result.output)
    print(result.usage())

if __name__ == "__main__":
    asyncio.run(main())
