; Lua language tags for repomap
; Based on Lua grammar patterns

; Function definitions
(function_declaration
  name: (identifier) @name.definition.function) @definition.function

; Local function definitions
(local_function_declaration
  name: (identifier) @name.definition.function) @definition.function

; Variable assignments
(assignment_statement
  (variable_list
    (identifier) @name.definition.variable)) @definition.variable

; Local variable declarations
(local_declaration
  (variable_list
    (identifier) @name.definition.variable)) @definition.variable

; Function calls
(function_call
  name: (identifier) @name.reference.call) @reference.call

(function_call
  name: (dot_index_expression
    field: (identifier) @name.reference.call)) @reference.call

; Method calls
(function_call
  name: (method_index_expression
    method: (identifier) @name.reference.call)) @reference.call

; References to variables
(identifier) @ref
