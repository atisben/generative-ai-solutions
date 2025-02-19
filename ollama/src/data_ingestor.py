from typing import List

from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from src.config import Config
from src.config import configure_logging
from src.file_loader import File
from uuid import uuid4

logger = configure_logging()  
 

CONTEXT_PROMPT = """ 
You're an expert in document analysis. Your task is to provide a brief, relevant context for a chunk of the following document.

Here is the document 
<document>
{document}
</document>

here is the chunk we want to situate within the whole document:
<chunk>
{chunk}
</chunk>

Provide a concise context (2-3 sentences) for this chunk, considering the following guidelines: 
1. Identify the main topic or concept discussed in the chunk.
2. Mention any relevant information or comparison with the broader context.
3. If applicable, not how this piece of information relate to the overall document or the broader context.
4. Include any key figures, dates or percentage that provide important context. 
5. Do not use phrases like "This chunk discusses" or "This section provides". Instead directly state the context.

Please give a short context to situate this chunk within the overal document for the purpose of improving search retrieval of this chunk. 

Context:
""".strip()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=Config.Preprocessing.CHUNK_SIZE,
    chunk_overlap=Config.Preprocessing.CHUNK_OVERLAP
)

def create_llm() -> ChatOllama:
    return ChatOllama(model=Config.Preprocessing.LLM, temperature=0, keep_alive=1)

def create_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=Config.Preprocessing.EMBEDDING_MODEL)

def create_reranker() -> FlashrankRerank:
    return FlashrankRerank(
        model=Config.Preprocessing.RERANKER, top_n=Config.Chatbot.N_CONTEXT_RESULTS
    )

def create_or_get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=Config.VectorStore.COLLECTION_NAME,
        embedding_function=create_embeddings(),
        persist_directory=Config.Path.DB_DIR.as_posix(),  # Where to save data locally, remove if not necessary
    )

def _generate_context(llm: ChatOllama, document: str, chunk: str) -> str:
    """Generates additional context for a chunk of text given a broader document."""
    messages = CONTEXT_PROMPT.format(document=document, chunk=chunk)
    response = llm.invoke(messages)
    return(response.content)
     

def _create_chunks(document: Document) -> List[Document]:
    """Split the document into chunks and add context."""
    logger.info("Chunking document") 
    chunks = text_splitter.split_documents([document])
    logger.info(f"Generated {len(chunks)} chunks")
    if not Config.Preprocessing.CONTEXTUALIZE_CHUNKS:
        return chunks
    llm = create_llm()
    contextual_chunks = []
    for i, chunk in enumerate(chunks):
        logger.info(f"Creating context for chunk {i}") 
        context = _generate_context(llm, document.page_content, chunk.page_content)
        chunk_with_context = f"{context}\n\n{chunk.page_content}"
        contextual_chunks.append(Document(page_content=chunk_with_context, metadata=chunk.metadata))
    return contextual_chunks


def ingest_files(files: List[File]) -> BaseRetriever:
    # Ingest the documents as langchain Documents objects
    documents = [Document(file.content, metadata={"source": file.name}) for file in files]
    chunks = []
    for document in documents:
        # Adding chuncks within the chunk list for all the documents
        chunks.extend(_create_chunks(document))

    # Builing retriever
    logger.info("Creating embeddings") 
    vector_store = create_or_get_vectorstore()
    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=uuids)
    semantic_retriever = vector_store.as_retriever(search_kwargs={"k": Config.Preprocessing.N_SEMANTIC_RESULTS})

    # semantic_retriever = InMemoryVectorStore.from_documents(
    #      chunks, create_embeddings()
    # ).as_retriever(search_kwargs={"k": Config.Preprocessing.N_SEMANTIC_RESULTS})

    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = Config.Preprocessing.N_BM25_RESULTS

    ensemble_retriever = EnsembleRetriever(
        retrievers=[semantic_retriever, bm25_retriever],
        weights=[0.6, 0.4]
    )

    return ContextualCompressionRetriever(
        base_compressor=create_reranker(), base_retriever=ensemble_retriever
    )
    