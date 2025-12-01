import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Welcome to Not Amazon</h1>
      <p>Amazon Clone, Jeff pls don't sue us :)</p>
      <div style={{ marginTop: "1rem", display: "flex", gap: "1rem" }}>
        <Link href="/login">Login</Link>
        <Link href="/signup">Sign Up</Link>
        <Link href="/products">Products</Link>
        <Link href="/cart">Cart</Link>
        <Link href="/admin">Admin</Link>
      </div>
    </main>
  );
}