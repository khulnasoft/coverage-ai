import os
from pathlib import Path


def get_queries_scheme(lang: str) -> str:
    """
    Get query scheme for a language.
    This function now supports dynamic updates through the QueryManager.
    """
    try:
        # Try to use the global query manager if available
        try:
            from coverage_ai.lsp_logic.file_map.query_manager import get_global_query_manager
            manager = get_global_query_manager()
            query = manager.get_query(lang)
            if query:
                return query
        except ImportError:
            # QueryManager not available, fall back to static loading
            pass
        
        # Load the relevant queries (fallback method)
        curr_path = Path(__file__).parent
        
        # Try tree-sitter-{lang}-tags.scm first (standard naming)
        path = os.path.join(curr_path, f"tree-sitter-{lang}-tags.scm")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        
        # Try {lang}-tags.scm naming (for zig and other languages)
        path = os.path.join(curr_path, f"{lang}-tags.scm")
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        
        return ""
    except (KeyError, FileNotFoundError):
        return ""
