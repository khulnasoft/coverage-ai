; MATLAB language tags for repomap
; Based on MATLAB grammar patterns

; Function definitions
(function
  name: (identifier) @name.definition.function) @definition.function

; Variable assignments
(assignment
  left: (identifier) @name.definition.variable) @definition.variable

; Function calls
(call
  function: (identifier) @name.reference.call) @reference.call

(call
  function: (dot_expression
    right: (identifier) @name.reference.call)) @reference.call

; References to variables
(identifier) @ref
