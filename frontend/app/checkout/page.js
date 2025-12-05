"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";
import StripeProvider from "@/app/components/StripeProvider";
import StripePaymentForm from "@/app/components/StripePaymentForm";
import Navigation from "../components/Navigation";
import "../styles/checkout.css";

export default function CheckoutPage() {
  const router = useRouter();
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isAuthed, setIsAuthed] = useState(false);
  const [total, setTotal] = useState(0);
  const [clientSecret, setClientSecret] = useState("");
  const [showPaymentForm, setShowPaymentForm] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/auth/login");
    } else {
      setIsAuthed(true);
      loadCart();
    }
  }, [router]);

  const loadCart = async () => {
    try {
      const savedUser = localStorage.getItem("user");
      if (!savedUser) return;
      
      const user = JSON.parse(savedUser);
      const userId = user.user_id || user.id;

      const response = await api.get(`/transactions/cart/${userId}`);
      setCart(response.data.items);
      setTotal(response.data.total);
    } catch (err) {
      console.error("Error loading cart:", err);
      //cart is empty or doesn't exist
      if (err.response && err.response.status === 404) {
        setCart([]);
        setTotal(0);
      }
    }
  };

  const handleCheckout = async () => {
    setLoading(true);
    setError("");

    try {
      const savedUser = localStorage.getItem("user");
      const user = JSON.parse(savedUser);
      const userId = user.user_id || user.id;

      const response = await api.post(`/transactions/create-payment-intent/${userId}`, {
        currency: "cad"
      });

      const { client_secret, payment_intent_id } = response.data;

      if (!client_secret) {
        setError("Failed to create payment intent");
        return;
      }

      localStorage.setItem("payment_intent_id", payment_intent_id);
      setClientSecret(client_secret);
      setShowPaymentForm(true);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to process payment. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveItem = async (productId) => {
    try {
      const savedUser = localStorage.getItem("user");
      const user = JSON.parse(savedUser);
      const userId = user.user_id || user.id;

      await api.delete(`/cart/${userId}/remove?product_id=${productId}`);
      loadCart();
    } catch (err) {
      console.error("Error removing item:", err);
    }
  };

  const handleUpdateQuantity = async (productId, quantity) => {
    if (quantity <= 0) {
      handleRemoveItem(productId);
      return;
    }

    try {
      const savedUser = localStorage.getItem("user");
      const user = JSON.parse(savedUser);
      const userId = user.user_id || user.id;

      await api.patch(`/cart/${userId}/update?product_id=${productId}&quantity=${quantity}`);
      loadCart();
    } catch (err) {
      console.error("Error updating quantity:", err);
    }
  };

  const handlePaymentSuccess = async (paymentIntent) => {
    try {
      await api.post(`/transactions/confirm-payment/${paymentIntent.id}`);
    } catch (err) {
      console.error("Failed to confirm payment with backend:", err);
    }

    localStorage.removeItem("cart");
    localStorage.removeItem("payment_intent_id");
    setCart([]);
    setShowPaymentForm(false);
    
    alert("Payment successful! Your order has been placed.");
    
    router.push("/dashboard");
  };

  const handlePaymentError = (error) => {
    setError("Payment failed: " + error.message);
    setShowPaymentForm(false);
  };

  if (!isAuthed) {
    return null;
  }

  if (cart.length === 0) {
    return (
      <>
        <Navigation showOnAuth={true} />
        <main className="checkout-empty-container">
          <div className="checkout-empty-card">
            <h1>Your Cart is Empty</h1>
            <p>Add some items to your cart to get started!</p>
            <Link href="/" className="checkout-empty-btn">
              Continue Shopping
            </Link>
          </div>
        </main>
      </>
    );
  }


  return (
    <>
      <Navigation showOnAuth={true} />

      <main className="checkout-container">
        <div className="checkout-card">
          <h1 className="checkout-title">Checkout</h1>

          {error && <div className="checkout-error">{error}</div>}

          <h2 className="checkout-section-title">Order Summary</h2>

          <div className="checkout-items">
            {cart.map((item) => (
              <div key={item.product_id} className="checkout-item">
                <div className="checkout-item-info">
                  <h3>{item.name}</h3>
                  <p>${item.price_per_unit.toFixed(2)}</p>
                </div>

                <div className="checkout-controls">
                  <button
                    onClick={() =>
                      handleUpdateQuantity(
                        item.product_id,
                        Math.max(0, item.quantity - 1)
                      )
                    }
                    className="checkout-qty-btn"
                  >
                    -
                  </button>

                  <span className="checkout-qty">{item.quantity}</span>

                  <button
                    onClick={() =>
                      handleUpdateQuantity(
                        item.product_id,
                        item.quantity + 1
                      )
                    }
                    className="checkout-qty-btn"
                  >
                    +
                  </button>

                  <p className="checkout-subtotal">
                    ${item.subtotal.toFixed(2)}
                  </p>

                  <button
                    onClick={() => handleRemoveItem(item.product_id)}
                    className="checkout-remove-btn"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="checkout-total-box">
            <div>
              <span>Subtotal:</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <div>
              <span>Tax (10%):</span>
              <span>${(total * 0.1).toFixed(2)}</span>
            </div>
            <div className="checkout-total">
              <span>Total:</span>
              <span>${(total * 1.1).toFixed(2)}</span>
            </div>
          </div>

          {!showPaymentForm ? (
            <>
              <button
                onClick={handleCheckout}
                disabled={loading}
                className="checkout-btn"
              >
                {loading ? "Processing..." : "Proceed to Payment"}
              </button>

              <Link href="/" className="checkout-back-shop">
                Continue Shopping
              </Link>
            </>
          ) : (
            <div className="checkout-payment-box">
              <h2>Payment Details</h2>

              <StripeProvider clientSecret={clientSecret}>
                <StripePaymentForm
                  clientSecret={clientSecret}
                  onSuccess={handlePaymentSuccess}
                  onError={handlePaymentError}
                />
              </StripeProvider>

              <button
                onClick={() => setShowPaymentForm(false)}
                className="checkout-cancel-btn"
              >
                Cancel Payment
              </button>
            </div>
          )}
        </div>
      </main>
    </>
  );
}