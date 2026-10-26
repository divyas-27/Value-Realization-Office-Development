import { BrowserRouter, Routes, Route, NavLink, useNavigate } from "react-router-dom";
import "./App.css";
import ProtectedRoute from "./ProtectedRoute";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetails from "./pages/ProjectDetails";
import NewProject from "./pages/NewProject";
import PlannedValue from "./pages/PlannedValue";
import RealizedValue from "./pages/RealizedValue";
import Approvals from "./pages/Approvals";
import Reports from "./pages/Reports";

function Sidebar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const name = localStorage.getItem("name");
  const role = localStorage.getItem("role");

  function logout() {
    localStorage.clear();
    navigate("/");
    window.location.reload();
  }

  return (
    <nav className="sidebar">
      <h2>VRO</h2>
      {token ? (
        <>
          <div className="user-info">
            <strong>{name}</strong>
            <span>{role}</span>
          </div>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/projects">Projects</NavLink>
          <NavLink to="/new-project">New Project</NavLink>
          <NavLink to="/planned-value">Planned Value</NavLink>
          <NavLink to="/realized-value">Realized Value</NavLink>
          <NavLink to="/approvals">Approvals</NavLink>
          <NavLink to="/reports">Reports</NavLink>
          <button className="logout-btn" onClick={logout}>Logout</button>
        </>
      ) : (
        <NavLink to="/">Login</NavLink>
      )}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <Sidebar />
        <main className="content">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/projects" element={<ProtectedRoute><Projects /></ProtectedRoute>} />
            <Route path="/projects/:id" element={<ProtectedRoute><ProjectDetails /></ProtectedRoute>} />
            <Route path="/new-project" element={<ProtectedRoute><NewProject /></ProtectedRoute>} />
            <Route path="/planned-value" element={<ProtectedRoute><PlannedValue /></ProtectedRoute>} />
            <Route path="/realized-value" element={<ProtectedRoute><RealizedValue /></ProtectedRoute>} />
            <Route path="/approvals" element={<ProtectedRoute><Approvals /></ProtectedRoute>} />
            <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;