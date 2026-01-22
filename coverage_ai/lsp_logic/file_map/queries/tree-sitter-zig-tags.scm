; Zig language tags for repomap
; Based on Zig grammar and common patterns

; Function definitions
(FunctionDecl
  name: (IDENTIFIER) @name.definition.function) @definition.function

; Struct definitions
(ContainerDecl
  (ContainerField
    name: (IDENTIFIER) @name.definition.class)) @definition.class

; Enum definitions
(ContainerDecl
  (ContainerField
    name: (IDENTIFIER) @name.definition.enum)) @definition.enum

; Union definitions
(ContainerDecl
  (ContainerField
    name: (IDENTIFIER) @name.definition.union)) @definition.union

; Variable declarations (const, var)
(ConstDecl
  name: (IDENTIFIER) @name.definition.variable) @definition.variable

(VarDecl
  name: (IDENTIFIER) @name.definition.variable) @definition.variable

; Global declarations
(GlobalDecl
  name: (IDENTIFIER) @name.definition.variable) @definition.variable

; Test declarations
(TestDecl
  name: (IDENTIFIER) @name.definition.function) @definition.function

; Function calls
(CallExpr
  function: (IDENTIFIER) @name.reference.call) @reference.call

(CallExpr
  function: (FieldExpr
    field: (IDENTIFIER) @name.reference.call)) @reference.call

; References to variables/constants
(Identifier) @ref

; Type definitions
(TypeExpr
  (IDENTIFIER) @name.reference.type) @reference.type

; Parameter names
(ParamDecl
  name: (IDENTIFIER) @name.definition.parameter) @definition.parameter

; Error set definitions
(ErrorSetDecl
  name: (IDENTIFIER) @name.definition.error) @definition.error

; Comptime function declarations
(ComptimeDecl
  (FunctionDecl
    name: (IDENTIFIER) @name.definition.function)) @definition.function

; Pub function declarations
(PubDecl
  (FunctionDecl
    name: (IDENTIFIER) @name.definition.function)) @definition.function

; Pub struct/enum/union declarations
(PubDecl
  (ContainerDecl
    (ContainerField
      name: (IDENTIFIER) @name.definition.class))) @definition.class

; Using namespace
(UsingDecl
  namespace: (IDENTIFIER) @name.reference.namespace) @reference.namespace

; Import declarations
(ImportDecl
  import: (IDENTIFIER) @name.reference.module) @reference.module
