"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Navigation from "@/app/components/Navigation";
import "@/app/styles/subscriptions.css";

export default function SubscriptionsPage() {
    const router = useRouter();
    const [subs, setSubs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const savedUser = localStorage.getItem("user");
        if (!savedUser) {
        router.push("/auth/login");
        return;
        }

        const user = JSON.parse(savedUser);
        loadSubscriptions(user.user_id || user.id);
    }, []);

    const loadSubscriptions = async (userId) => {
        try {
        const response = await api.get(`/subscriptions/${userId}`);
        setSubs(response.data || []);
        } catch (err) {
        console.error("Failed to load subscriptions:", err);
        } finally {
        setLoading(false);
        }
    };

    return (
        <>
        <Navigation showOnAuth={true} />

        <main className="subs-container">
            <h1 className="subs-title">Recurring Purchases</h1>

            {loading ? (
            <p className="subs-loading">Loading...</p>
            ) : subs.length === 0 ? (
            <p className="subs-empty">You currently have no recurring purchases.</p>
            ) : (
            <div className="subs-list">
                {subs.map((sub) => (
                <div key={sub.id} className="subs-card">
                    <div className="subs-row">
                    <span className="subs-label">Product ID:</span>
                    <span className="subs-value">{sub.product_id}</span>
                    </div>

                    <div className="subs-row">
                    <span className="subs-label">Interval:</span>
                    <span className="subs-value">{sub.interval_days} days</span>
                    </div>

                    <div className="subs-row">
                    <span className="subs-label">Next Renewal:</span>
                    <span className="subs-value">
                        {new Date(sub.next_renewal).toLocaleString()}
                    </span>
                    </div>

                    <div className="subs-row">
                    <span className="subs-label">Status:</span>
                    <span
                        className={`subs-status ${
                        sub.active ? "subs-active" : "subs-inactive"
                        }`}
                    >
                        {sub.active ? "Active" : "Paused"}
                    </span>
                    </div>
                </div>
                ))}
            </div>
            )}
        </main>
        </>
  );
}
