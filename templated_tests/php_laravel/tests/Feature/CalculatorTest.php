<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class CalculatorTest extends TestCase
{
    /**
     * Test health check endpoint.
     */
    public function test_health_check(): void
    {
        $response = $this->getJson('/api/health');

        $response->assertStatus(200)
                 ->assertJsonStructure([
                     'status',
                     'timestamp',
                     'version'
                 ])
                 ->assertJson(['status' => 'OK']);
    }

    /**
     * Test addition operation.
     */
    public function test_addition(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'add',
            'a' => 5,
            'b' => 3
        ]);

        $response->assertStatus(200)
                 ->assertJson([
                     'operation' => 'add',
                     'a' => 5,
                     'b' => 3,
                     'result' => 8
                 ]);
    }

    /**
     * Test subtraction operation.
     */
    public function test_subtraction(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'subtract',
            'a' => 10,
            'b' => 4
        ]);

        $response->assertStatus(200)
                 ->assertJson([
                     'operation' => 'subtract',
                     'a' => 10,
                     'b' => 4,
                     'result' => 6
                 ]);
    }

    /**
     * Test multiplication operation.
     */
    public function test_multiplication(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'multiply',
            'a' => 6,
            'b' => 7
        ]);

        $response->assertStatus(200)
                 ->assertJson([
                     'operation' => 'multiply',
                     'a' => 6,
                     'b' => 7,
                     'result' => 42
                 ]);
    }

    /**
     * Test division operation.
     */
    public function test_division(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'divide',
            'a' => 20,
            'b' => 5
        ]);

        $response->assertStatus(200)
                 ->assertJson([
                     'operation' => 'divide',
                     'a' => 20,
                     'b' => 5,
                     'result' => 4
                 ]);
    }

    /**
     * Test division by zero.
     */
    public function test_division_by_zero(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'divide',
            'a' => 10,
            'b' => 0
        ]);

        $response->assertStatus(400)
                 ->assertJson([
                     'error' => 'Division by zero'
                 ]);
    }

    /**
     * Test invalid operation.
     */
    public function test_invalid_operation(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'invalid',
            'a' => 5,
            'b' => 3
        ]);

        $response->assertStatus(400)
                 ->assertJsonValidationErrors(['operation']);
    }

    /**
     * Test missing parameters.
     */
    public function test_missing_parameters(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'add',
            'a' => 5
        ]);

        $response->assertStatus(400)
                 ->assertJsonValidationErrors(['b']);
    }

    /**
     * Test non-numeric parameters.
     */
    public function test_non_numeric_parameters(): void
    {
        $response = $this->postJson('/api/calculate', [
            'operation' => 'add',
            'a' => 'five',
            'b' => 3
        ]);

        $response->assertStatus(400)
                 ->assertJsonValidationErrors(['a']);
    }
}
