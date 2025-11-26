import asyncio
from src.tools.websearch import WebSearchTool

async def main():
    tool = WebSearchTool()
    print("Searching for 'python programming'...")
    results = await tool.search("python programming", max_results=3)
    
    if not results:
        print("No results found!")
    else:
        print(f"Found {len(results)} results:")
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['title']}")
            print(f"   URL: {res['url']}")
            print(f"   Snippet: {res['snippet'][:100]}...")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
