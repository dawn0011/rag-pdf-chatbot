"""LCEL RAG chain construction for PDF Q&A."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_groq import ChatGroq


def format_docs(docs) -> str:
    """Format retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(retriever: BaseRetriever, llm: ChatGroq) -> Runnable:
    """
    Build an LCEL RAG chain using pipe syntax.

    The chain:
    1. Takes the user's question
    2. Retrieves relevant chunks from the vector store using MMR
    3. Formats them as context
    4. Passes context + question to the prompt
    5. Sends to the LLM
    6. Parses the output as a string

    Args:
        retriever: LangChain retriever (from vector store)
        llm: ChatGroq LLM instance

    Returns:
        LCEL Runnable chain that accepts {"question": str} and returns str
    """
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant that answers questions based on provided context.

Context from the document:
{context}

Question: {question}

Instructions:
- Answer based ONLY on the context provided above.
- If the question cannot be answered from the context, say "I cannot find this information in the document."
- Be concise and clear.
- If relevant, cite the specific part of the document you're referencing."""
    )

    # LCEL pipe chain: retriever -> format_docs, question passthrough -> prompt -> llm -> output_parser
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
