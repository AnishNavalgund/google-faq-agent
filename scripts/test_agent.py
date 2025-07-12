import asyncio
from agents.faq_agent import faq_agent

async def main():
    result = await faq_agent.run("Can I pay with coins made of chocolate?")
    print("Answer source:", result.output.source)
    print("Answer:", result.output.answer)
    print("Score:", result.output.score)
    print("Tokens used:", result.usage())

if __name__ == "__main__":
    asyncio.run(main())
