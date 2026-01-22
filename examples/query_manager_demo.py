#!/usr/bin/env python3
"""
Query Manager Demo
Demonstrates real-time query updates and dynamic language support.
"""

import time
import tempfile
from pathlib import Path

from coverage_ai.lsp_logic.file_map.query_manager import QueryManager, QueryUpdateEvent


def on_query_update(event: QueryUpdateEvent):
    """Callback function for query updates"""
    print(f"🔄 Query Update: {event.language} - {event.event_type}")
    if event.error_message:
        print(f"   Error: {event.error_message}")
    elif event.previous_hash and event.new_hash:
        print(f"   Content changed: {event.previous_hash[:8]}... -> {event.new_hash[:8]}...")


def demonstrate_basic_usage():
    """Demonstrate basic QueryManager usage"""
    print("🚀 Query Manager Demo")
    print("=" * 50)
    
    # Create query manager with callback
    manager = QueryManager(update_callbacks=[on_query_update])
    
    # Show initial statistics
    stats = manager.get_statistics()
    print(f"\n📊 Initial Statistics:")
    print(f"   Total languages: {stats['total_languages']}")
    print(f"   Valid queries: {stats['valid_queries']}")
    print(f"   Total size: {stats['total_size_bytes']} bytes")
    print(f"   Watching enabled: {stats['watching_enabled']}")
    
    # List supported languages
    languages = manager.list_supported_languages()
    print(f"\n🌍 Supported Languages (first 10): {languages[:10]}")
    print(f"   Total: {len(languages)} languages")
    
    # Get query info for a specific language
    python_info = manager.get_query_info("python")
    if python_info:
        print(f"\n🐍 Python Query Info:")
        print(f"   File: {python_info.file_path}")
        print(f"   Size: {python_info.size_bytes} bytes")
        print(f"   Valid: {python_info.is_valid}")
        print(f"   Last modified: {python_info.last_modified}")
    
    return manager


def demonstrate_custom_queries(manager: QueryManager):
    """Demonstrate adding custom queries"""
    print(f"\n🔧 Custom Query Demo")
    print("-" * 30)
    
    # Add a custom query for a fictional language
    custom_query = """
; FictionalLang query patterns
(function_definition
  name: (identifier) @name.definition.function) @definition.function

(class_definition
  name: (identifier) @name.definition.class) @definition.class

(variable_declaration
  name: (identifier) @name.definition.variable) @definition.variable

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

; References
(identifier) @ref
    """.strip()
    
    print("Adding custom query for 'fictionallang'...")
    success = manager.add_custom_query("fictionallang", custom_query)
    print(f"Success: {success}")
    
    # Test the custom query
    query = manager.get_query("fictionallang")
    print(f"Custom query loaded: {len(query) > 0}")
    
    # Show updated statistics
    stats = manager.get_statistics()
    print(f"Updated total languages: {stats['total_languages']}")
    
    # Remove the custom query
    print("\nRemoving custom query...")
    removed = manager.remove_custom_query("fictionallang")
    print(f"Removed: {removed}")
    
    # Verify removal
    query = manager.get_query("fictionallang")
    print(f"Query still exists: {query is not None}")


def demonstrate_file_watching():
    """Demonstrate real-time file watching"""
    print(f"\n👁️  File Watching Demo")
    print("-" * 30)
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create query manager watching temp directory
        manager = QueryManager(queries_dir=str(temp_path), enable_watching=True)
        
        print(f"Watching directory: {temp_dir}")
        
        # Create a new query file
        test_query = """
; Test language
(test_function
  name: (identifier) @name.definition.function) @definition.function
        """.strip()
        
        test_file = temp_path / "tree-sitter-testlang-tags.scm"
        print(f"Creating file: {test_file.name}")
        
        # Wait a moment for file system events
        time.sleep(0.1)
        test_file.write_text(test_query)
        time.sleep(0.5)  # Allow file watcher to process
        
        # Check if query was loaded
        query = manager.get_query("testlang")
        print(f"Query loaded: {len(query) > 0}")
        
        # Modify the file
        print("Modifying file...")
        modified_query = test_query + "\n\n; Added comment\n"
        test_file.write_text(modified_query)
        time.sleep(0.5)
        
        # Check update history
        history = manager.get_update_history(5)
        print(f"Recent updates: {len(history)}")
        for event in history[-2:]:  # Show last 2 events
            print(f"  - {event.language}: {event.event_type} at {event.timestamp.strftime('%H:%M:%S')}")
        
        # Delete the file
        print("Deleting file...")
        test_file.unlink()
        time.sleep(0.5)
        
        # Verify removal
        query = manager.get_query("testlang")
        print(f"Query still exists after deletion: {query is not None}")


def demonstrate_export_import(manager: QueryManager):
    """Demonstrate export/import functionality"""
    print(f"\n📤 Export/Import Demo")
    print("-" * 25)
    
    # Export queries
    export_file = "queries_export.json"
    print(f"Exporting queries to {export_file}...")
    success = manager.export_queries(export_file)
    print(f"Export successful: {success}")
    
    if success:
        # Check file size
        export_path = Path(export_file)
        if export_path.exists():
            size_kb = export_path.stat().st_size / 1024
            print(f"Export file size: {size_kb:.1f} KB")
            
            # Clean up
            export_path.unlink()
            print("Export file cleaned up")


def demonstrate_statistics(manager: QueryManager):
    """Demonstrate statistics and monitoring"""
    print(f"\n📈 Statistics & Monitoring")
    print("-" * 30)
    
    # Get detailed statistics
    stats = manager.get_statistics()
    
    print("Current Statistics:")
    for key, value in stats.items():
        if key == "last_update" and value:
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")
    
    # Show update history
    history = manager.get_update_history(10)
    print(f"\nRecent Update History ({len(history)} events):")
    for event in history[-5:]:  # Show last 5 events
        status = "✅" if event.event_type != "error" else "❌"
        print(f"  {status} {event.language}: {event.event_type} at {event.timestamp.strftime('%H:%M:%S')}")


def main():
    """Run all demonstrations"""
    print("🎯 Query Manager Comprehensive Demo")
    print("=" * 60)
    
    try:
        # Basic usage
        manager = demonstrate_basic_usage()
        
        # Custom queries
        demonstrate_custom_queries(manager)
        
        # File watching (in temp directory)
        demonstrate_file_watching()
        
        # Export/import
        demonstrate_export_import(manager)
        
        # Statistics
        demonstrate_statistics(manager)
        
        print(f"\n✅ Demo completed successfully!")
        print(f"💡 The QueryManager is now ready for production use with:")
        print(f"   - Real-time file watching")
        print(f"   - Dynamic query updates")
        print(f"   - Custom language support")
        print(f"   - Export/import capabilities")
        print(f"   - Comprehensive monitoring")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
