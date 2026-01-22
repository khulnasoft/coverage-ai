; Arduino language tags for repomap
; Based on C++ grammar with Arduino-specific patterns

; Function definitions
(function_definition
  declarator: (function_declarator
    declarator: (identifier) @name.definition.function)) @definition.function

; Variable declarations
(declaration
  declarator: (init_declarator
    declarator: (identifier) @name.definition.variable)) @definition.variable

; Class definitions
(class_specifier
  name: (type_identifier) @name.definition.class) @definition.class

; Struct definitions
(struct_specifier
  name: (type_identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_specifier
  name: (type_identifier) @name.definition.enum) @definition.enum

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (field_expression
    field: (field_identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
(type_identifier) @ref
