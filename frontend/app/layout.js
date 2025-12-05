import Navigation from "./components/Navigation";
import "./globals.css";

export const metadata = {
  title: 'Bitcoin Miner',
  description: 'An e-commerce site by StackSquad',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "sans-serif" }}>
        <Navigation />
        {children}
      </body>
    </html>
  );
}