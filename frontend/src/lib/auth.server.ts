import jwt from 'jsonwebtoken';
import { randomBytes } from 'crypto';
import { env } from '$env/dynamic/private';

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
        return decoded.username === env.ROOT_USERNAME && decoded.password === env.ROOT_PASSWORD && decoded.timestamp > Date.now() - 3_600_000; // Token is valid for 1 hour
    } catch (error) {
        console.error('Token verification failed');
        return false;
    }
}