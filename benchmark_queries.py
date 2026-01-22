#!/usr/bin/env python3
"""
Benchmark script for tree-sitter query loading performance.
Tests loading time for all supported languages.
"""

import time
from coverage_ai.lsp_logic.file_map.queries.get_queries import get_queries_scheme

def benchmark_query_loading():
    """Benchmark query loading performance for all supported languages"""
    
    # List of all supported languages
    supported_languages = [
        "arduino", "c", "cpp", "c_sharp", "chatito", "clojure", "commonlisp",
        "d", "dart", "elisp", "elixir", "elm", "fortran", "gleam", "go",
        "haskell", "hcl", "java", "javascript", "julia", "kotlin", "lua",
        "matlab", "ocaml", "php", "pony", "properties", "python", "ql",
        "r", "racket", "ruby", "rust", "scala", "solidity", "swift",
        "typescript", "udev", "zig"
    ]
    
    print("🚀 Benchmarking Tree-Sitter Query Loading Performance")
    print("=" * 60)
    
    # Benchmark individual language loading
    individual_times = {}
    total_start = time.time()
    
    for lang in supported_languages:
        start_time = time.time()
        queries = get_queries_scheme(lang)
        end_time = time.time()
        
        load_time = (end_time - start_time) * 1000  # Convert to milliseconds
        individual_times[lang] = load_time
        
        # Check if queries were loaded successfully
        status = "✅" if queries.strip() else "❌"
        query_size = len(queries)
        
        print(f"{status} {lang:<12} {load_time:>6.2f}ms {query_size:>6} chars")
    
    total_end = time.time()
    total_time = (total_end - total_start) * 1000
    
    print("\n" + "=" * 60)
    print("📊 Performance Summary")
    print("=" * 60)
    
    # Calculate statistics
    times = list(individual_times.values())
    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    max_lang = max(individual_times, key=individual_times.get)
    min_lang = min(individual_times, key=individual_times.get)
    
    print(f"Total languages:     {len(supported_languages)}")
    print(f"Total loading time:  {total_time:.2f}ms")
    print(f"Average per language: {avg_time:.2f}ms")
    print(f"Fastest language:    {min_lang} ({min_time:.2f}ms)")
    print(f"Slowest language:    {max_lang} ({max_time:.2f}ms)")
    
    # Performance classification
    if total_time < 50:
        performance = "🟢 Excellent"
    elif total_time < 100:
        performance = "🟡 Good"
    elif total_time < 200:
        performance = "🟠 Acceptable"
    else:
        performance = "🔴 Needs optimization"
    
    print(f"Overall performance: {performance}")
    
    # Memory usage estimate (rough approximation)
    total_chars = sum(len(get_queries_scheme(lang)) for lang in supported_languages)
    estimated_memory_kb = total_chars / 1024
    print(f"Estimated memory:    {estimated_memory_kb:.1f} KB for all queries")
    
    return {
        'total_time_ms': total_time,
        'avg_time_ms': avg_time,
        'max_time_ms': max_time,
        'min_time_ms': min_time,
        'max_lang': max_lang,
        'min_lang': min_lang,
        'total_languages': len(supported_languages),
        'estimated_memory_kb': estimated_memory_kb
    }

def benchmark_repeated_loading():
    """Benchmark repeated loading of the same queries"""
    print("\n🔄 Benchmarking Repeated Loading")
    print("=" * 40)
    
    test_languages = ["python", "javascript", "rust", "swift", "zig"]
    iterations = 100
    
    for lang in test_languages:
        start_time = time.time()
        for _ in range(iterations):
            get_queries_scheme(lang)
        end_time = time.time()
        
        total_time = (end_time - start_time) * 1000
        avg_time = total_time / iterations
        
        print(f"{lang:<12} {total_time:>6.2f}ms total, {avg_time:>4.2f}ms avg ({iterations} iterations)")

if __name__ == "__main__":
    results = benchmark_query_loading()
    benchmark_repeated_loading()
    
    print(f"\n✅ Benchmark completed successfully!")
    print(f"📈 Results: Loading {results['total_languages']} languages in {results['total_time_ms']:.2f}ms")
