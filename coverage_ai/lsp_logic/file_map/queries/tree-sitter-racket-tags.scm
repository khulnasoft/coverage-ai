; Racket language tags for repomap
; Based on Racket/Scheme grammar patterns

; Function definitions (define)
(parenthesized_expression
  (identifier) @name.definition.function
  .) @definition.function

; Variable definitions (define)
(parenthesized_expression
  (identifier) @name.definition.variable
  .) @definition.variable

; Macro definitions (define-syntax)
(parenthesized_expression
  (identifier) @name.definition.function
  .) @definition.function

; Struct definitions (define-struct)
(parenthesized_expression
  (identifier) @name.definition.class
  .) @definition.class

; Class definitions (define-class)
(parenthesized_expression
  (identifier) @name.definition.class
  .) @definition.class

; Function calls
(parenthesized_expression
  . (identifier) @name.reference.call
  .) @reference.call

; References to symbols
(identifier) @ref
