<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\CalculatorController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::get('/health', [CalculatorController::class, 'health']);

Route::post('/calculate', [CalculatorController::class, 'calculate']);
