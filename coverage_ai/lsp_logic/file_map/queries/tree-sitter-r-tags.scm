; R language tags for repomap
; Based on R grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable assignments
(assignment
  left: (identifier) @name.definition.variable) @definition.variable

; Variable definitions (<-)
(assignment
  left: (identifier) @name.definition.variable) @definition.variable

; Function calls
(call
  function: (identifier) @name.reference.call) @reference.call

(call
  function: (subset
    x: (identifier) @name.reference.call)) @reference.call

; References to variables
(identifier) @ref
