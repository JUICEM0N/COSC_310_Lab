"use client";

import "./globals.css";
import "./styles/home.css";
import "./styles/navbar.css";
import "./styles/search.css";
import "./styles/ProductCard.css";

import { useState, useEffect } from "react";
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

  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/items/`);
        const data = await res.json();
        setProducts(data);
        setResults(data);
      } catch (err) {
        console.error("Failed to fetch products:", err);
      }
    };

    fetchProducts();
  }, []);

  const submitSearch = async (e) => {
    if (e.key !== "Enter") return;

    if (!search.trim()) {
      setResults(products);
      return;
    }

    setSearching(true);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/items/search?keyword=${encodeURIComponent(
          search
        )}`
      );

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Search failed:", err);
    }

    setSearching(false);
  };

  async function ApplyFilters() {
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
        setResults([]);
        return;
      }

      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Filter failed:", err);
    }
  }

  return (
    <main className="home-container">
      <div className="filters-sidebar">
        <h2>Filters</h2>

        <div className="filter-group">
          <label>Price Range</label>
          <input
            type="number"
            placeholder="Min"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label>Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="">All</option>
            <option value="electronics">Electronics</option>
            <option value="fashion">Fashion</option>
            <option value="home">Home</option>
            <option value="books">Books</option>
            <option value="sports">Sports</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Minimum Rating</label>
          <select
            value={minRating}
            onChange={(e) => setMinRating(e.target.value)}
          >
            <option value="">Any</option>
            <option value="4">4 Stars & Up</option>
            <option value="3">3 Stars & Up</option>
            <option value="2">2 Stars & Up</option>
            <option value="1">1 Star & Up</option>
          </select>
        </div>

        <button onClick={ApplyFilters} className="apply-filters-btn">
          Apply Filters
        </button>
      </div>

      <div className="products-main-content">
        <div className="products-grid">
          {searching ? (
            <p>Searching...</p>
          ) : results.length > 0 ? (
            results.map((product, index) => (
              <ProductCard key={`${product.product_id}-${index}`} item={product} />
            ))
          ) : (
            <p>No products found.</p>
          )}
        </div>
      </div>
    </main>
  );
}