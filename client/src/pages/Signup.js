import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Container, Form, Button, Alert } from 'react-bootstrap';

const Signup = () => {
    const navigate = useNavigate();
    
    const [user, setUser] = useState({ name: '', email: '', password: '' });
    const [status, setStatus] = useState({ loading: false, error: null });

    const updateField = (e) => {
        setUser(prev => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const onSignupSubmit = async (e) => {
        e.preventDefault();
        setStatus({ loading: true, error: null });

        try {
            const res = await fetch('http://localhost:8000/api/v1/user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            });

            if (!res.ok) {
                const errData = await res.json();
                const detail = errData.detail;
                if (Array.isArray(detail)) {
                    throw new Error(detail.map(e => e.msg).join(', '));
                }
                throw new Error(errData.detail || 'Sign up failed');
            }

            navigate('/login');
        } catch (err) {
            setStatus({ loading: false, error: err.message });
        }
    };

    return (
        <Container className="mt-5" style={{ maxWidth: '400px' }}>
            <div className="mb-4">
                <h2 className="fw-bold">Create Account</h2>
                <p className="text-muted small">Fill out the details below to join us!</p>
            </div>

            {status.error && <Alert variant="danger" className="small">{status.error}</Alert>}

            <Form onSubmit={onSignupSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label className="small text-muted">Full Name</Form.Label>
                    <Form.Control 
                        name="name" 
                        type="text" 
                        value={user.name} 
                        onChange={updateField} 
                        required 
                    />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label className="small text-muted">Email Address</Form.Label>
                    <Form.Control 
                        name="email" 
                        type="email" 
                        value={user.email} 
                        onChange={updateField} 
                        required 
                    />
                </Form.Group>

                <Form.Group className="mb-4">
                    <Form.Label className="small text-muted">Password</Form.Label>
                    <Form.Control 
                        name="password" 
                        type="password" 
                        value={user.password} 
                        onChange={updateField} 
                        required 
                    />
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100" disabled={status.loading}>
                    {status.loading ? 'Creating account...' : 'Sign Up'}
                </Button>
            </Form>

            <div className="mt-3 text-center small">
                <span className="text-muted">Already a member?</span>{' '}
                <Link to="/login" className="text-decoration-none">Log in here</Link>
            </div>
        </Container>
    );
};

export default Signup;