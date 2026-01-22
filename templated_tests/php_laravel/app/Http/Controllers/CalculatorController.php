<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Validator;

class CalculatorController extends Controller
{
    /**
     * Perform calculator operations.
     */
    public function calculate(Request $request): JsonResponse
    {
        $validator = Validator::make($request->all(), [
            'operation' => 'required|in:add,subtract,multiply,divide',
            'a' => 'required|numeric',
            'b' => 'required|numeric',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'error' => 'Validation failed',
                'details' => $validator->errors()
            ], 400);
        }

        $operation = $request->input('operation');
        $a = $request->input('a');
        $b = $request->input('b');

        try {
            $result = match ($operation) {
                'add' => $this->add($a, $b),
                'subtract' => $this->subtract($a, $b),
                'multiply' => $this->multiply($a, $b),
                'divide' => $this->divide($a, $b),
            };

            return response()->json([
                'operation' => $operation,
                'a' => $a,
                'b' => $b,
                'result' => $result,
                'timestamp' => now()->toISOString()
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'error' => $e->getMessage()
            ], 400);
        }
    }

    /**
     * Health check endpoint.
     */
    public function health(): JsonResponse
    {
        return response()->json([
            'status' => 'OK',
            'timestamp' => now()->toISOString(),
            'version' => '1.0.0'
        ]);
    }

    private function add(float $a, float $b): float
    {
        return $a + $b;
    }

    private function subtract(float $a, float $b): float
    {
        return $a - $b;
    }

    private function multiply(float $a, float $b): float
    {
        return $a * $b;
    }

    private function divide(float $a, float $b): float
    {
        if ($b == 0) {
            throw new \Exception('Division by zero');
        }
        return $a / $b;
    }
}
