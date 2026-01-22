"""
AI-Driven Code Analysis Pipeline
Integrates FileMap with AI summarization for intelligent code analysis.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from coverage_ai.lsp_logic.file_map.file_map import FileMap
from coverage_ai.ai_caller import AiCaller


@dataclass
class AnalysisResult:
    """Result of code analysis for a single file"""
    file_path: str
    language: str
    definitions: List[Dict[str, Any]]
    references: List[Dict[str, Any]]
    summary: str
    complexity_score: float
    lines_of_code: int
    processing_time: float


@dataclass
class ProjectAnalysis:
    """Analysis results for an entire project"""
    project_path: str
    total_files: int
    analyzed_files: int
    supported_languages: List[str]
    results: List[AnalysisResult]
    total_processing_time: float
    project_summary: str


class CodeAnalyzer:
    """
    AI-driven code analysis pipeline using FileMap for structure extraction
    and AI models for intelligent summarization and analysis.
    """
    
    def __init__(self, 
                 ai_caller: Optional[AiCaller] = None,
                 max_workers: int = 4,
                 enable_ai_summary: bool = True):
        """
        Initialize the code analyzer.
        
        Args:
            ai_caller: AI caller for generating summaries
            max_workers: Maximum number of parallel workers
            enable_ai_summary: Whether to generate AI summaries
        """
        self.ai_caller = ai_caller
        self.max_workers = max_workers
        self.enable_ai_summary = enable_ai_summary
        
        # Supported file extensions
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript', '.jsx': 'javascript', '.ts': 'typescript', '.tsx': 'typescript',
            '.java': 'java',
            '.c': 'c', '.h': 'c',
            '.cpp': 'cpp', '.cxx': 'cpp', '.cc': 'cpp', '.hpp': 'cpp', '.hxx': 'cpp',
            '.cs': 'c_sharp',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.hs': 'haskell',
            '.ml': 'ocaml', '.mli': 'ocaml',
            '.php': 'php',
            '.rb': 'ruby',
            '.r': 'r', '.R': 'r',
            '.dart': 'dart',
            '.lua': 'lua',
            '.m': 'matlab',
            '.sol': 'solidity',
            '.zig': 'zig',
            '.elm': 'elm',
            '.clj': 'clojure',
            '.lisp': 'commonlisp',
            '.d': 'd',
            '.ex': 'elixir',
            '.gleam': 'gleam',
            '.pony': 'pony',
            '.properties': 'properties',
            '.rkt': 'racket',
            '.hcl': 'hcl',
            '.jl': 'julia',
            '.f': 'fortran', '.f90': 'fortran', '.F90': 'fortran',
            '.arduino': 'arduino', '.ino': 'arduino',
            '.udev': 'udev',
            '.chatito': 'chatito'
        }
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        suffix = Path(file_path).suffix.lower()
        return self.supported_extensions.get(suffix)
    
    def analyze_file(self, file_path: str, project_base: Optional[str] = None) -> Optional[AnalysisResult]:
        """
        Analyze a single file using FileMap and AI summarization.
        
        Args:
            file_path: Path to the file to analyze
            project_base: Base path of the project for relative paths
            
        Returns:
            AnalysisResult with file structure and AI summary
        """
        start_time = time.time()
        
        try:
            # Detect language
            language = self.detect_language(file_path)
            if not language:
                return None
            
            # Create FileMap instance
            filemap = FileMap(
                fname_full_path=file_path,
                project_base_path=project_base,
                parent_context=True,
                child_context=False,
                header_max=5
            )
            
            # Get structure information
            summary = filemap.summarize()
            
            # Extract definitions and references
            query_results = filemap.get_query_results()
            if query_results:
                results, captures = query_results
                
                definitions = [r for r in results if r['kind'] == 'def']
                references = [r for r in results if r['kind'] == 'ref']
            else:
                definitions = []
                references = []
            
            # Calculate complexity metrics
            complexity_score = self._calculate_complexity(definitions, references, file_path)
            
            # Count lines of code
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines_of_code = len([line for line in f if line.strip()])
            except:
                lines_of_code = 0
            
            # Generate AI summary if enabled
            ai_summary = ""
            if self.enable_ai_summary and self.ai_caller and definitions:
                ai_summary = self._generate_ai_summary(file_path, language, definitions, summary)
            
            processing_time = time.time() - start_time
            
            return AnalysisResult(
                file_path=file_path,
                language=language,
                definitions=definitions,
                references=references,
                summary=ai_summary or summary,
                complexity_score=complexity_score,
                lines_of_code=lines_of_code,
                processing_time=processing_time
            )
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _calculate_complexity(self, definitions: List[Dict], references: List[Dict], file_path: str) -> float:
        """Calculate a simple complexity score based on definitions and references"""
        try:
            # Basic complexity metrics
            def_count = len(definitions)
            ref_count = len(references) if references else 0
            
            # File size factor
            file_size = os.path.getsize(file_path) / 1024  # KB
            
            # Complexity score (0-100 scale)
            base_score = (def_count * 10 + ref_count * 2)
            size_factor = min(file_size / 100, 20)  # Max 20 points for size
            
            complexity = min(base_score + size_factor, 100)
            return round(complexity, 2)
            
        except:
            return 0.0
    
    def _generate_ai_summary(self, file_path: str, language: str, 
                           definitions: List[Dict], structure_summary: str) -> str:
        """Generate AI-powered summary of the file"""
        if not self.ai_caller:
            return ""
        
        try:
            # Prepare context for AI
            def_info = []
            for definition in definitions[:10]:  # Limit to first 10 definitions
                def_info.append(f"- {definition['name']} ({definition['kind']}) at line {definition['line']}")
            
            prompt = f"""
            Analyze this {language} code file and provide a concise summary:
            
            File: {file_path}
            
            Key definitions found:
            {chr(10).join(def_info)}
            
            Structure summary:
            {structure_summary}
            
            Provide a brief summary (2-3 sentences) describing what this file does and its main components.
            """
            
            # Call AI (implementation depends on your AI caller)
            response = self.ai_caller.call_ai(prompt)
            return response.strip() if response else ""
            
        except Exception as e:
            print(f"Error generating AI summary for {file_path}: {e}")
            return ""
    
    def analyze_project(self, project_path: str, 
                       max_files: Optional[int] = None) -> ProjectAnalysis:
        """
        Analyze an entire project directory.
        
        Args:
            project_path: Path to the project directory
            max_files: Maximum number of files to analyze (for large projects)
            
        Returns:
            ProjectAnalysis with comprehensive results
        """
        start_time = time.time()
        
        # Find all code files
        code_files = []
        for root, dirs, files in os.walk(project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 
                                                   '.venv', 'venv', 'target', 'build']]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self.detect_language(file_path):
                    code_files.append(file_path)
        
        if max_files:
            code_files = code_files[:max_files]
        
        # Analyze files in parallel
        results = []
        supported_languages = set()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all files for analysis
            future_to_file = {
                executor.submit(self.analyze_file, file_path, project_path): file_path 
                for file_path in code_files
            }
            
            # Collect results
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    results.append(result)
                    supported_languages.add(result.language)
        
        total_time = time.time() - start_time
        
        # Generate project summary
        project_summary = self._generate_project_summary(results, supported_languages)
        
        return ProjectAnalysis(
            project_path=project_path,
            total_files=len(code_files),
            analyzed_files=len(results),
            supported_languages=list(supported_languages),
            results=results,
            total_processing_time=total_time,
            project_summary=project_summary
        )
    
    def _generate_project_summary(self, results: List[AnalysisResult], 
                                languages: set) -> str:
        """Generate a summary of the entire project"""
        if not results:
            return "No analyzable files found."
        
        total_defs = sum(len(r.definitions) for r in results)
        total_refs = sum(len(r.references) for r in results)
        total_loc = sum(r.lines_of_code for r in results)
        avg_complexity = sum(r.complexity_score for r in results) / len(results)
        
        language_counts = {}
        for result in results:
            language_counts[result.language] = language_counts.get(result.language, 0) + 1
        
        top_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary = f"""
Project Analysis Summary:
- Total files analyzed: {len(results)}
- Lines of code: {total_loc:,}
- Total definitions: {total_defs}
- Average complexity: {avg_complexity:.1f}/100
- Top languages: {', '.join([f'{lang} ({count})' for lang, count in top_languages])}
        """.strip()
        
        return summary
    
    def export_results(self, analysis: ProjectAnalysis, output_path: str, format: str = 'json'):
        """Export analysis results to file"""
        if format.lower() == 'json':
            self._export_json(analysis, output_path)
        elif format.lower() == 'csv':
            self._export_csv(analysis, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, analysis: ProjectAnalysis, output_path: str):
        """Export results as JSON"""
        data = {
            'project_path': analysis.project_path,
            'summary': analysis.project_summary,
            'metrics': {
                'total_files': analysis.total_files,
                'analyzed_files': analysis.analyzed_files,
                'supported_languages': analysis.supported_languages,
                'total_processing_time': analysis.total_processing_time
            },
            'files': []
        }
        
        for result in analysis.results:
            data['files'].append({
                'path': result.file_path,
                'language': result.language,
                'definitions_count': len(result.definitions),
                'references_count': len(result.references),
                'complexity_score': result.complexity_score,
                'lines_of_code': result.lines_of_code,
                'processing_time': result.processing_time,
                'summary': result.summary
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, analysis: ProjectAnalysis, output_path: str):
        """Export results as CSV"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'File Path', 'Language', 'Definitions', 'References', 
                'Complexity', 'Lines of Code', 'Processing Time', 'Summary'
            ])
            
            for result in analysis.results:
                writer.writerow([
                    result.file_path,
                    result.language,
                    len(result.definitions),
                    len(result.references),
                    result.complexity_score,
                    result.lines_of_code,
                    result.processing_time,
                    result.summary
                ])


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CodeAnalyzer(enable_ai_summary=False)  # Set to True with AI caller
    
    # Analyze current directory
    project_path = "/Users/khulnasoft/Work/coverage-ai"
    analysis = analyzer.analyze_project(project_path, max_files=50)
    
    print(analysis.project_summary)
    
    # Export results
    analyzer.export_results(analysis, "project_analysis.json", "json")
    analyzer.export_results(analysis, "project_analysis.csv", "csv")
    
    print(f"\nAnalysis completed in {analysis.total_processing_time:.2f}s")
    print(f"Analyzed {analysis.analyzed_files}/{analysis.total_files} files")
