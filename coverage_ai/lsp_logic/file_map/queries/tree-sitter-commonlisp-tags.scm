; Common Lisp language tags for repomap
; Based on Common Lisp grammar patterns

; Function definitions (defun)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Variable definitions (defvar, defparameter)
(list
  (identifier) @name.definition.variable
  .) @definition.variable

; Macro definitions (defmacro)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Class definitions (defclass)
(list
  (identifier) @name.definition.class
  .) @definition.class

; Generic function definitions (defgeneric)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Method definitions (defmethod)
(list
  (identifier) @name.definition.function
  .) @definition.function

; Function calls
(list
  . (identifier) @name.reference.call
  .) @reference.call

; References to symbols
(identifier) @ref
