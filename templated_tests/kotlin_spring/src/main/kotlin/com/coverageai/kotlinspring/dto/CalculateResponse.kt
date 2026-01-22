package com.coverageai.kotlinspring.dto

import com.fasterxml.jackson.annotation.JsonInclude
import java.time.Instant

@JsonInclude(JsonInclude.Include.NON_NULL)
data class CalculateResponse(
    val operation: String? = null,
    val a: Double? = null,
    val b: Double? = null,
    val result: Double? = null,
    val timestamp: Instant? = null,
    val error: String? = null
)
