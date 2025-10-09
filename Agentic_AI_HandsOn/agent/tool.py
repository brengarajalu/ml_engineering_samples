import math

try:
    from duckduckgo_search import DDGS

    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False
    print("Warning: duckduckgo-search not installed. Using mock search instead.")


class Tools:
    def __init__(self):
        self.ddg = DDGS() if DDGS_AVAILABLE else None

    @staticmethod
    def calculate(expression: str) -> float:
        # Basic calculator using eval() - in production, use a safer method
        try:
            # Remove any unsafe characters
            safe_expr = ''.join(c for c in expression if c in '0123456789+-*/(). ')
            return eval(safe_expr)
        except:
            return "Error: Invalid calculation"

    def search(self, query: str) -> str:
        if not DDGS_AVAILABLE:
            # Fallback mock search
            return f"Mock search results for: {query}\n1. Sample Result\n   This is a mock search result.\n2. Another Result\n   Another mock search description."

        try:
            # Get first 3 results from DuckDuckGo
            results = list(self.ddg.text(query, max_results=3))

            if not results:
                return "No results found"

            # Format the results
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['body']}\n"
                )

            return "\n".join(formatted_results)

        except Exception as e:
            return f"Error performing search: {str(e)}"