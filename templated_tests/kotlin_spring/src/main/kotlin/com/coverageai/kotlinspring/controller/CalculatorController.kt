package com.coverageai.kotlinspring.controller

import com.coverageai.kotlinspring.service.CalculatorService
import com.coverageai.kotlinspring.dto.CalculateRequest
import com.coverageai.kotlinspring.dto.CalculateResponse
import com.coverageai.kotlinspring.dto.HealthResponse
import jakarta.validation.Valid
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.time.Instant

@RestController
@RequestMapping("/api")
class CalculatorController(private val calculatorService: CalculatorService) {

    @GetMapping("/health")
    fun health(): ResponseEntity<HealthResponse> {
        return ResponseEntity.ok(
            HealthResponse(
                status = "OK",
                timestamp = Instant.now(),
                version = "1.0.0"
            )
        )
    }

    @PostMapping("/calculate")
    fun calculate(@Valid @RequestBody request: CalculateRequest): ResponseEntity<CalculateResponse> {
        return try {
            val result = calculatorService.calculate(request.operation, request.a, request.b)
            ResponseEntity.ok(
                CalculateResponse(
                    operation = request.operation,
                    a = request.a,
                    b = request.b,
                    result = result,
                    timestamp = Instant.now()
                )
            )
        } catch (e: IllegalArgumentException) {
            ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(CalculateResponse(error = e.message))
        }
    }
}
