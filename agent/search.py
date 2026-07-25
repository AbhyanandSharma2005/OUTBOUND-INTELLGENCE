"""
Thin wrapper around Tavily web search.
Groq's LLMs have no built-in browsing, so every fact used downstream
must come from here first -- the model only ever *synthesizes* real
snippets, it never invents them.
"""
from tavily import TavilyClient


def run_search(api_key: str, query: str, max_results: int = 5) -> str:
    """Run one web search and return a compact, citeable text block."""
    client = TavilyClient(api_key=api_key)
    try:
        resp = client.search(query=query, max_results=max_results, search_depth="advanced")
    except Exception as e:
        return f"[SEARCH_ERROR for query '{query}': {e}]"

    results = resp.get("results", [])
    if not results:
        return f"[NO_RESULTS for query '{query}']"

    blocks = []
    for r in results:
        title = r.get("title", "")
        url = r.get("url", "")
        content = (r.get("content", "") or "")[:800]
        blocks.append(f"SOURCE: {title}\nURL: {url}\nSNIPPET: {content}")
    return "\n\n".join(blocks)


def multi_search(api_key: str, queries: list[str], max_results: int = 4) -> str:
    """Run several queries and concatenate labeled results."""
    sections = []
    for q in queries:
        sections.append(f"### Query: {q}\n{run_search(api_key, q, max_results)}")
    return "\n\n".join(sections)
