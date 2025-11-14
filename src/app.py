"""
Gradio demo wiring: input question -> retrieve -> compose_answer -> show quotes.
"""


def launch_app():
    """
    Start a small Gradio Interface.

    # TODO hints:
    # - Load index/metadata and the embedding model once at startup.
    # - Build a predict(question) callable that returns answer + quoted spans.
    # - Interface: textbox in, markdown + quotes out.

    # === TODO (you code this) ===
    # UI formatting: show answer first, then a collapsible "Evidence" section listing [n] citations.
    # Hints:
    # 1) Use markdown with blockquotes for quotes; show source metadata inline.
    # 2) Provide a toggle to show the underlying chunk text when needed.
    # Acceptance:
    # - Predict(question) returns a dict or markdown that renders cleanly in Gradio.

    # Acceptance:
    # - Running launch_app() opens a working local demo after you implement TODOs.
    """
    raise NotImplementedError

