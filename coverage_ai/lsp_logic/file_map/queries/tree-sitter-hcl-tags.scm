; HCL (HashiCorp Configuration Language) tags for repomap
; Based on HCL grammar patterns

; Variable definitions
(variable_declaration
  name: (identifier) @name.definition.variable) @definition.variable

; Resource definitions
(resource
  type: (identifier) @name.definition.class
  name: (identifier) @name.definition.variable) @definition.class

; Data source definitions
(data
  type: (identifier) @name.definition.class
  name: (identifier) @name.definition.variable) @definition.class

; Module definitions
(module
  name: (identifier) @name.definition.module) @definition.module

; Provider definitions
(provider
  name: (identifier) @name.definition.class) @definition.class

; Output definitions
(output
  name: (identifier) @name.definition.variable) @definition.variable

; Local values definitions
locals
  (attribute
    name: (identifier) @name.definition.variable) @definition.variable

; Terraform blocks
(terraform_block) @definition.class

; References to variables/resources
(identifier) @ref
