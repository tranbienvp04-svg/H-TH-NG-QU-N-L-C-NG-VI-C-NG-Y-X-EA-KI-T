import { Link, useLocation } from 'react-router-dom';

export function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation();
  return (
    <div>
      <header style={{ background: '#0f172a', color: 'white', padding: '16px 24px' }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <strong>Đảng ủy xã Ea Kiết</strong>
          <nav style={{ display: 'flex', gap: 16 }}>
            <Link to="/" style={{ color: location.pathname === '/' ? '#93c5fd' : 'white' }}>Dashboard</Link>
            <Link to="/tasks" style={{ color: location.pathname === '/tasks' ? '#93c5fd' : 'white' }}>Nhiệm vụ</Link>
            <Link to="/login" style={{ color: location.pathname === '/login' ? '#93c5fd' : 'white' }}>Đăng nhập</Link>
          </nav>
        </div>
      </header>
      <main className="container">{children}</main>
    </div>
  );
}
