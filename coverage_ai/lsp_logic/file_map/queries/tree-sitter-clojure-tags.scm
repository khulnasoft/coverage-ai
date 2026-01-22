; Clojure language tags for repomap
; Based on Clojure grammar patterns

; Function definitions (defn)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Variable definitions (def)
(list
  (identifier) @name.definition.variable
  .) @definition.variable

; Macro definitions (defmacro)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Protocol definitions
(list
  (identifier) @name.definition.class
  .) @definition.class

; Record definitions
(list
  (identifier) @name.definition.class
  .) @definition.class

; Function calls
(list
  . (identifier) @name.reference.call
  .) @reference.call

; References to symbols
(identifier) @ref
