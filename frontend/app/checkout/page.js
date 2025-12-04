"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Link from "next/link";
import StripeProvider from "@/app/components/StripeProvider";
import StripePaymentForm from "@/app/components/StripePaymentForm";

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
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md text-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Your Cart is Empty
          </h1>
          <p className="text-gray-600 mb-6">
            Add some items to your cart to get started!
          </p>
          <Link
            href="/"
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg inline-block"
          >
            Continue Shopping
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">Checkout</h1>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {/* Cart Items */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Order Summary
            </h2>
            <div className="space-y-4">
              {cart.map((item) => (
                <div
                  key={item.product_id}
                  className="flex justify-between items-center p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800">
                      {item.name}
                    </h3>
                    <p className="text-gray-600">${item.price_per_unit.toFixed(2)}</p>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() =>
                          handleUpdateQuantity(
                            item.product_id,
                            Math.max(0, item.quantity - 1)
                          )
                        }
                        className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                      >
                        -
                      </button>
                      <span className="w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() =>
                          handleUpdateQuantity(item.product_id, item.quantity + 1)
                        }
                        className="px-2 py-1 bg-gray-200 rounded hover:bg-gray-300"
                      >
                        +
                      </button>
                    </div>

                    <div className="w-24 text-right">
                      <p className="font-semibold text-gray-800">
                        ${item.subtotal.toFixed(2)}
                      </p>
                    </div>

                    <button
                      onClick={() => handleRemoveItem(item.product_id)}
                      className="px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Totals */}
          <div className="bg-gray-50 p-4 rounded-lg mb-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-700">Subtotal:</span>
              <span className="text-gray-800 font-semibold">
                ${total.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-700">Tax (estimated):</span>
              <span className="text-gray-800 font-semibold">
                ${(total * 0.1).toFixed(2)}
              </span>
            </div>
            <div className="border-t border-gray-300 pt-2 flex justify-between items-center">
              <span className="text-lg font-semibold text-gray-800">Total:</span>
              <span className="text-lg font-semibold text-indigo-600">
                ${(total * 1.1).toFixed(2)}
              </span>
            </div>
          </div>

          {/* Payment Section */}
          {!showPaymentForm ? (
            <>
              <button
                onClick={handleCheckout}
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition duration-200 mb-4"
              >
                {loading ? "Processing..." : "Proceed to Payment"}
              </button>

              <Link
                href="/"
                className="block text-center text-indigo-600 hover:underline"
              >
                Continue Shopping
              </Link>
            </>
          ) : (
            <div className="mt-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Payment Details
              </h2>
              <StripeProvider clientSecret={clientSecret}>
                <StripePaymentForm
                  clientSecret={clientSecret}
                  onSuccess={handlePaymentSuccess}
                  onError={handlePaymentError}
                />
              </StripeProvider>
              <button
                onClick={() => setShowPaymentForm(false)}
                className="mt-4 w-full text-center text-gray-600 hover:underline"
              >
                Cancel Payment
              </button>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
