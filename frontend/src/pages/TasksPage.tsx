import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Task } from '../types/models';

export function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    api.get<Task[]>('/api/v1/tasks').then((res) => setTasks(res.data));
  }, []);

  return (
    <section className="card">
      <h2>Danh sách nhiệm vụ</h2>
      {tasks.map((task) => (
        <div key={task.id} style={{ borderBottom: '1px solid #e2e8f0', padding: '12px 0' }}>
          <strong>{task.title}</strong>
          <p>{task.description}</p>
          <small>Trạng thái: {task.status}</small>
        </div>
      ))}
    </section>
  );
}
