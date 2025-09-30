import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button';
import { Loader2, Server, ServerCrash, Upload, Search, LineChart } from 'lucide-react';
import toast from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type Page = "home" | "upload" | "query" | "analytics";

interface HomePageProps {
  setActivePage: (page: Page) => void;
}

export default function HomePage({ setActivePage }: HomePageProps) {
  const [healthStatus, setHealthStatus] = useState<'checking' | 'healthy' | 'unhealthy'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
          setHealthStatus('healthy');
        } else {
          setHealthStatus('unhealthy');
        }
      } catch (error) {
        setHealthStatus('unhealthy');
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">RAG Document Assistant</h2>
        <p className="text-muted-foreground mt-2">Upload documents, query them with AI, and extract insights</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>API Health Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center space-x-4 p-4 rounded-md bg-secondary">
              {healthStatus === 'checking' && <Loader2 className="h-6 w-6 animate-spin" />}
              {healthStatus === 'healthy' && <Server className="h-6 w-6 text-green-500" />}
              {healthStatus === 'unhealthy' && <ServerCrash className="h-6 w-6 text-red-500" />}
              <span className="font-medium">
                {healthStatus === 'checking' && 'Checking connection...'}
                {healthStatus === 'healthy' && 'API Connected'}
                {healthStatus === 'unhealthy' && 'API Disconnected'}
              </span>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col space-y-4">
            <Button onClick={() => setActivePage('upload')}>
              <Upload className="mr-2 h-4 w-4" /> Upload Document
            </Button>
            <Button variant="outline" onClick={() => setActivePage('query')}>
              <Search className="mr-2 h-4 w-4" /> Query Documents
            </Button>
            <Button variant="outline" onClick={() => setActivePage('analytics')}>
              <LineChart className="mr-2 h-4 w-4" /> View Analytics
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}