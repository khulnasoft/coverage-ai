; Chatito language tags for repomap
; Based on Chatito grammar patterns

; Intent definitions
(intent_definition
  name: (identifier) @name.definition.class) @definition.class

; Entity definitions
(entity_definition
  name: (identifier) @name.definition.class) @definition.class

; Slot definitions
(slot_definition
  name: (identifier) @name.definition.variable) @definition.variable

; References to intents/entities
(identifier) @ref
