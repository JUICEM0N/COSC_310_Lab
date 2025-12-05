"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";
import Navigation from "../../components/Navigation";
import "../../styles/register.css";

export default function RegisterPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

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

    // do passwords match
    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    try {
      const response = await api.post("/auth/register", {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });

      // Registration successful
      router.push("/auth/login?registered=true");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navigation showOnAuth={true} />

      <main className="register-container">
        <div className="register-card">
          <h1 className="register-title">Create Account</h1>

          {error && <div className="register-error">{error}</div>}

          <form onSubmit={handleSubmit} className="register-form">
            <label className="register-label">Username</label>
            <input
              type="text"
              name="username"
              className="register-input"
              placeholder="Enter username"
              value={formData.username}
              onChange={handleChange}
              required
            />

            <label className="register-label">Email</label>
            <input
              type="email"
              name="email"
              className="register-input"
              placeholder="Enter email"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <label className="register-label">Password</label>
            <input
              type="password"
              name="password"
              className="register-input"
              placeholder="Enter password"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <label className="register-label">Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              className="register-input"
              placeholder="Confirm password"
              value={formData.confirm_password}
              onChange={handleChange}
              required
            />

            <button type="submit" disabled={loading} className="register-btn">
              {loading ? "Creating Account..." : "Register"}
            </button>
          </form>

          <p className="register-login-text">
            Already have an account?{" "}
            <Link href="/auth/login" className="register-login-link">
              Login
            </Link>
          </p>
        </div>
      </main>
    </>
  );
}
