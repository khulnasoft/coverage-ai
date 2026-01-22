; Gleam language tags for repomap
; Based on Gleam grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable bindings
(binding
  name: (identifier) @name.definition.variable) @definition.variable

; Type definitions
(type_definition
  name: (type_name) @name.definition.type) @definition.type

; Type alias definitions
(type_alias_definition
  name: (type_name) @name.definition.type) @definition.type

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (module_access
    name: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
(type_name) @ref
