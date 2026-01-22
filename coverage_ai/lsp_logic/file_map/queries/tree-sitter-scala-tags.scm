; Scala language tags for repomap
; Based on Scala grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(val_definition
  name: (identifier) @name.definition.variable) @definition.variable

(var_definition
  name: (identifier) @name.definition.variable) @definition.variable

; Class definitions
(class_definition
  name: (identifier) @name.definition.class) @definition.class

; Object definitions
(object_definition
  name: (identifier) @name.definition.class) @definition.class

; Trait definitions
(trait_definition
  name: (identifier) @name.definition.class) @definition.class

; Case class definitions
(case_class_definition
  name: (identifier) @name.definition.class) @definition.class

; Package definitions
(package_definition
  name: (identifier) @name.definition.module) @definition.module

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (field_expression
    field: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
