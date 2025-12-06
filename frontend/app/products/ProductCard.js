"use client";

import { useState } from "react";
import api from "@/lib/api";

export default function ProductCard({ item }) {

    const [interval, setInterval] = useState(1);

    const addToCart = async () => {
        const savedUser = localStorage.getItem("user");
        if (!savedUser) {
            alert("Please login to add items to cart");
            return;
        }

        const user = JSON.parse(savedUser);
        const userId = user.user_id || user.id;

        try {
            await api.post(`/cart/${userId}/add?product_id=${item.product_id}&quantity=1`);
            alert("Item added to cart!");
        } catch (error) {
            alert("Failed to add item to cart");
        }
    };

    const createSubscription = async () => {
        const savedUser = localStorage.getItem("user");
        if (!savedUser) {
            alert("Please login to create a subscription");
            return;
        }

        const user = JSON.parse(savedUser);
        const userId = user.user_id || user.id;

        try {
            await api.post(`/subscriptions/create`, {
                user_id: String(userId),
                item_id: String(item.product_id),
                interval_days: Number(interval)
            });

            alert(`Subscription created! You will be charged every ${interval} day(s).`);
        } catch (error) {
            alert("Failed to create subscription");
        }
    };

    const aboutList = item.about_product
        ? item.about_product.split("|")
        : [];

    const userNames = item.user_name?.split(",") || [];
    const reviewTitles = item.review_title?.split(",") || [];
    const reviewContents = item.review_content?.split(",") || [];

    return (
        <div className="product-card expanded-card">

            <img 
                src={item.img_link}
                alt={item.product_name}
                className="product-img"
            />

            <h2 className="product-title">{item.product_name}</h2>

            <p className="product-price">
                <strong>{item.discounted_price}</strong>
                <span className="actual-price"> {item.actual_price}</span>
                <span className="discount"> ({item.discount_percentage} off)</span>
            </p>

            <button type="button" className="add-to-cart" onClick={addToCart}>
                Add to Cart
            </button>

            <div className="subscribe-section">
                <label className="subscribe-label">
                    How often? (days):
                </label>

                <input
                    type="number"
                    min="1"
                    className="subscribe-input"
                    value={interval}
                    onChange={(e) => {
                        const val = Number(e.target.value);
                        if (val > 0) setInterval(val);
                    }}
                />

                <button
                    type="button"
                    className="subscribe-btn"
                    onClick={createSubscription}
                >
                    Subscribe
                </button>
            </div>

            <p className="rating-line">
                Rating: {item.rating}/5
                <span className="rating-count"> ({item.rating_count} reviews)</span>
            </p>

            <div className="about-section">
                <strong>Item Description:</strong>
                <ul>
                    {aboutList.map((point, i) => (
                        <li key={i}>{point}</li>
                    ))}
                </ul>
            </div>

            <div className="reviews-section">
                <strong>Customer Reviews:</strong>
                {reviewTitles.map((title, i) => (
                    <div key={i} className="review-block">
                        <p className="review-title"><b>{title}</b></p>
                        <p className="review-content">
                            {reviewContents[i]}
                        </p>
                        <p className="review-user">
                            — {userNames[i] || "Unknown User"}
                        </p>
                    </div>
                ))}
            </div>

            <p className="stock-line">
                Current Stock: <strong>{item.quantity}</strong>
            </p>
        </div>
    );
}
