; Kotlin language tags for repomap
; Based on Kotlin grammar patterns

; Function definitions
(function_declaration
  name: (simple_identifier) @name.definition.function) @definition.function

; Variable declarations
(property_declaration
  name: (simple_identifier) @name.definition.variable) @definition.variable

(val_declaration
  name: (simple_identifier) @name.definition.variable) @definition.variable

(var_declaration
  name: (simple_identifier) @name.definition.variable) @definition.variable

; Class definitions
(class_declaration
  name: (type_identifier) @name.definition.class) @definition.class

; Object declarations
(object_declaration
  name: (simple_identifier) @name.definition.class) @definition.class

; Interface definitions
(interface_declaration
  name: (type_identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_class
  name: (type_identifier) @name.definition.enum) @definition.enum

; Companion object
(companion_object) @definition.class

; Function calls
(call_expression
  (simple_identifier) @name.reference.call) @reference.call

(call_expression
  (navigation_expression
    (simple_identifier) @name.reference.call)) @reference.call

; References to variables/types
(simple_identifier) @ref
(type_identifier) @ref
