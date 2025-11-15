"""
Gradio demo wiring: input question -> retrieve -> compose_answer -> show quotes.
"""
from pathlib import Path
import yaml
import numpy as np
import faiss
import gradio as gr
from sentence_transformers import SentenceTransformer
from src.embed_index import load_index
from src.retrieve import retrieve
from src.compose import compose_answer


def load_config(config_path="configs/app.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def embed_query(query: str, model: SentenceTransformer) -> np.ndarray:
    """Embed a query string using the model. Returns normalized embedding."""
    embedding = model.encode([query], normalize_embeddings=True, show_progress_bar=False)
    embedding = np.array(embedding, dtype=np.float32)
    faiss.normalize_L2(embedding)  # Normalize for IndexFlatIP
    return embedding[0]  # Return 1D array (retrieve expects this)


def format_composed_answer(composed: dict) -> str:
    """
    Format composed answer with citations as markdown for display.
    """
    output = f"## Answer\n\n{composed['answer']}\n\n"
    
    if composed.get('references'):
        output += "## Evidence\n\n"
        for ref in composed['references']:
            output += f"{ref}\n\n"
    
    return output


def predict(query: str, index, metadata_df, model: SentenceTransformer, config, chunks_lookup: dict = None):
    """
    Main prediction function: retrieve chunks, compose answer, and format for display.
    """
    if not query or not query.strip():
        return "Please enter a question."
    
    k = config.get('top_k', 5)
    max_quotes = config.get('max_answer_tokens', 300) // 100  # Rough estimate: ~3 quotes
    
    # Create embedding function for retrieve()
    def embed_fn(q: str) -> np.ndarray:
        return embed_query(q, model)
    
    # Retrieve top-k chunks using the retrieve() function
    try:
        retrieved = retrieve(
            query=query,
            index=index,
            embed_fn=embed_fn,
            metadata_df=metadata_df,
            chunks_lookup=chunks_lookup,
            k=k
        )
        
        if not retrieved:
            return "No results found. Try a different query."
        
        # Compose answer using retrieved chunks
        try:
            composed = compose_answer(query, retrieved, max_quotes=max_quotes)
            output = format_composed_answer(composed)
            return output
        except Exception as compose_error:
            # Fallback: show raw retrieval results if composition fails
            return f"Error composing answer: {compose_error}\n\nRetrieved {len(retrieved)} chunks."
        
    except Exception as e:
        return f"Error processing query: {str(e)}"


def launch_app(config_path="configs/app.yaml", index_dir="data/index"):
    """
    Start a Gradio Interface for the RAG system.
    
    Args:
        config_path: Path to config YAML file
        index_dir: Directory containing the FAISS index and metadata
    
    Returns:
        Gradio Interface object
    """
    # Load configuration
    config = load_config(config_path)
    
    print("📚 Loading FAISS index and metadata...")
    index, metadata_df = load_index(index_dir)
    
    print(f"🤖 Loading embedding model: {config['embedding_model']}...")
    model = SentenceTransformer(config['embedding_model'])
    
    # Load chunks data for retrieve() function (needs text for compose_answer)
    chunks_lookup = None
    try:
        import json
        book_name = config['book']
        chunks_file = Path(f"data/interim/chunks/{book_name}_chunks.json")
        if chunks_file.exists():
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks_list = json.load(f)
                chunks_lookup = {chunk['id']: chunk for chunk in chunks_list}
            print(f"✅ Loaded {len(chunks_lookup)} chunks for retrieval and composition")
        else:
            print(f"⚠️  Chunks file not found: {chunks_file}")
            print("   Retrieval will work but compose_answer may not have chunk text")
    except Exception as e:
        print(f"⚠️  Could not load chunks data: {e}")
        print("   Retrieval will work but compose_answer may not have chunk text")
    
    # Create prediction function with loaded resources
    def predict_wrapper(query: str):
        return predict(query, index, metadata_df, model, config, chunks_lookup)
    
    # Create Gradio interface
    interface = gr.Interface(
        fn=predict_wrapper,
        inputs=gr.Textbox(
            label="Question",
            placeholder="Ask a question about the book...",
            lines=2
        ),
        outputs=gr.Markdown(label="Answer & Evidence"),
        title="📚 Classics RAG Q&A",
        description=f"""
        Ask questions about **{config['book'].title()}**!
        
        This system uses semantic search to find relevant passages and compose answers.
        """,
        examples=[
            "What does Lord Henry say about influence?",
            "How does the story describe Dorian's portrait?",
            "What is the main theme of the book?",
        ] if config['book'] == 'dorian' else [
            "How does Homer portray Achilles' anger?",
            "What happens in Book 1?",
            "Describe the shield of Achilles.",
        ],
        theme=gr.themes.Soft(),
    )
    
    print("✅ Gradio interface ready!")
    return interface


if __name__ == "__main__":
    interface = launch_app()
    interface.launch(share=False, server_name="0.0.0.0", server_port=7860)

