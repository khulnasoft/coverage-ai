; Dart language tags for repomap
; Based on Dart grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Method definitions
(method_definition
  name: (identifier) @name.definition.function) @definition.function

; Variable declarations
(variable_declaration
  name: (identifier) @name.definition.variable) @definition.variable

; Class definitions
(class_definition
  name: (identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_definition
  name: (identifier) @name.definition.enum) @definition.enum

; Mixin definitions
(mixin_definition
  name: (identifier) @name.definition.class) @definition.class

; Extension definitions
(extension_declaration
  name: (identifier) @name.definition.class) @definition.class

; Function calls
(call_expression
  function: (identifier) @name.reference.call) @reference.call

(call_expression
  function: (field_expression
    field: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
