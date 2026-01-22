; Solidity language tags for repomap
; Based on Solidity grammar patterns

; Function definitions
(function_definition
  name: (identifier) @name.definition.function) @definition.function

; Constructor definitions
(constructor_definition
  name: (identifier) @name.definition.function) @definition.function

; Fallback/receive functions
(fallback_function) @definition.function
(receive_function) @definition.function

; Variable declarations
(state_variable_declaration
  (variable_declaration
    name: (identifier) @name.definition.variable)) @definition.variable

; Contract definitions
(contract_definition
  name: (identifier) @name.definition.class) @definition.class

; Interface definitions
(interface_definition
  name: (identifier) @name.definition.class) @definition.class

; Library definitions
(library_definition
  name: (identifier) @name.definition.class) @definition.class

; Struct definitions
(struct_definition
  name: (identifier) @name.definition.class) @definition.class

; Enum definitions
(enum_definition
  name: (identifier) @name.definition.enum) @definition.enum

; Event definitions
(event_definition
  name: (identifier) @name.definition.event) @definition.event

; Modifier definitions
(modifier_definition
  name: (identifier) @name.definition.function) @definition.function

; Function calls
(member_expression
  property: (identifier) @name.reference.call) @reference.call

(call_expression
  callee: (identifier) @name.reference.call) @reference.call

; References to variables/types
(identifier) @ref
