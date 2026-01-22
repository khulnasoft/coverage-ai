package com.coverageai.kotlinspring.dto

import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.NotNull
import jakarta.validation.constraints.Pattern

data class CalculateRequest(
    @field:NotBlank(message = "Operation is required")
    @field:Pattern(regexp = "^(add|subtract|multiply|divide)$", message = "Invalid operation")
    val operation: String,
    
    @field:NotNull(message = "First number is required")
    val a: Double,
    
    @field:NotNull(message = "Second number is required")
    val b: Double
)
