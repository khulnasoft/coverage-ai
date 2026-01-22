; Haskell language tags for repomap
; Based on Haskell grammar patterns

; Function definitions
(function
  name: (variable) @name.definition.function) @definition.function

; Pattern function definitions
(pattern_function
  name: (variable) @name.definition.function) @definition.function

; Variable bindings (let, where)
(bind
  name: (variable) @name.definition.variable) @definition.variable

; Type signatures
(signature
  name: (variable) @name.definition.function) @definition.function

; Type definitions
(data_type
  name: (type) @name.definition.type) @definition.type

; Newtype definitions
(newtype
  name: (type) @name.definition.type) @definition.type

; Type class definitions
(class
  name: (type) @name.definition.class) @definition.class

; Instance definitions
(instance
  name: (type) @name.definition.class) @definition.class

; Module definitions
(module
  name: (module_name) @name.definition.module) @definition.module

; Function calls
(infix
  left: (variable) @name.reference.call) @reference.call

(apply
  function: (variable) @name.reference.call) @reference.call

; References to variables/types
(variable) @ref
(type) @ref
