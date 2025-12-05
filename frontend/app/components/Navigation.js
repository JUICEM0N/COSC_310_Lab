"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

export default function Navigation({ search, setSearch, submitSearch, showOnAuth = false }) {
  const pathname = usePathname();
  const router = useRouter();

  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const user = localStorage.getItem("user");

    if (token && user) {
      setIsLoggedIn(true);
      try {
        const userData = JSON.parse(user);
        setUsername(userData.username);
      } catch (err) {
        console.error("Error parsing user data:", err);
      }
    }
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    setIsLoggedIn(false);
    router.push("/auth/login");
  };

  if (!showOnAuth && pathname?.startsWith("/auth")) return null;

  return (
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
        {isLoggedIn ? (
          <>
            <Link href="/dashboard" className="nav-link">
              Dashboard
            </Link>

            <Link href="/cart">
              <img src="/cart.svg" alt="Cart" className="cart-img" />
            </Link>

            <div className="nav-profile">
              <span style={{ marginRight: "10px", fontWeight: "500" }}>
                Hi, {username}
              </span>

              <button
                onClick={handleLogout}
                style={{
                  background: "#ff4444",
                  color: "white",
                  border: "none",
                  padding: "8px 16px",
                  borderRadius: "4px",
                  cursor: "pointer",
                  fontWeight: "bold"
                }}
              >
                Logout
              </button>
            </div>
          </>
        ) : (
          <>
            <Link href="/auth/login" className="nav-link">
              Login
            </Link>

            <Link
              href="/auth/register"
              style={{
                background: "#ff9900",
                color: "white",
                textDecoration: "none",
                padding: "8px 16px",
                borderRadius: "4px",
                fontWeight: "bold",
                marginLeft: "10px"
              }}
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}