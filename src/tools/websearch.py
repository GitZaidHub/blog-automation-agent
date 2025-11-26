import asyncio
from duckduckgo_search import DDGS

class WebSearchTool:
    """Real web search using DuckDuckGo."""
    
    def _search_sync(self, query: str, max_results: int):
        """Synchronous search execution."""
        results = []
        try:
            with DDGS() as ddgs:
                # ddgs.text returns an iterator, convert to list
                search_results = list(ddgs.text(query, max_results=max_results))
                for r in search_results:
                    results.append({
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "url": r.get("href", "")
                    })
        except Exception as e:
            print(f"Error performing search: {e}")
        return results

    async def search(self, query: str, max_results: int = 5):
        """
        Search the web for the given query.
        
        Args:
            query: The search query string.
            max_results: Maximum number of results to return (default 5).
            
        Returns:
            List of dictionaries containing 'title', 'snippet', and 'url'.
        """
        loop = asyncio.get_running_loop()
        # Run synchronous search in a separate thread to avoid blocking the event loop
        return await loop.run_in_executor(None, self._search_sync, query, max_results)
