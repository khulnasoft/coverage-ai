const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Calculator operations
const add = (a, b) => a + b;
const subtract = (a, b) => a - b;
const multiply = (a, b) => a * b;
const divide = (a, b) => {
    if (b === 0) {
        throw new Error('Division by zero');
    }
    return a / b;
};

// Routes
app.get('/health', (req, res) => {
    res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.post('/calculate', (req, res) => {
    const { operation, a, b } = req.body;
    
    if (!operation || a === undefined || b === undefined) {
        return res.status(400).json({ 
            error: 'Missing required parameters: operation, a, b' 
        });
    }
    
    if (typeof a !== 'number' || typeof b !== 'number') {
        return res.status(400).json({ 
            error: 'Parameters a and b must be numbers' 
        });
    }
    
    try {
        let result;
        switch (operation) {
            case 'add':
                result = add(a, b);
                break;
            case 'subtract':
                result = subtract(a, b);
                break;
            case 'multiply':
                result = multiply(a, b);
                break;
            case 'divide':
                result = divide(a, b);
                break;
            default:
                return res.status(400).json({ 
                    error: 'Invalid operation. Use: add, subtract, multiply, divide' 
                });
        }
        
        res.json({ 
            operation, 
            a, 
            b, 
            result,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({ error: 'Route not found' });
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}

module.exports = app;
