const request = require('supertest');
const app = require('../server');

describe('Docker Demo Server', () => {
    describe('GET /api/health', () => {
        it('should return health status', async () => {
            const response = await request(app)
                .get('/api/health')
                .expect(200);
            
            expect(response.body).toHaveProperty('status', 'OK');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body).toHaveProperty('container');
        });
    });

    describe('GET /', () => {
        it('should serve the main page', async () => {
            await request(app)
                .get('/')
                .expect(200)
                .expect('Content-Type', /text/);
        });
    });

    describe('GET /nonexistent', () => {
        it('should serve main page for non-existent routes', async () => {
            await request(app)
                .get('/nonexistent')
                .expect(200)
                .expect('Content-Type', /text/);
        });
    });
});
