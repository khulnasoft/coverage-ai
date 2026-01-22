; Pony language tags for repomap
; Based on Pony grammar patterns

; Function definitions
(method
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(variable
  name: (identifier) @name.definition.variable) @definition.variable

; Class definitions
(class
  name: (identifier) @name.definition.class) @definition.class

; Actor definitions
(actor
  name: (identifier) @name.definition.class) @definition.class

; Primitive definitions
(primitive
  name: (identifier) @name.definition.class) @definition.class

; Trait definitions
(trait
  name: (identifier) @name.definition.class) @definition.class

; Interface definitions
(interface
  name: (identifier) @name.definition.class) @definition.class

; Function calls
(call
  receiver: (identifier) @name.reference.call) @reference.call

(call
  receiver: (dot
    right: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
