"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Navigation from "../../components/Navigation";
import "../../styles/login.css";

export default function ChangePasswordPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [isAuthed, setIsAuthed] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth/login");
    } else {
      setIsAuthed(true);
    }
  }, [router]);

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
    setSuccess("");
    setLoading(true);

    if (formData.new_password !== formData.confirm_password) {
      setError("New passwords do not match");
      setLoading(false);
      return;
    }

    try {
      await api.post("/auth/change-password", {
        old_password: formData.old_password,
        new_password: formData.new_password,
      });

      setSuccess("Password changed successfully!");
      setFormData({
        old_password: "",
        new_password: "",
        confirm_password: "",
      });

      setTimeout(() => {
        router.push("/dashboard");
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to change password");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthed) {
    return null;
  }

  return (
    <>
      <Navigation showOnAuth={true} />
      <main className="login-container">
        <div className="login-card">
          <h1 className="login-title">Change Password</h1>

          {error && <div className="login-error">{error}</div>}
          {success && <div className="login-success">{success}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <div>
              <label className="login-label">Current Password</label>
              <input
                type="password"
                name="old_password"
                className="login-input"
                value={formData.old_password}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label className="login-label">New Password</label>
              <input
                type="password"
                name="new_password"
                className="login-input"
                value={formData.new_password}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label className="login-label">Confirm New Password</label>
              <input
                type="password"
                name="confirm_password"
                className="login-input"
                value={formData.confirm_password}
                onChange={handleChange}
                required
              />
            </div>

            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? "Changing..." : "Change Password"}
            </button>
          </form>
        </div>
      </main>
    </>
  );
}
