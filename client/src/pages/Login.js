import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Form, Button, Alert } from 'react-bootstrap';

function Login() {
    const navigate = useNavigate();
    const [creds, setCreds] = useState({ email: '', password: '' });
    const [status, setStatus] = useState({ loading: false, error: null });

    const updateField = (e) => {
        setCreds(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const onLoginSubmit = async (e) => {
        e.preventDefault();
        setStatus({ loading: true, error: null });

        try {
            const formData = new URLSearchParams();
            formData.append('username', creds.email);
            formData.append('password', creds.password);

            const res = await fetch('http://localhost:8000/api/v1/user/auth', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData,
                credentials: 'include'
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || 'Unauthorized');
            }

            navigate('/home');
        } catch (err) {
            setStatus({ loading: false, error: err.message });
        }
    };

    return (
        <Container className="mt-5" style={{ maxWidth: '400px' }}>
            <div className="mb-4">
                <h2 className="fw-bold">Login</h2>
                <p className="text-muted small">Login to continue.</p>
            </div>

            {status.error && <Alert variant="danger" className="small">{status.error}</Alert>}

            <Form onSubmit={onLoginSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label className="small text-muted">Email Address</Form.Label>
                    <Form.Control 
                        name="email" 
                        type="email" 
                        value={creds.email} 
                        onChange={updateField} 
                        required 
                    />
                </Form.Group>
                <Form.Group className="mb-4">
                    <Form.Label className="small text-muted">Password</Form.Label>
                    <Form.Control 
                        name="password" 
                        type="password" 
                        value={creds.password} 
                        onChange={updateField} 
                        required 
                    />
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100" disabled={status.loading}>
                    {status.loading ? 'Signing in...' : 'Sign In'}
                </Button>
            </Form>
        </Container>
    );
};

export default Login;