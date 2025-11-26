import duckduckgo_search
print(dir(duckduckgo_search))
try:
    from duckduckgo_search import DDGS
    print("DDGS available")
except ImportError:
    print("DDGS NOT available")

try:
    from duckduckgo_search import AsyncDDGS
    print("AsyncDDGS available")
except ImportError:
    print("AsyncDDGS NOT available")
