; Fortran language tags for repomap
; Based on Fortran grammar patterns

; Function definitions
(function_statement
  name: (identifier) @name.definition.function) @definition.function

; Subroutine definitions
(subroutine_statement
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(entity_declaration
  (entity_decl
    (identifier) @name.definition.variable)) @definition.variable

; Type definitions
(derived_type_statement
  name: (identifier) @name.definition.class) @definition.class

; Module definitions
(module_statement
  name: (identifier) @name.definition.module) @definition.module

; Program definitions
(program_statement
  name: (identifier) @name.definition.class) @definition.class

; Function calls
(call_statement
  name: (identifier) @name.reference.call) @reference.call

; References to variables/types
(identifier) @ref
