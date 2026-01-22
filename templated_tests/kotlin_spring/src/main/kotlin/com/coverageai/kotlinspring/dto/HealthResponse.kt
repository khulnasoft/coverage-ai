package com.coverageai.kotlinspring.dto

import java.time.Instant

data class HealthResponse(
    val status: String,
    val timestamp: Instant,
    val version: String
)
