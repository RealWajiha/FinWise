from langchain_openai import ChatOpenAI
from langchain_classic.chains import LLMChain

from .config import MODEL_NAME

from .prompts import (
    FINANCIAL_PROMPT_TEMPLATE,
    CHAT_PROMPT,
    NARRATIVE_CHAT_TEMPLATE,
)


# ============================================================
# CREATE LLM
# ============================================================

def create_llm(
    api_key: str,
    temperature: float = 0,
):
    """
    Create a ChatOpenAI model using the API key supplied
    by the user at runtime.

    The API key is NOT loaded from config.py or stored
    in this module.
    """

    if not api_key or not api_key.strip():
        raise ValueError(
            "OpenAI API key is required. "
            "Please enter your own API key."
        )

    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=temperature,
        api_key=api_key.strip(),
    )


# ============================================================
# FINANCIAL LLM CHAIN
# ============================================================

def create_financial_chain(llm):
    """
    Create the financial analysis LLMChain.

    The LLM instance is created by create_llm() using
    the user's runtime API key.
    """

    return LLMChain(
        llm=llm,
        prompt=FINANCIAL_PROMPT_TEMPLATE,
    )


# ============================================================
# ANALYZE FINANCES
# ============================================================

def analyze_finances(
    llm,
    inputs,
):
    """
    Analyze financial information using the supplied LLM.

    The API key is already attached to the LLM instance
    created at runtime.
    """

    chain = create_financial_chain(
        llm
    )

    response = chain.invoke(
        inputs
    )

    if isinstance(response, dict):

        return response.get(
            "text",
            str(response),
        )

    return str(response)


# ============================================================
# STREAM RECOMMENDATIONS
# ============================================================

def stream_recommendations(
    llm,
    inputs,
):
    """
    Stream personalized financial recommendations.

    The supplied LLM already uses the user's runtime
    OpenAI API key.
    """

    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(
        **inputs
    )

    for chunk in llm.stream(
        messages
    ):

        if chunk.content:
            yield chunk.content