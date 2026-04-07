import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Button, Navbar, Nav, Spinner, Alert, Form, InputGroup } from 'react-bootstrap';

function Todolist() {
    const navigate = useNavigate();
    const [tasks, setTasks] = useState([]);
    const [status, setStatus] = useState({loading: true, error: null});
    
    const [newTaskTitle, setNewTaskTitle] = useState("");

    const fetchTasks = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/v1/task', {
                method: 'GET',
                credentials: 'include' 
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (!res.ok) {
                throw new Error("Failed to fetch tasks");
            }
            const data = await res.json();

            if (Array.isArray(data)) {
                setTasks(data);
            } else if (data && Array.isArray(data.tasks)) {
                setTasks(data.tasks);
            } else {
                setTasks([]);
            }

            setStatus({ loading: false, error: null })
        } catch (err) {
            setStatus({ loading: false, error: err.message })
        } finally {
            setStatus(prev => ({ ...prev, loading: false }));
        }
    };

    useEffect(() => {
        fetchTasks();
    }, []);

    const toggleTask = async (task) => {
        const isCompleted = task.state === 'completed';
        const newState = isCompleted ? 'open' : 'completed';

        setTasks(prevTasks =>
            prevTasks.map(t => (t.id === task.id ? { ...t, state: newState } : t))
        );

        try {
            const res = await fetch(`http://localhost:8000/api/v1/task/${task.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state: newState }),
                credentials: 'include'
            });

            if (!res.ok) {
                fetchTasks(); 
            }
        } catch (err) {
            console.error("Update failed:", err);
            fetchTasks();
        }
    };

    const handleAddTask = async (e) => {
        e.preventDefault(); 
        
        if (!newTaskTitle.trim()) return; 

        try {
            const res = await fetch('http://localhost:8000/api/v1/task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: newTaskTitle }),
                credentials: 'include'
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (res.ok) {
                const newTask = await res.json();
                setTasks(prev => [...prev, newTask]);
                setNewTaskTitle("");
            } else {
                console.error("Failed to add task");
            }
        } catch (err) {
            console.error("Network error when adding task:", err);
        }
    };

    if (status.loading) {
        return (
            <Container className="text-center mt-5">
                <Spinner animation="border" variant="primary" />
                <p className="mt-2">Loading your tasks...</p>
            </Container>
        );
    }

    if (status.error) {
        return (
            <Container className="mt-5">
                <Alert variant="danger">{status.error}</Alert>
                <Button onClick={fetchTasks}>Try Again</Button>
            </Container>
        );
    }

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f0f4ff' }}>
            <Navbar bg="white" className="px-4 shadow-sm mb-5">
                <Navbar.Brand href="/" className="fw-bold text-primary">
                    DoIt
                </Navbar.Brand>
                <Nav className="me-auto"></Nav>
                <Button variant="outline-danger" onClick={() => navigate('/login')}>
                    Logout
                </Button>
            </Navbar>

            <Container className="d-flex justify-content-center">
                <div
                    className="shadow-lg rounded-4 bg-white p-4"
                    style={{ width: '400px', minHeight: '300px' }}
                >
                    <h4 className="fw-bold mb-4">My To Do List</h4>

                    {tasks.length === 0 ? (
                        <p className="text-muted text-center mt-4 mb-4">No tasks found.</p>
                    ) : (
                        tasks.map((task) => {
                            const isCompleted = task.state === 'completed';
                            return (
                                <div key={task.id} className="d-flex align-items-center gap-3 mb-3">
                                    <input
                                        type="checkbox"
                                        checked={isCompleted}
                                        onChange={() => toggleTask(task)}
                                        style={{ width: '18px', height: '18px', cursor: 'pointer' }}
                                    />
                                    <span
                                        style={{
                                            textDecoration: isCompleted ? 'line-through' : 'none',
                                            color: isCompleted ? '#aaa' : '#000',
                                            fontSize: '1.1rem',
                                            transition: 'all 0.2s ease-in-out',
                                            cursor: 'pointer'
                                        }}
                                        onClick={() => toggleTask(task)}
                                    >
                                        {task.title}
                                    </span>
                                </div>
                            );
                        })
                    )}

                    <Form onSubmit={handleAddTask} className="mt-4">
                        <InputGroup>
                            <Form.Control
                                placeholder="What needs to be done?"
                                value={newTaskTitle}
                                onChange={(e) => setNewTaskTitle(e.target.value)}
                            />
                            <Button variant="primary" type="submit" className="fw-bold">
                                + Add
                            </Button>
                        </InputGroup>
                    </Form>

                </div>
            </Container>
        </div>
    );
}

export default Todolist;