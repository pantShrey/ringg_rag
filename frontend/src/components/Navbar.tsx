import { BotMessageSquare } from 'lucide-react';

type Page = "home" | "upload" | "query" | "analytics";

interface NavbarProps {
  activePage: Page;
  setActivePage: (page: Page) => void;
}

const NavLink = ({ page, activePage, setActivePage, children }: { page: Page, activePage: Page, setActivePage: (page: Page) => void, children: React.ReactNode }) => (
  <button
    onClick={() => setActivePage(page)}
    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
      activePage === page 
        ? 'bg-primary text-primary-foreground' 
        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
    }`}
  >
    {children}
  </button>
);

export default function Navbar({ activePage, setActivePage }: NavbarProps) {
  return (
    <nav className="border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-4">
            <BotMessageSquare className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold">RAG Assistant</span>
          </div>
          <div className="flex items-center space-x-2">
            <NavLink page="home" activePage={activePage} setActivePage={setActivePage}>Home</NavLink>
            <NavLink page="upload" activePage={activePage} setActivePage={setActivePage}>Upload</NavLink>
            <NavLink page="query" activePage={activePage} setActivePage={setActivePage}>Query</NavLink>
            <NavLink page="analytics" activePage={activePage} setActivePage={setActivePage}>Analytics</NavLink>
          </div>
        </div>
      </div>
    </nav>
  );
}