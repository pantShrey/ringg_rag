import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ToastProvider } from '@/components/ToastProvider'

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RAG Document Assistant",
  description: "Upload, search, and analyze your documents with ease.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <ToastProvider />
        {children}
      </body>
    </html>
  );
}