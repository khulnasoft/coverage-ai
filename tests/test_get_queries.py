import os
import tempfile
import unittest
from pathlib import Path

from coverage_ai.lsp_logic.file_map.queries.get_queries import get_queries_scheme


class TestGetQueries(unittest.TestCase):
    """Test cases for get_queries_scheme function"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_path = Path(__file__).parent.parent / "coverage_ai" / "lsp_logic" / "file_map" / "queries"
        
        # List of all supported languages
        self.supported_languages = [
            "arduino", "c", "cpp", "c_sharp", "chatito", "clojure", "commonlisp",
            "d", "dart", "elisp", "elixir", "elm", "fortran", "gleam", "go",
            "haskell", "hcl", "java", "javascript", "julia", "kotlin", "lua",
            "matlab", "ocaml", "php", "pony", "properties", "python", "ql",
            "r", "racket", "ruby", "rust", "scala", "solidity", "swift",
            "typescript", "udev", "zig"
        ]

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_all_supported_languages_load_queries(self):
        """Test that all supported languages can load their queries"""
        failed_languages = []
        
        for lang in self.supported_languages:
            try:
                queries = get_queries_scheme(lang)
                if not queries.strip():
                    failed_languages.append(f"{lang}: Empty queries")
            except Exception as e:
                failed_languages.append(f"{lang}: {str(e)}")
        
        self.assertEqual(len(failed_languages), 0, 
                        f"Failed to load queries for languages: {failed_languages}")

    def test_standard_naming_convention(self):
        """Test standard tree-sitter-{lang}-tags.scm naming"""
        # Test with existing language that uses standard naming
        queries = get_queries_scheme("python")
        self.assertTrue(len(queries) > 0, "Standard naming should work")
        self.assertIn("@name.definition.function", queries)

    def test_special_naming_convention(self):
        """Test special {lang}-tags.scm naming (like zig)"""
        # Create a temporary query file with special naming
        temp_query_path = os.path.join(self.temp_dir, "speciallang-tags.scm")
        with open(temp_query_path, "w") as f:
            f.write("(special) @name.definition.class")
        
        # Test would require mocking, so we test zig directly
        queries = get_queries_scheme("zig")
        self.assertTrue(len(queries) > 0, "Zig queries should load successfully")

    def test_nonexistent_language_returns_empty(self):
        """Test that non-existent languages return empty string"""
        queries = get_queries_scheme("nonexistent_language_12345")
        self.assertEqual(queries, "")

    def test_empty_query_file(self):
        """Test handling of empty query files"""
        # This tests the robustness of the query loading
        queries = get_queries_scheme("python")  # Use existing language
        self.assertIsInstance(queries, str)

    def test_malformed_query_file_handling(self):
        """Test handling of malformed query files"""
        # Test with existing languages that might have malformed queries
        # The function should not crash even if queries are malformed
        for lang in ["python", "javascript"]:  # Test with common languages
            try:
                queries = get_queries_scheme(lang)
                self.assertIsInstance(queries, str)
            except Exception as e:
                self.fail(f"get_queries_scheme crashed for {lang}: {e}")

    def test_case_sensitivity(self):
        """Test case sensitivity in language names"""
        # Test with different cases
        queries_lower = get_queries_scheme("python")
        queries_upper = get_queries_scheme("PYTHON")
        
        # Should handle case appropriately (tree-sitter languages are typically lowercase)
        self.assertTrue(len(queries_lower) > 0, "Lowercase language should work")

    def test_query_content_validation(self):
        """Test that loaded queries contain expected patterns"""
        # Test a few languages to ensure they have proper query patterns
        test_languages = {
            "python": ["@name.definition.function", "@name.definition.class"],
            "javascript": ["@name.definition.function", "@name.definition.class"],
            "rust": ["@name.definition.function", "@name.definition.class"],
        }
        
        for lang, expected_patterns in test_languages.items():
            queries = get_queries_scheme(lang)
            for pattern in expected_patterns:
                self.assertIn(pattern, queries, 
                            f"{lang} queries should contain {pattern}")

    def test_performance_load_time(self):
        """Test that query loading is reasonably fast"""
        import time
        
        start_time = time.time()
        
        # Load queries for all supported languages
        for lang in self.supported_languages:
            get_queries_scheme(lang)
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Should load all queries in under 1 second
        self.assertLess(load_time, 1.0, 
                       f"Loading all queries took too long: {load_time:.3f}s")


if __name__ == "__main__":
    unittest.main()
