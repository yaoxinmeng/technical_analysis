import jwt from 'jsonwebtoken';
import { randomBytes } from 'crypto';
import { ROOT_USERNAME, ROOT_PASSWORD } from '$env/static/private';

// Generate a public/private key pair for JWT signing
const privateKey = randomBytes(32).toString('hex');

export function generateToken(username: string, password: string): string {
    const payload = {
        username: username,
        password: password,
        timestamp: Date.now()
    };

    return jwt.sign(payload, privateKey);
}


export function verifyToken(token: string): boolean {
    try {
        const decoded = jwt.verify(token, privateKey) as jwt.JwtPayload;
        if (!decoded) {
            console.error('Invalid token structure');
            return false; 
        }
        return decoded.username === ROOT_USERNAME && decoded.password === ROOT_PASSWORD && decoded.timestamp > Date.now() - 3_600_000; // Token is valid for 1 hour
    } catch (error) {
        console.error('Token verification failed:', error);
        return false;
    }
}