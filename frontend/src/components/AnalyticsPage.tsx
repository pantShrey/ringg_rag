import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Loader2, Sigma } from 'lucide-react';
import toast from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface AnalyticsResult {
  document: string;
  field: string;
  operation: string;
  result: number;
}

export default function AnalyticsPage() {
  const [documentName, setDocumentName] = useState('');
  const [field, setField] = useState('');
  const [operation, setOperation] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalyticsResult | null>(null);

  const handleAnalytics = async () => {
    setIsLoading(true);
    setResult(null);
    try {
      const params = new URLSearchParams({
        document_name: documentName,
        field,
        operation,
      });
      const response = await fetch(`${API_URL}/json-query?${params}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch analytics');
      }

      const data = await response.json();
      setResult(data);
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">Document Analytics</h2>
        <p className="text-muted-foreground mt-2">Extract numerical insights from your JSON documents</p>
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Analytics Parameters</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="json-doc-name" className="text-sm font-medium">Document Name</label>
              <Input id="json-doc-name" value={documentName} onChange={(e) => setDocumentName(e.target.value)} placeholder="e.g., data.json" />
            </div>
            <div className="space-y-2">
              <label htmlFor="field" className="text-sm font-medium">Field</label>
              <Input id="field" value={field} onChange={(e) => setField(e.target.value)} placeholder="e.g., price" />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Operation</label>
              <Select onValueChange={setOperation}>
                <SelectTrigger>
                  <SelectValue placeholder="Select an operation" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="max">Maximum</SelectItem>
                  <SelectItem value="min">Minimum</SelectItem>
                  <SelectItem value="sum">Sum</SelectItem>
                  <SelectItem value="avg">Average</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button onClick={handleAnalytics} disabled={isLoading || !documentName || !field || !operation} className="w-full">
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Calculate
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Result</CardTitle>
          </CardHeader>
          <CardContent className="flex items-center justify-center h-full text-center">
            {isLoading && <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />}
            
            {!isLoading && !result && (
              <div className=" text-muted-foreground space-y-2">
                <Sigma className="mx-auto h-12 w-12" />
                <p className="mt-4">Your result will appear here.</p>
              </div>
            )}

            {!isLoading && result && (
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground capitalize">{result.operation} of "{result.field}"</p>
                <p className="text-5xl font-bold tracking-tighter">{result.result.toLocaleString()}</p>
                <p className="text-sm text-muted-foreground mt-2">{result.document}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}