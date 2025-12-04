"use client";

import "./globals.css";

import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main className="main-container">

      <nav className="navbar">
        <div className="nav-left">
          <Link href="/">
            <Image 
              src="/logo-new.png"
              alt="Site Logo"
              width={150}
              height={70}
              className="nav-logo"
            />
          </Link>
        </div>

        <div className="nav-center">
          <input 
            type="text" 
            placeholder="Search products…" 
            className="search-bar"
          />
        </div>

        <div className="nav-right">
          <a href="/cart" className="nav-cart">
            <img 
              src="/cart.svg" 
              alt="Cart"
              className="cart-img"
            />
          </a>

          <a href="/dashboard" className="nav-profile">
            <img 
              src="/profile-icon.svg" 
              alt="Profile"
              className="profile-img"
            />
          </a>
        </div>
      </nav>

      <section className="content">
        <h1>Welcome to Not Amazon</h1>
        <p>Your all-in-one shopping platform — created by StackSquad</p>

        <div className="feature-card">
          <h2>Products of the Week</h2>
          <p>Need to implement</p>
        </div>
      </section>

    </main>
  );
}