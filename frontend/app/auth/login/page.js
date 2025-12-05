"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";
import Navigation from "../../components/Navigation";
import "../../styles/login.css";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (searchParams.get("registered") === "true") {
      setSuccess("Registration successful! Please log in.");
    }
  }, [searchParams]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", {
        email: formData.email,
        password: formData.password,
      });

      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      router.push("/");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Login failed. Check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navigation showOnAuth={true} />

      <main className="login-container">
        <div className="login-card">
          <h1 className="login-title">Login</h1>

          {success && <div className="login-success">{success}</div>}
          {error && <div className="login-error">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <label className="login-label">Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter email"
              className="login-input"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <label className="login-label">Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter password"
              className="login-input"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p className="login-register-text">
            Don’t have an account?{" "}
            <Link href="/auth/register" className="login-register-link">
              Register
            </Link>
          </p>
        </div>
      </main>
    </>
  );
}
