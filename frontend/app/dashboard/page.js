"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";
import Navigation from "../components/Navigation";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [penalties, setPenalties] = useState([]);
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
    const userData = JSON.parse(savedUser);

    if (userData.isAdmin) {
      router.push("/admin-dashboard"); // redirect admins
      return;
    }

    setUser(userData);
    loadDashboardData(userData.user_id || userData.id);
  } catch (err) {
    console.error("Error parsing user data:", err);
    router.push("/auth/login");
  }
}, [router]);


  const loadDashboardData = async (userId) => {
    try {
      const response = await api.get(`/user_dashboard/${userId}`);
      if (response.data && response.data.data) {
        setTransactions(response.data.data.transactions || []);
        setPenalties(response.data.data.penalties || []);
      }
    } catch (err) {
      setError("Failed to load dashboard data");
      console.error("Error loading dashboard:", err);
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

  if (loading) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-700">Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <>
    <Navigation showOnAuth={true} />

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
              Welcome, {user.username}!
            </h1>
            <p style={{ color: "#666", marginTop: "5px" }}>{user.email}</p>
            <p style={{ color: "#888", fontSize: "0.9rem" }}>
              User ID: {user.user_id || user.id}
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
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
            >
              Change Password
            </Link>
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
            href="/checkout"
            style={{
              background: "#f0fdf4",
              border: "1px solid #bbf7d0",
              padding: "20px",
              borderRadius: "8px",
              textDecoration: "none",
              textAlign: "center",
              transition: "transform 0.2s",
            }}
          >
            <h3
              style={{
                margin: "0 0 5px 0",
                color: "#166534",
                fontSize: "1.25rem",
                fontWeight: "600"
              }}
            >
              View Cart
            </h3>
            <p style={{ margin: 0, color: "#15803d" }}>Check your cart</p>
          </Link>

          <Link
            href="/dashboard/subscriptions"
            style={{
              background: "#fff7ed",
              border: "1px solid #fed7aa",
              padding: "20px",
              borderRadius: "8px",
              textDecoration: "none",
              textAlign: "center",
              transition: "transform 0.2s",
            }}
          >
            <h3
              style={{
                margin: "0 0 5px 0",
                color: "#c2410c",
                fontSize: "1.25rem",
                fontWeight: "600"
              }}
            >
              Recurring Purchases
            </h3>
            <p style={{ margin: 0, color: "#9a3412" }}>Manage subscriptions</p>
          </Link>

          <Link
            href="/"
            style={{
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              padding: "20px",
              borderRadius: "8px",
              textDecoration: "none",
              textAlign: "center",
              transition: "transform 0.2s",
            }}
          >
            <h3
              style={{
                margin: "0 0 5px 0",
                color: "#1e40af",
                fontSize: "1.25rem",
                fontWeight: "600"
              }}
            >
              Shop
            </h3>
            <p style={{ margin: 0, color: "#1d4ed8" }}>Browse products</p>
          </Link>
        </div>

        {/* Transaction History */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          }}
        >
          <h2
            style={{
              fontSize: "1.5rem",
              fontWeight: "bold",
              marginBottom: "20px",
              borderBottom: "1px solid #eee",
              paddingBottom: "10px",
            }}
          >
            Order History
          </h2>

          {error && (
            <div
              style={{
                background: "#fef2f2",
                color: "#991b1b",
                padding: "15px",
                borderRadius: "4px",
                marginBottom: "20px",
                border: "1px solid #fecaca",
              }}
            >
              {error}
            </div>
          )}

          {transactions.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0" }}>
              <p style={{ color: "#666", marginBottom: "15px" }}>No orders yet</p>
              <Link
                href="/"
                style={{
                  color: "#ff9900",
                  fontWeight: "bold",
                  textDecoration: "none",
                }}
              >
                Start shopping
              </Link>
            </div>
          ) : (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "20px",
              }}
            >
              {transactions.map((transaction, index) => (
                <div
                  key={transaction.transaction_id || index}
                  style={{
                    border: "1px solid #e5e7eb",
                    borderRadius: "8px",
                    padding: "20px",
                    transition: "box-shadow 0.2s",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "flex-start",
                      marginBottom: "15px",
                    }}
                  >
                    <div>
                      <h3
                        style={{
                          margin: "0 0 5px 0",
                          fontWeight: "600",
                        }}
                      >
                        Order #{" "}
                        {transaction.transaction_id
                          ? transaction.transaction_id.slice(0, 8)
                          : index + 1}
                      </h3>
                      <p
                        style={{
                          margin: 0,
                          color: "#666",
                          fontSize: "0.9rem",
                        }}
                      >
                        {new Date(
                          transaction.date ||
                            transaction.created_at ||
                            Date.now()
                        ).toLocaleDateString("en-US", {
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                    <span
                      style={{
                        padding: "4px 12px",
                        borderRadius: "20px",
                        fontSize: "0.85rem",
                        fontWeight: "600",
                        background:
                          transaction.status === "completed"
                            ? "#dcfce7"
                            : "#f3f4f6",
                        color:
                          transaction.status === "completed"
                            ? "#166534"
                            : "#374151",
                      }}
                    >
                      {transaction.status}
                    </span>
                  </div>

                  <div
                    style={{
                      fontSize: "1.25rem",
                      fontWeight: "bold",
                      color: "#333",
                      marginBottom: "15px",
                    }}
                  >
                    $
                    {(
                      transaction.total_amount ||
                      transaction.amount ||
                      0
                    ).toFixed(2)}
                  </div>

                  {(transaction.products || transaction.items) &&
                    (transaction.products || transaction.items).length > 0 && (
                      <div
                        style={{
                          borderTop: "1px solid #eee",
                          paddingTop: "15px",
                          marginTop: "10px",
                        }}
                      >
                        <p
                          style={{
                            margin: "0 0 10px 0",
                            fontSize: "0.9rem",
                            color: "#555",
                            fontWeight: "500",
                          }}
                        >
                          Items:
                        </p>
                        <ul
                          style={{
                            margin: 0,
                            paddingLeft: "20px",
                            color: "#666",
                          }}
                        >
                          {(transaction.products || transaction.items).map(
                            (item, idx) => (
                              <li
                                key={idx}
                                style={{
                                  marginBottom: "5px",
                                  fontSize: "0.9rem",
                                }}
                              >
                                {item.quantity}x{" "}
                                {item.name || item.product_name || `Product ${item.product_id}`} - $
                                {(item.price_per_unit || item.price || 0).toFixed(2)}
                              </li>
                            )
                          )}
                        </ul>
                      </div>
                    )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Penalties Section */}
        <div
          style={{
            background: "white",
            padding: "30px",
            borderRadius: "8px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            marginTop: "30px",
          }}
        >
          <h2
            style={{
              fontSize: "1.5rem",
              fontWeight: "bold",
              marginBottom: "20px",
              borderBottom: "1px solid #eee",
              paddingBottom: "10px",
              color: "#991b1b",
            }}
          >
            Penalties
          </h2>

          {penalties.length === 0 ? (
            <p style={{ color: "#666" }}>No penalties on record.</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
              {penalties.map((penalty, index) => (
                <div
                  key={index}
                  style={{
                    border: "1px solid #fecaca",
                    background: "#fef2f2",
                    borderRadius: "8px",
                    padding: "15px",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <h3 style={{ margin: "0 0 5px 0", color: "#991b1b", fontWeight: "600" }}>
                      {penalty.reason || "Penalty"}
                    </h3>
                    <span style={{ fontWeight: "bold", color: "#991b1b" }}>
                      -${(penalty.amount || 0).toFixed(2)}
                    </span>
                  </div>
                  <p style={{ margin: 0, color: "#7f1d1d", fontSize: "0.9rem" }}>
                    Date: {new Date(penalty.date || Date.now()).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
    </>
  );
}
