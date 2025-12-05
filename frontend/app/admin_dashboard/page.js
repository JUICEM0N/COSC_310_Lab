"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";

export default function AdminDashboardPage() {
  const router = useRouter();

  // Admin info
  const [admin, setAdmin] = useState(null);

  // Dashboard data
  const [transactions, setTransactions] = useState([]);
  const [penalties, setPenalties] = useState([]);
  const [users, setUsers] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [productsOfWeek, setProductsOfWeek] = useState([]);
  const [summary, setSummary] = useState({});

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");

    if (!token || !savedUser) {
      router.push("/auth/login");
      return;
    }

    try {
      const adminData = JSON.parse(savedUser);

      if (!adminData.isAdmin) {
        router.push("/dashboard"); // Non-admins go to normal dashboard
        return;
      }

      setAdmin(adminData);
      loadAdminData();
    } catch (err) {
      console.error("Error loading admin data:", err);
      router.push("/auth/login");
    }
  }, [router]);

  const loadAdminData = async () => {
    try {
      const [
        transactionsRes,
        penaltiesRes,
        usersRes,
        inventoryRes,
        summaryRes,
        productsWeekRes,
      ] = await Promise.all([
        api.get("/admin_dashboard/download/transactions"),
        api.get("/admin/penalties/all"), // Adjust endpoint if needed
        api.get("/admin_dashboard/users"),
        api.get("/admin_dashboard/inventory"),
        api.get("/admin_dashboard/summary"),
        api.get("/admin/products-of-week"),
      ]);

      setTransactions(transactionsRes.data || []);
      setPenalties(penaltiesRes?.data || []);
      setUsers(usersRes.data || []);
      setInventory(inventoryRes.data || []);
      setSummary(summaryRes.data || {});
      setProductsOfWeek(productsWeekRes.data || []);
    } catch (err) {
      console.error("Error loading admin dashboard:", err);
      setError("Failed to load admin dashboard data");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    router.push("/auth/login");
  };

  const downloadTransactions = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(transactions));
    const dlAnchorElem = document.createElement("a");
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", "transactions.json");
    dlAnchorElem.click();
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-700">Loading admin dashboard...</p>
        </div>
      </main>
    );
  }

  if (!admin) return null;

  return (
    <main className="main-container">
      <div className="content">

        {/* Header */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <h1 style={{ margin: 0, color: "#333" }}>
              Welcome, {admin.username} (Admin)!
            </h1>
            <p style={{ color: "#666", marginTop: "5px" }}>{admin.email}</p>
            <p style={{ color: "#888", fontSize: "0.9rem" }}>
              Admin ID: {admin.user_id || admin.id}
            </p>
          </div>

          <div style={{ display: "flex", gap: "15px" }}>
            <Link
              href="/auth/change-password"
              style={{
                padding: "10px 20px",
                border: "1px solid #ddd",
                borderRadius: "4px",
                textDecoration: "none",
                color: "#333",
                fontWeight: "500",
              }}
            >
              Change Password
            </Link>
            <button
              onClick={handleLogout}
              style={{
                padding: "10px 20px",
                border: "1px solid #ddd",
                borderRadius: "4px",
                background: "#fef2f2",
                color: "#991b1b",
                fontWeight: "500",
              }}
            >
              Logout
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
            gap: "20px",
            marginBottom: "40px",
          }}
        >
          <Link
            href="/"
            style={{
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              padding: "20px",
              borderRadius: "8px",
              textDecoration: "none",
              textAlign: "center",
            }}
          >
            <h3
              style={{
                margin: "0 0 5px 0",
                color: "#1e40af",
                fontSize: "1.25rem",
                fontWeight: "600",
              }}
            >
              Shop
            </h3>
            <p style={{ margin: 0, color: "#1d4ed8" }}>Browse products</p>
          </Link>

          <button
            onClick={downloadTransactions}
            style={{
              background: "#fef3c7",
              border: "1px solid #fde68a",
              padding: "20px",
              borderRadius: "8px",
              textAlign: "center",
              cursor: "pointer",
            }}
          >
            <h3
              style={{
                margin: "0 0 5px 0",
                color: "#92400e",
                fontSize: "1.25rem",
                fontWeight: "600",
              }}
            >
              Download Transactions
            </h3>
            <p style={{ margin: 0, color: "#78350f" }}>Download JSON file</p>
          </button>
        </div>

        {/* Summary */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Summary</h2>
          <p>Total Users: {summary.totalUsers || 0}</p>
          <p>Total Sales: ${summary.totalSales?.toFixed(2) || 0}</p>
        </div>

        {/* Inventory */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Inventory</h2>
          <ul>
            {inventory.map(item => (
              <li key={item.product_id}>{item.name} - Stock: {item.stock}</li>
            ))}
          </ul>
        </div>

        {/* Products of the Week */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Products of the Week</h2>
          <ul>
            {productsOfWeek.map(p => (
              <li key={p.product_id}>{p.name}</li>
            ))}
          </ul>
        </div>

        {/* Users / Manage Users */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Manage Users</h2>
          {users.map(u => (
            <div key={u.user_id} style={{ display: "flex", justifyContent: "space-between", padding: "10px", borderBottom: "1px solid #eee" }}>
              <div>{u.username} ({u.email})</div>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={() => api.post("/admin/promote", { user_id: u.user_id })}>Promote</button>
                <button onClick={async () => {
                  const amount = prompt("Penalty amount:");
                  const reason = prompt("Reason:");
                  if (amount && reason) {
                    await api.post("/admin/penalty", { user_id: u.user_id, amount: parseFloat(amount), reason });
                    alert(`Penalty applied to ${u.username}`);
                  }
                }}>Apply Penalty</button>
              </div>
            </div>
          ))}
        </div>

        {/* Transactions */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginBottom: "30px",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Transactions</h2>
          {transactions.length === 0 ? <p>No transactions</p> :
            transactions.map(t => (
              <div key={t.transaction_id} style={{ borderBottom: "1px solid #eee", padding: "10px 0" }}>
                <p>Order #{t.transaction_id?.slice(0, 8)} - ${t.total_amount?.toFixed(2)}</p>
              </div>
            ))
          }
        </div>

        {/* Penalties */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "10px" }}>Penalties</h2>
          {penalties.length === 0 ? <p>No penalties</p> :
            penalties.map(p => (
              <div key={p.penalty_id} style={{ borderBottom: "1px solid #fecaca", padding: "10px 0" }}>
                <p>{p.reason} - ${p.amount}</p>
              </div>
            ))
          }
        </div>

      </div>
    </main>
  );
}
