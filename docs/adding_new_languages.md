# Adding New Languages to Tree-Sitter Query System

This guide explains how to add support for new programming languages to the tree-sitter query system used by the FileMap class.

## Overview

The FileMap class uses tree-sitter queries to analyze code structure and extract definitions, references, and other semantic information. Each language needs a query file that defines patterns for identifying language constructs.

## File Structure

Query files are located in:
```
coverage_ai/lsp_logic/file_map/queries/
```

Two naming conventions are supported:
1. **Standard**: `tree-sitter-{language}-tags.scm` (e.g., `tree-sitter-python-tags.scm`)
2. **Special**: `{language}-tags.scm` (e.g., `zig-tags.scm`)

## Step-by-Step Guide

### 1. Create Query File

Create a new query file with the appropriate naming convention:
```bash
# Standard naming (recommended)
touch coverage_ai/lsp_logic/file_map/queries/tree-sitter-mylang-tags.scm

# Special naming (for languages with unique requirements)
touch coverage_ai/lsp_logic/file_map/queries/mylang-tags.scm
```

### 2. Define Query Patterns

Add tree-sitter query patterns to identify language constructs. Common patterns include:

#### Basic Structure
```scheme
; Language name tags for repomap
; Based on {language} grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(variable_declaration
  name: (identifier) @name.definition.variable) @definition.variable

; Class/struct definitions
(class_definition
  name: (identifier) @name.definition.class) @definition.class

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

; References
(identifier) @ref
```

#### Common Tag Types

- **Definitions**: `@name.definition.function`, `@name.definition.class`, `@name.definition.variable`, `@name.definition.enum`
- **References**: `@name.reference.call`, `@name.reference.type`, `@name.reference.module`
- **General**: `@ref` (for any identifier)

### 3. Language-Specific Patterns

Different languages have different grammar structures. Here are examples:

#### Functional Languages (Haskell, Lisp)
```scheme
; Function definitions
(function
  name: (variable) @name.definition.function) @definition.function

; Pattern matching
(pattern_function
  name: (variable) @name.definition.function) @definition.function
```

#### Object-Oriented Languages (Java, C++)
```scheme
; Class definitions
(class_declaration
  name: (identifier) @name.definition.class) @definition.class

; Method definitions
(method_declaration
  name: (identifier) @name.definition.function) @definition.function
```

#### Markup/Configuration Languages
```scheme
; Property keys
(property
  key: (identifier) @name.definition.variable) @definition.variable
```

### 4. Test the Query

Use the built-in testing framework:

```python
from coverage_ai.lsp_logic.file_map.queries.get_queries import get_queries_scheme

# Test query loading
queries = get_queries_scheme("mylang")
print(f"Loaded {len(queries)} characters of queries")
```

Run the test suite:
```bash
python -m pytest tests/test_get_queries.py -v
```

### 5. Update Documentation

Update the FileMap class docstring to include the new language:

```python
"""
Supported languages: Arduino, C, C++, C#, ..., MyLang, ...
"""
```

## Query Pattern Examples

### Python
```scheme
; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Class definitions
(class_definition
  name: (identifier) @name.definition.class) @definition.class
```

### JavaScript
```scheme
; Function declarations
(function_declaration
  name: (identifier) @name.definition.function) @definition.function

; Arrow functions
(arrow_function
  (identifier) @name.definition.function) @definition.function
```

### Rust
```scheme
; Function definitions
(function_item
  name: (identifier) @name.definition.function) @definition.function

; Struct definitions
(struct_item
  name: (type_identifier) @name.definition.class) @definition.class
```

## Best Practices

1. **Use Standard Naming**: Prefer `tree-sitter-{lang}-tags.scm` unless there's a specific reason for special naming
2. **Include Comments**: Add comments explaining the language and patterns
3. **Test Thoroughly**: Use the test suite to ensure queries load correctly
4. **Follow Patterns**: Use consistent tag naming conventions
5. **Handle Edge Cases**: Consider different declaration styles and language features

## Common Pitfalls

1. **Incorrect Grammar**: Using node names that don't exist in the language's tree-sitter grammar
2. **Missing Patterns**: Forgetting to handle common constructs like imports or exports
3. **Inconsistent Naming**: Using different tag names for similar constructs
4. **Performance Issues**: Creating overly complex queries that slow down parsing

## Debugging Queries

If queries don't work as expected:

1. **Check Grammar**: Verify node names against the language's tree-sitter grammar
2. **Test with Examples**: Use simple code samples to test individual patterns
3. **Use Tree-Sitter CLI**: Debug queries with the official tree-sitter command-line tools
4. **Review Similar Languages**: Look at existing query files for similar languages

## Validation

After adding a new language:

1. Run the test suite: `python -m pytest tests/test_get_queries.py -v`
2. Test with actual code files in the target language
3. Verify the FileMap class can process files correctly
4. Update any relevant documentation

## Performance Considerations

- Keep queries as simple as possible
- Avoid overly complex patterns
- Test performance with large codebases
- Use the benchmark script: `python benchmark_queries.py`

## Getting Help

- Reference existing query files in the `queries/` directory
- Check tree-sitter language documentation
- Look at the official tree-sitter query patterns
- Review language-specific grammar files
