; Swift language tags for repomap
; Based on Swift grammar patterns

; Function definitions
(function_declaration
  name: (identifier) @name.definition.function) @definition.function

; Method definitions
(method_declaration
  name: (identifier) @name.definition.function) @definition.function

; Initializer definitions
(initializer_declaration) @definition.function

; Variable declarations
(variable_declaration
  (pattern
    (identifier) @name.definition.variable)) @definition.variable

; Constant declarations
(let_declaration
  (pattern
    (identifier) @name.definition.variable)) @definition.variable

; Class definitions
(class_declaration
  name: (type_identifier) @name.definition.class) @definition.class

; Struct definitions
(struct_declaration
  name: (type_identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_declaration
  name: (type_identifier) @name.definition.enum) @definition.enum

; Protocol definitions
(protocol_declaration
  name: (type_identifier) @name.definition.class) @definition.class

; Extension declarations
(extension_declaration
  type: (user_type
    (type_identifier) @name.definition.class)) @definition.class

; Function calls
(call_expression
  callee: (identifier) @name.reference.call) @reference.call

(call_expression
  callee: (member_expression
    property: (identifier) @name.reference.call)) @reference.call

; References to variables/types
(identifier) @ref
(type_identifier) @ref
