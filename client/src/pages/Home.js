import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Button, Navbar, Nav, Spinner, Alert, Form, InputGroup } from 'react-bootstrap';

function Home() {
    const navigate = useNavigate();
    const [tasks, setTasks] = useState([]);
    const [status, setStatus] = useState({ loading: true, error: null });
    const [editId, setEditId] = useState(null);
    const [editTitle, setEditTitle] = useState('');
    const [newTaskTitle, setNewTaskTitle] = useState('');

    const fetchTasks = useCallback(async () => {
        try {
            const res = await fetch('http://localhost:8000/api/v1/task', {
                method: 'GET',
                credentials: 'include',
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (!res.ok) {
                throw new Error('Failed to fetch tasks');
            }

            const data = await res.json();
            if (Array.isArray(data)) {
                setTasks(data);
            } else if (data && Array.isArray(data.tasks)) {
                setTasks(data.tasks);
            } else {
                setTasks([]);
            }

            setStatus({ loading: false, error: null });
        } catch (err) {
            setStatus({ loading: false, error: err.message });
        }
    } , [navigate]);

    useEffect(() => {
        fetchTasks();
    }, [fetchTasks]);

    const toggleTask = async (task) => {
        const isCompleted = task.state === 'completed';
        const newState = isCompleted ? 'open' : 'completed';

        setTasks((prevTasks) =>
            prevTasks.map((t) => (t.id === task.id ? { ...t, state: newState } : t))
        );

        try {
            const res = await fetch(`http://localhost:8000/api/v1/task/${task.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state: newState }),
                credentials: 'include',
            });

            if (!res.ok) {
                fetchTasks();
            }
        } catch (err) {
            console.error('Update failed:', err);
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
                body: JSON.stringify({ title: newTaskTitle.trim() }),
                credentials: 'include',
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (res.ok) {
                const newTask = await res.json();
                setTasks((prev) => [...prev, newTask]);
                setNewTaskTitle('');
            } else {
                console.error('Failed to add task');
            }
        } catch (err) {
            console.error('Network error when adding task:', err);
        }
    };

    const handleDelete = async (taskId) => {
        try {
            const res = await fetch(`http://localhost:8000/api/v1/task/${taskId}`, {
                method: 'DELETE',
                credentials: 'include',
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (res.ok) {
                setTasks((prev) => prev.filter((task) => task.id !== taskId));
            } else {
                console.error('Failed to delete task');
            }
        } catch (err) {
            console.error('Error when deleting task:', err);
        }
    };

    const handleEditSave = async (taskId) => {
        if (!editTitle.trim()) return;

        try {
            const res = await fetch(`http://localhost:8000/api/v1/task/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: editTitle.trim() }),
                credentials: 'include',
            });

            if (res.status === 401) {
                navigate('/login');
                return;
            }

            if (res.ok) {
                const updatedTask = await res.json();
                setTasks((prev) => prev.map((task) => (task.id === taskId ? updatedTask : task)));
                setEditId(null);
                setEditTitle('');
            } else {
                console.error('Failed to update task');
            }
        } catch (err) {
            console.error('Error when editing task:', err);
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

    const handleLogout = async () => {
        await fetch('http://localhost:8000/api/v1/user/logout', {
            method: "POST",
            credentials: 'include'
        });
        navigate('/login');
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f0f4ff' }}>
            <Navbar bg="white" className="px-4 shadow-sm mb-5">
                <Navbar.Brand href="/" className="fw-bold text-primary">
                    DoIt
                </Navbar.Brand>
                <Nav className="me-auto"></Nav>
                <Button variant="outline-danger" onClick={handleLogout}>
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

                                    {editId === task.id ? (
                                        <InputGroup>
                                            <Form.Control
                                            value={editTitle}
                                            onChange={(e) => setEditTitle(e.target.value)}
                                            onKeyDown={(e) => {
                                                if (e.key === 'Enter') handleEditSave(task.id);
                                                if (e.key === 'Escape') setEditId(null);
                                            }}
                                            onBlur={() => handleEditSave(task.id)}
                                            autoFocus
                                        />
                                            <Button variant="success" size="sm" onClick={() => handleEditSave(task.id)}>
                                                Save
                                            </Button>
                                            <Button 
                                                variant="secondary"
                                                size="sm"
                                                onMouseDown={(e) => e.preventDefault()}
                                                onClick={() => setEditId(null)}
                                            >
                                                Cancel
                                            </Button>
                                        </InputGroup>
                                    ) : (
                                        <>
                                            <span
                                                style={{
                                                    textDecoration: isCompleted ? 'line-through' : 'none',
                                                    color: isCompleted ? '#aaa' : '#000',
                                                    fontSize: '1rem',
                                                    flexGrow: 1,
                                                    cursor: 'text',
                                                }}
                                                onClick={() => {
                                                    setEditId(task.id);
                                                    setEditTitle(task.title);
                                                }}
                                            >
                                                {task.title}
                                            </span>
                                            <Button
                                                variant="outline-danger"
                                                size="sm"
                                                onClick={() => handleDelete(task.id)}
                                            >
                                                🗑️
                                            </Button>
                                        </>
                                    )}
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

export default Home;