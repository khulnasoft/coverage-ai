; Julia language tags for repomap
; Based on Julia grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Short function definitions
(short_function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable assignments
(assignment
  left: (identifier) @name.definition.variable) @definition.variable

; Constant assignments (const)
(const_statement
  (assignment
    left: (identifier) @name.definition.variable)) @definition.variable

; Struct definitions
(struct_definition
  name: (identifier) @name.definition.class) @definition.class

; Abstract type definitions
(abstract_type_definition
  name: (identifier) @name.definition.type) @definition.type

; Primitive type definitions
(primitive_type_definition
  name: (identifier) @name.definition.type) @definition.type

; Module definitions
(module_definition
  name: (identifier) @name.definition.module) @definition.module

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (field_expression
    field: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
