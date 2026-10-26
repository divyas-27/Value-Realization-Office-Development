import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetails from "./pages/ProjectDetails";
import NewProject from "./pages/NewProject";
import PlannedValue from "./pages/PlannedValue";
import RealizedValue from "./pages/RealizedValue";
import Approvals from "./pages/Approvals";
import Reports from "./pages/Reports";

function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <nav className="sidebar">
          <h2>VRO</h2>
          <NavLink to="/">Login</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/projects">Projects</NavLink>
          <NavLink to="/new-project">New Project</NavLink>
          <NavLink to="/planned-value">Planned Value</NavLink>
          <NavLink to="/realized-value">Realized Value</NavLink>
          <NavLink to="/approvals">Approvals</NavLink>
          <NavLink to="/reports">Reports</NavLink>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/:id" element={<ProjectDetails />} />
            <Route path="/new-project" element={<NewProject />} />
            <Route path="/planned-value" element={<PlannedValue />} />
            <Route path="/realized-value" element={<RealizedValue />} />
            <Route path="/approvals" element={<Approvals />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;