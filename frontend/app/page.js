"use client";

import "./globals.css";

import { useState } from "react";
import Image from "next/image";
import ProductCard from "./products/ProductCard";

export default function Home() {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);

  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [category, setCategory] = useState("");
  const [minRating, setMinRating] = useState("");

  const submitSearch = async (e) => {
    if (e.key !== "Enter") return;

    console.log("SubmitSearch TRIGGERED");

    if (!search.trim()) {
      setResults([]);
      return;
    }

    setSearching(true);

    try {
      const res = await fetch(
        `http://localhost:8000/items/search?keyword=${encodeURIComponent(search)}`
      );

      const data = await res.json();
      console.log("SEARCH RESULTS RAW:", data);

      setResults(data);
    } catch (err) {
      console.error("Search failed:", err);
    }

    setSearching(false);
  };

  async function ApplyFilters() {
    console.log("ApplyFilters TRIGGERED");

    const params = new URLSearchParams();

    if (search) params.append("keyword", search);
    if (minPrice) params.append("min_price", minPrice);
    if (maxPrice) params.append("max_price", maxPrice);
    if (category) params.append("category", category);
    if (minRating) params.append("rating", minRating);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/items/search/filter?${params.toString()}`
      );

      if (!res.ok) {
        console.error("FILTER ERROR", res.status);
        setResults([]);
        return;
      }

      const data = await res.json();
      console.log("FILTER RESULTS RAW:", data);

      setResults(data);
    } catch (err) {
      console.error("Filter failed:", err);
    }
  }

  return (
    <main className="main-container">

      <nav className="navbar">
        <div className="nav-left">
          <a href="/">
            <Image 
              src="/logo-new.png"
              alt="Site Logo"
              width={150}
              height={70}
              className="nav-logo"
            />
          </a>
        </div>

        <div className="nav-center">
          <input 
            type="text"
            placeholder="Search products"
            className="search-bar"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={submitSearch}
          />
        </div>

        <div className="nav-right">
          <a href="/cart">
            <img src="/cart.svg" alt="Cart" className="cart-img" />
          </a>

          <a href="/dashboard">
            <img src="/profile-icon.svg" alt="Profile" className="profile-img" />
          </a>
        </div>
      </nav>

      {results.length > 0 && (
        <div className="filter-bar">
          <input
            type="number"
            placeholder="Min Price"
            className="filter-input"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
          />

          <input
            type="number"
            placeholder="Max Price"
            className="filter-input"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />

          <input
            type="text"
            placeholder="Category"
            className="filter-input"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />

          <input
            type="number"
            step="0.1"
            placeholder="Min Rating"
            className="filter-input"
            value={minRating}
            onChange={(e) => setMinRating(e.target.value)}
          />

          <button className="filter-btn" onClick={ApplyFilters}>
            Apply Filters
          </button>
        </div>
      )}

      {search.length > 0 && (
        <div className="search-results">
          {!searching && results.length === 0 && (
            <p>No results found.</p>
          )}

          <div className="product-grid">
            {Array.isArray(results) && results.length > 0 ? (
              results.map((item) => {
                if (!item || !item.product_id) {
                  console.warn("Invalid item skipped:", item);
                  return null;
                }
                return <ProductCard key={item.product_id} item={item} />;
              })
            ) : (
              <p className="no-results">No products to display.</p>
            )}
          </div>
        </div>
      )}

      {search.length === 0 && (
        <section className="content">
          <h1>Welcome to Not Amazon</h1>
          <p>Your all-in-one shopping platform — created by StackSquad</p>

          <div className="feature-card">
            <h2>Featured Products</h2>
            <p>Product grid coming soon.</p>
          </div>
        </section>
      )}
    </main>
  );
}