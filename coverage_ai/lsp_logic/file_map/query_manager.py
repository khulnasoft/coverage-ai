"""
Dynamic Query Manager for Real-Time Updates
Supports evolving languages and custom grammars.
"""

import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from coverage_ai.lsp_logic.file_map.queries.get_queries import get_queries_scheme


@dataclass
class QueryInfo:
    """Information about a query file"""
    language: str
    file_path: str
    content_hash: str
    last_modified: datetime
    size_bytes: int
    is_valid: bool
    error_message: Optional[str] = None


@dataclass
class QueryUpdateEvent:
    """Event representing a query update"""
    language: str
    event_type: str  # 'created', 'modified', 'deleted', 'error'
    timestamp: datetime
    file_path: str
    previous_hash: Optional[str] = None
    new_hash: Optional[str] = None
    error_message: Optional[str] = None


class QueryFileWatcher(FileSystemEventHandler):
    """File system watcher for query files"""
    
    def __init__(self, query_manager: 'QueryManager'):
        self.query_manager = query_manager
        
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.scm'):
            self.query_manager._handle_file_change('modified', event.src_path)
            
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.scm'):
            self.query_manager._handle_file_change('created', event.src_path)
            
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.scm'):
            self.query_manager._handle_file_change('deleted', event.src_path)


class QueryManager:
    """
    Dynamic query manager that supports real-time updates for evolving languages
    and custom grammars.
    """
    
    def __init__(self, 
                 queries_dir: Optional[str] = None,
                 enable_watching: bool = True,
                 update_callbacks: Optional[List[Callable]] = None):
        """
        Initialize the query manager.
        
        Args:
            queries_dir: Directory containing query files (auto-detected if None)
            enable_watching: Enable file system watching for real-time updates
            update_callbacks: Callback functions to call on query updates
        """
        self.queries_dir = Path(queries_dir) if queries_dir else Path(__file__).parent / "queries"
        self.enable_watching = enable_watching
        self.update_callbacks = update_callbacks or []
        
        # Query cache and metadata
        self._query_cache: Dict[str, str] = {}
        self._query_info: Dict[str, QueryInfo] = {}
        self._update_history: List[QueryUpdateEvent] = []
        
        # File watching
        self._observer = None
        self._watch_thread = None
        self._lock = threading.RLock()
        
        # Initialize
        self._load_all_queries()
        if self.enable_watching:
            self._start_watching()
    
    def _load_all_queries(self):
        """Load all query files and build cache"""
        with self._lock:
            self._query_cache.clear()
            self._query_info.clear()
            
            for query_file in self.queries_dir.glob("*.scm"):
                language = self._extract_language_from_filename(query_file.name)
                if language:
                    self._load_query_file(language, query_file)
    
    def _extract_language_from_filename(self, filename: str) -> Optional[str]:
        """Extract language name from query filename"""
        if filename.startswith("tree-sitter-") and filename.endswith("-tags.scm"):
            # tree-sitter-{lang}-tags.scm
            return filename[12:-9]  # Remove "tree-sitter-" and "-tags.scm"
        elif filename.endswith("-tags.scm"):
            # {lang}-tags.scm
            return filename[:-9]  # Remove "-tags.scm"
        return None
    
    def _load_query_file(self, language: str, file_path: Path):
        """Load a single query file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content_hash = hashlib.md5(content.encode()).hexdigest()
            stat = file_path.stat()
            
            # Validate query syntax
            is_valid, error_msg = self._validate_query_content(content)
            
            query_info = QueryInfo(
                language=language,
                file_path=str(file_path),
                content_hash=content_hash,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
                is_valid=is_valid,
                error_message=error_msg
            )
            
            self._query_cache[language] = content
            self._query_info[language] = query_info
            
        except Exception as e:
            # Store error info
            query_info = QueryInfo(
                language=language,
                file_path=str(file_path),
                content_hash="",
                last_modified=datetime.now(),
                size_bytes=0,
                is_valid=False,
                error_message=str(e)
            )
            self._query_info[language] = query_info
    
    def _validate_query_content(self, content: str) -> tuple[bool, Optional[str]]:
        """Validate query file content"""
        if not content.strip():
            return False, "Empty file"
        
        # Basic syntax checks
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens != close_parens:
            return False, f"Unbalanced parentheses: {open_parens} open, {close_parens} close"
        
        # Check for at least one query pattern
        if '@name.definition.' not in content and '@name.reference.' not in content:
            return False, "No definition or reference patterns found"
        
        return True, None
    
    def _start_watching(self):
        """Start file system watching"""
        try:
            self._observer = Observer()
            event_handler = QueryFileWatcher(self)
            self._observer.schedule(event_handler, str(self.queries_dir), recursive=False)
            self._observer.start()
        except Exception as e:
            print(f"Warning: Could not start file watching: {e}")
            self.enable_watching = False
    
    def _handle_file_change(self, event_type: str, file_path: str):
        """Handle file system events"""
        try:
            file_path_obj = Path(file_path)
            language = self._extract_language_from_filename(file_path_obj.name)
            
            if not language:
                return
            
            with self._lock:
                previous_hash = self._query_info.get(language, QueryInfo(
                    language="", file_path="", content_hash="", 
                    last_modified=datetime.now(), size_bytes=0, is_valid=False
                )).content_hash
                
                if event_type in ['created', 'modified']:
                    self._load_query_file(language, file_path_obj)
                    new_hash = self._query_info[language].content_hash
                elif event_type == 'deleted':
                    # Remove from cache
                    self._query_cache.pop(language, None)
                    self._query_info.pop(language, None)
                    new_hash = None
                
                # Create update event
                update_event = QueryUpdateEvent(
                    language=language,
                    event_type=event_type,
                    timestamp=datetime.now(),
                    file_path=file_path,
                    previous_hash=previous_hash,
                    new_hash=new_hash
                )
                
                self._update_history.append(update_event)
                
                # Notify callbacks
                self._notify_callbacks(update_event)
                
        except Exception as e:
            # Create error event
            error_event = QueryUpdateEvent(
                language=language or "unknown",
                event_type="error",
                timestamp=datetime.now(),
                file_path=file_path,
                error_message=str(e)
            )
            self._update_history.append(error_event)
            self._notify_callbacks(error_event)
    
    def _notify_callbacks(self, event: QueryUpdateEvent):
        """Notify all registered callbacks"""
        for callback in self.update_callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in update callback: {e}")
    
    def get_query(self, language: str) -> Optional[str]:
        """Get query for a language with caching"""
        with self._lock:
            return self._query_cache.get(language)
    
    def get_query_info(self, language: str) -> Optional[QueryInfo]:
        """Get metadata about a query"""
        with self._lock:
            return self._query_info.get(language)
    
    def list_supported_languages(self) -> List[str]:
        """List all supported languages"""
        with self._lock:
            return list(self._query_cache.keys())
    
    def get_update_history(self, limit: int = 50) -> List[QueryUpdateEvent]:
        """Get recent update history"""
        with self._lock:
            return self._update_history[-limit:]
    
    def reload_queries(self):
        """Manually reload all queries"""
        self._load_all_queries()
    
    def add_custom_query(self, language: str, query_content: str, 
                         file_path: Optional[str] = None) -> bool:
        """
        Add a custom query for a language.
        
        Args:
            language: Language identifier
            query_content: Query file content
            file_path: Optional file path to save the query
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate content
            is_valid, error_msg = self._validate_query_content(query_content)
            if not is_valid:
                return False
            
            # Save to file if path provided
            if file_path:
                file_path_obj = Path(file_path)
                file_path_obj.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path_obj, 'w', encoding='utf-8') as f:
                    f.write(query_content)
            
            # Update cache
            with self._lock:
                content_hash = hashlib.md5(query_content.encode()).hexdigest()
                self._query_cache[language] = query_content
                
                query_info = QueryInfo(
                    language=language,
                    file_path=file_path or f"<custom:{language}>",
                    content_hash=content_hash,
                    last_modified=datetime.now(),
                    size_bytes=len(query_content.encode()),
                    is_valid=True
                )
                self._query_info[language] = query_info
                
                # Create update event
                update_event = QueryUpdateEvent(
                    language=language,
                    event_type="created",
                    timestamp=datetime.now(),
                    file_path=file_path or f"<custom:{language}>",
                    new_hash=content_hash
                )
                self._update_history.append(update_event)
                self._notify_callbacks(update_event)
            
            return True
            
        except Exception as e:
            print(f"Error adding custom query: {e}")
            return False
    
    def remove_custom_query(self, language: str) -> bool:
        """Remove a custom query"""
        with self._lock:
            if language in self._query_cache:
                self._query_cache.pop(language, None)
                self._query_info.pop(language, None)
                
                update_event = QueryUpdateEvent(
                    language=language,
                    event_type="deleted",
                    timestamp=datetime.now(),
                    file_path=f"<custom:{language}>"
                )
                self._update_history.append(update_event)
                self._notify_callbacks(update_event)
                return True
            return False
    
    def export_queries(self, output_path: str, format: str = 'json') -> bool:
        """Export all queries to a file"""
        try:
            if format.lower() == 'json':
                data = {
                    'export_timestamp': datetime.now().isoformat(),
                    'total_languages': len(self._query_cache),
                    'queries': {}
                }
                
                for language, content in self._query_cache.items():
                    info = self._query_info.get(language)
                    data['queries'][language] = {
                        'content': content,
                        'info': asdict(info) if info else None
                    }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                return True
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            print(f"Error exporting queries: {e}")
            return False
    
    def import_queries(self, input_path: str, overwrite: bool = False) -> bool:
        """Import queries from a file"""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported_count = 0
            for language, query_data in data.get('queries', {}).items():
                if language not in self._query_cache or overwrite:
                    content = query_data.get('content', '')
                    if content and self.add_custom_query(language, content):
                        imported_count += 1
            
            return imported_count > 0
            
        except Exception as e:
            print(f"Error importing queries: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the query manager"""
        with self._lock:
            total_queries = len(self._query_cache)
            valid_queries = sum(1 for info in self._query_info.values() if info.is_valid)
            total_size = sum(info.size_bytes for info in self._query_info.values())
            
            recent_updates = len([e for e in self._update_history 
                                if (datetime.now() - e.timestamp).total_seconds() < 3600])
            
            return {
                'total_languages': total_queries,
                'valid_queries': valid_queries,
                'invalid_queries': total_queries - valid_queries,
                'total_size_bytes': total_size,
                'recent_updates_1h': recent_updates,
                'watching_enabled': self.enable_watching,
                'queries_directory': str(self.queries_dir),
                'last_update': self._update_history[-1].timestamp.isoformat() if self._update_history else None
            }
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if self._observer:
            self._observer.stop()
            self._observer.join()


# Global instance for easy access
_global_query_manager: Optional[QueryManager] = None


def get_global_query_manager() -> QueryManager:
    """Get the global query manager instance"""
    global _global_query_manager
    if _global_query_manager is None:
        _global_query_manager = QueryManager()
    return _global_query_manager


def reset_global_query_manager():
    """Reset the global query manager instance"""
    global _global_query_manager
    if _global_query_manager:
        del _global_query_manager
    _global_query_manager = None


# Example usage
if __name__ == "__main__":
    def on_query_update(event: QueryUpdateEvent):
        print(f"Query update: {event.language} - {event.event_type}")
    
    # Create query manager with callbacks
    manager = QueryManager(update_callbacks=[on_query_update])
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"Managing {stats['total_languages']} languages")
    
    # Add custom query
    custom_query = """
; Custom language example
(function_definition
  name: (identifier) @name.definition.function) @definition.function
    """.strip()
    
    manager.add_custom_query("mylang", custom_query)
    
    print(f"Supported languages: {manager.list_supported_languages()}")
