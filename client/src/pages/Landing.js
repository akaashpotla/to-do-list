import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Container, Navbar, Nav } from 'react-bootstrap';

const DEMO_TASKS = [
    { title: 'Morning Workout', done: true },
    { title: 'Team Meeting', done: false },
    { title: 'Buy Groceries', done: true },
    { title: 'Read 2 pages of a Book', done: false },
];

function Landing() {
    const navigate = useNavigate();
    const [tasks, setTasks] = useState(DEMO_TASKS);

    const toggleTask = (index) => {
        setTasks(prev => prev.map((task, i) =>
            i === index ? { ...task, done: !task.done } : task
        ));
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f0f4ff' }}>
            <Navbar bg="white" className="px-4 shadow-sm">
                <Navbar.Brand href="/" className="fw-bold text-primary">DoIt</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                </Nav>
                <div className="d-flex gap-2">
                    <Button variant="outline-primary" onClick={() => navigate('/login')}>Login</Button>
                    <Button variant="primary" onClick={() => navigate('/signup')}>Signup</Button>
                </div>
            </Navbar>

            <Container className="d-flex align-items-center justify-content-between" style={{ minHeight: '85vh' }}>
                <div style={{ maxWidth: '500px' }}>
                    <h1 className="fw-bold" style={{ fontSize: '3rem', color: '#000080' }}>Organize Your Life,{' '}
                        <span style={{ color: '#e84545' }}>Achieve Your Goals</span>
                    </h1>
                    <p className="mt-3 text-muted" style={{ fontSize: '1.2rem' }}>
                        Stop forgetting. Start doing. DoIt helps you manage your tasks effortlessly and stay on top of your day.
                    </p>
                    <Button
                        variant="primary"
                        size="lg"
                        className="mt-4 px-5 py-3 rounded-pill fw-bold"
                        onClick={() => navigate('/signup')}
                    >Get Started</Button>
                </div>

                <div className="shadow-lg rounded-4 bg-white p-4" style={{ width: '340px', minHeight: '300px' }}>
                    <h5 className="fw-bold mb-3">Today's Tasks</h5>
                    {tasks.map((task, i) => (
                        <div key={i} className="d-flex align-items-center gap-2 mb-3">
                            <input
                                type="checkbox"
                                checked={task.done}
                                onChange={() => toggleTask(i)}
                            />
                            <span style={{ 
                                textDecoration: task.done ? 'line-through' : 'none', 
                                color: task.done ? '#aaa' : '#000' 
                            }}>
                                {task.title}
                            </span>
                        </div>
                    ))}
                    <Button variant="danger" className="w-100 mt-2">+ Add Task</Button>
                </div>
            </Container>
        </div>
    );
}

export default Landing;