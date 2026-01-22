; D language tags for repomap
; Based on D grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(variable_declaration
  (variable_declaration_item
    name: (identifier) @name.definition.variable)) @definition.variable

; Class definitions
(class_definition
  name: (identifier) @name.definition.class) @definition.class

; Struct definitions
(struct_definition
  name: (identifier) @name.definition.class) @definition.class

; Interface definitions
(interface_definition
  name: (identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_definition
  name: (identifier) @name.definition.enum) @definition.enum

; Module definitions
(module_declaration
  name: (identifier) @name.definition.module) @definition.module

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (dot_expression
    right: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
