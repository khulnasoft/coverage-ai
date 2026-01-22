package com.coverageai.kotlinspring

import com.coverageai.kotlinspring.controller.CalculatorController
import com.coverageai.kotlinspring.service.CalculatorService
import com.fasterxml.jackson.databind.ObjectMapper
import org.junit.jupiter.api.Test
import org.mockito.kotlin.any
import org.mockito.kotlin.whenever
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.mock.mockito.MockBean
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.post
import org.springframework.test.web.servlet.get

@WebMvcTest(CalculatorController::class)
class CalculatorControllerTest(@Autowired val mockMvc: MockMvc) {

    @MockBean
    private lateinit var calculatorService: CalculatorService

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @Test
    fun `health check returns OK status`() {
        mockMvc.get("/api/health")
            .andExpect {
                status { isOk() }
                jsonPath("$.status") { value("OK") }
                jsonPath("$.version") { value("1.0.0") }
            }
    }

    @Test
    fun `calculate addition returns correct result`() {
        whenever(calculatorService.calculate("add", 5.0, 3.0)).thenReturn(8.0)

        val request = mapOf(
            "operation" to "add",
            "a" to 5.0,
            "b" to 3.0
        )

        mockMvc.post("/api/calculate") {
            contentType = MediaType.APPLICATION_JSON
            content = objectMapper.writeValueAsString(request)
        }.andExpect {
            status { isOk() }
            jsonPath("$.operation") { value("add") }
            jsonPath("$.a") { value(5.0) }
            jsonPath("$.b") { value(3.0) }
            jsonPath("$.result") { value(8.0) }
        }
    }

    @Test
    fun `calculate division by zero returns bad request`() {
        whenever(calculatorService.calculate(any(), any(), any()))
            .thenThrow(IllegalArgumentException("Division by zero"))

        val request = mapOf(
            "operation" to "divide",
            "a" to 10.0,
            "b" to 0.0
        )

        mockMvc.post("/api/calculate") {
            contentType = MediaType.APPLICATION_JSON
            content = objectMapper.writeValueAsString(request)
        }.andExpect {
            status { isBadRequest() }
            jsonPath("$.error") { value("Division by zero") }
        }
    }

    @Test
    fun `calculate with invalid operation returns bad request`() {
        val request = mapOf(
            "operation" to "invalid",
            "a" to 5.0,
            "b" to 3.0
        )

        mockMvc.post("/api/calculate") {
            contentType = MediaType.APPLICATION_JSON
            content = objectMapper.writeValueAsString(request)
        }.andExpect {
            status { isBadRequest() }
        }
    }

    @Test
    fun `calculate with missing parameters returns bad request`() {
        val request = mapOf(
            "operation" to "add",
            "a" to 5.0
        )

        mockMvc.post("/api/calculate") {
            contentType = MediaType.APPLICATION_JSON
            content = objectMapper.writeValueAsString(request)
        }.andExpect {
            status { isBadRequest() }
        }
    }
}
