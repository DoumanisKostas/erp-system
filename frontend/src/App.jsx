import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Customers from "./pages/Customers";
import Sales from "./pages/Sales";
import Reports from "./pages/Reports";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <aside className="sidebar">
          <h2>ERP System</h2>

          <nav>
            <Link to="/">Dashboard </Link>
            <Link to="/products">Products </Link>
            <Link to="/customers">Customers </Link>
            <Link to="/sales">Sales </Link>
            <Link to="/reports">Reports</Link>
          </nav>
        </aside>

        <main className="main">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/sales" element={<Sales />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;