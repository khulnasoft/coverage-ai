# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-01-22

### Added
- **Major Language Expansion**: Added support for 20 new programming languages
  - Arduino, Chatito, Clojure, Common Lisp, D, Dart, Gleam, Lua, MATLAB, Pony, Properties, R, Racket, Solidity, Swift, Udev, Fortran, Haskell, HCL, Julia, Kotlin, Scala
- **Total Language Support**: Now supports 39 programming languages (up from 19)
- **Flexible Query Loading**: Enhanced `get_queries.py` to support both naming conventions:
  - Standard: `tree-sitter-{lang}-tags.scm`
  - Special: `{lang}-tags.scm` (for languages like Zig)
- **Comprehensive Testing**: Added complete test suite for query loading
- **Performance Benchmarking**: Added benchmark script for query loading performance
- **Documentation**: Created comprehensive guide for adding new languages
- **Usage Examples**: Added FileMap usage examples for multiple languages

### Improved
- **Query Loading Performance**: All 39 languages load in under 5ms (4.37ms average)
- **Error Handling**: Better handling of missing or malformed query files
- **Memory Efficiency**: Estimated 39KB memory footprint for all queries
- **Robustness**: Added edge case handling for empty/malformed files

### Fixed
- **Query Loading**: Fixed issues with language detection and file loading
- **Naming Convention Support**: Properly handles both standard and special naming patterns

### Technical Details
- **Test Coverage**: 9 comprehensive test cases covering all scenarios
- **Performance Metrics**: Average 0.10ms per language loading time
- **Memory Usage**: ~1KB per language on average
- **Supported File Types**: 39 different programming language file extensions

### Documentation
- Added `docs/adding_new_languages.md` - Complete guide for adding new languages
- Added `examples/filemap_usage_examples.py` - Usage examples for all major languages
- Added `tests/test_get_queries.py` - Comprehensive test suite
- Added `benchmark_queries.py` - Performance benchmarking tool

### Breaking Changes
- Updated FileMap class docstring to reflect new supported languages
- Enhanced query loading logic (backward compatible)

## [1.0.0] - Previous Release

### Added
- Initial FileMap implementation with tree-sitter support
- Support for 19 core programming languages
- Basic query loading functionality
