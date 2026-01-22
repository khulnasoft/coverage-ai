const request = require('supertest');
const app = require('../src/app');

describe('Calculator API', () => {
    describe('GET /health', () => {
        it('should return health status', async () => {
            const response = await request(app)
                .get('/health')
                .expect(200);
            
            expect(response.body.status).toBe('OK');
            expect(response.body.timestamp).toBeDefined();
        });
    });
    
    describe('POST /calculate', () => {
        it('should perform addition', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'add', a: 5, b: 3 })
                .expect(200);
            
            expect(response.body.result).toBe(8);
            expect(response.body.operation).toBe('add');
        });
        
        it('should perform subtraction', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'subtract', a: 10, b: 4 })
                .expect(200);
            
            expect(response.body.result).toBe(6);
        });
        
        it('should perform multiplication', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'multiply', a: 6, b: 7 })
                .expect(200);
            
            expect(response.body.result).toBe(42);
        });
        
        it('should perform division', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'divide', a: 20, b: 5 })
                .expect(200);
            
            expect(response.body.result).toBe(4);
        });
        
        it('should handle division by zero', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'divide', a: 10, b: 0 })
                .expect(400);
            
            expect(response.body.error).toBe('Division by zero');
        });
        
        it('should handle invalid operation', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'invalid', a: 5, b: 3 })
                .expect(400);
            
            expect(response.body.error).toContain('Invalid operation');
        });
        
        it('should handle missing parameters', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'add', a: 5 })
                .expect(400);
            
            expect(response.body.error).toContain('Missing required parameters');
        });
        
        it('should handle non-numeric parameters', async () => {
            const response = await request(app)
                .post('/calculate')
                .send({ operation: 'add', a: 'five', b: 3 })
                .expect(400);
            
            expect(response.body.error).toContain('must be numbers');
        });
    });
    
    describe('404 handler', () => {
        it('should return 404 for unknown routes', async () => {
            const response = await request(app)
                .get('/unknown')
                .expect(404);
            
            expect(response.body.error).toBe('Route not found');
        });
    });
});
