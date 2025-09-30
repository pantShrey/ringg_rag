"use client";

import { useState } from 'react';
import Navbar from '@/components/Navbar';
import HomePage from '@/components/HomePage';
import UploadPage from '@/components/Upload';
import QueryPage from '@/components/QueryPage';
import AnalyticsPage from '@/components/AnalyticsPage';

type Page = "home" | "upload" | "query" | "analytics";

export default function Home() {
  const [activePage, setActivePage] = useState<Page>("home");

  const renderPage = () => {
    switch (activePage) {
      case "home":
        return <HomePage setActivePage={setActivePage} />;
      case "upload":
        return <UploadPage />;
      case "query":
        return <QueryPage />;
      case "analytics":
        return <AnalyticsPage />;
      default:
        return <HomePage setActivePage={setActivePage} />;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar activePage={activePage} setActivePage={setActivePage} />
      <main className="container mx-auto px-4 py-8">
        {renderPage()}
      </main>
    </div>
  );
}