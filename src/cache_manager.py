from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache


# ============================================================
# IN-MEMORY CACHE
# ============================================================

def set_memory_cache():
    """
    Enable RAM-based LangChain cache.

    The cache exists only while the application is running.
    It is not written to a persistent database file.
    """

    set_llm_cache(
        InMemoryCache()
    )

    return "InMemoryCache"


# ============================================================
# DISABLE CACHE
# ============================================================

def disable_cache():
    """
    Disable LangChain LLM caching.

    This is the safest option for public deployment because
    no persistent cache is created.
    """

    set_llm_cache(None)

    return "Cache disabled"


# ============================================================
# CONFIGURE CACHE
# ============================================================

def configure_cache(cache_type):
    """
    Configure the LangChain cache.

    Supported options:

        In-Memory
        Disabled

    SQLite caching is intentionally disabled for the public
    version to avoid persistent storage of requests,
    responses, or other potentially sensitive information.
    """

    if cache_type == "In-Memory":

        return set_memory_cache()

    # Any other value, including the old "SQLite" option,
    # safely falls back to disabled caching.

    return disable_cache()