import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Slider } from './ui/slider';
import { Loader2, Copy } from 'lucide-react';
import toast from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface QueryResult {
  text: string;
  chunk_id: number;
  similarity_score: number;
  document_name: string;
  vector_id: string;
}

export default function QueryPage() {
  const [documentName, setDocumentName] = useState('');
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(3);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<QueryResult[]>([]);

  const handleQuery = async () => {
    setIsLoading(true);
    setResults([]);
    try {
      const params = new URLSearchParams({
        document_name: documentName,
        query,
        top_k: topK.toString(),
      });
      const response = await fetch(`${API_URL}/query?${params}`);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch results');
      }

      const data = await response.json();
      setResults(data.results);
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">Query Documents</h2>
        <p className="text-muted-foreground mt-2">Search through your documents using natural language</p>
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        <div className="md:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Search Parameters</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="doc-name" className="text-sm font-medium">Document Name</label>
                <Input id="doc-name" value={documentName} onChange={(e) => setDocumentName(e.target.value)} placeholder="e.g., my_document.pdf" />
              </div>
              <div className="space-y-2">
                <label htmlFor="query" className="text-sm font-medium">Query</label>
                <Textarea id="query" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="What is the main topic?" />
              </div>
              <div className="space-y-2">
                <label htmlFor="top-k" className="text-sm font-medium">Number of Results: {topK}</label>
                <Slider id="top-k" value={[topK]} onValueChange={(value) => setTopK(value[0])} min={1} max={20} step={1} />
              </div>
              <Button onClick={handleQuery} disabled={isLoading || !documentName || !query} className="w-full">
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Search
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="md:col-span-2">
          {isLoading && (
            <div className="flex justify-center items-center h-full">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          )}

          {!isLoading && results.length === 0 && (
            <div className="flex justify-center items-center h-full p-8 text-center border-2 border-dashed rounded-lg">
                <p className="text-muted-foreground">Results will appear here.</p>
            </div>
          )}

          {!isLoading && results.length > 0 && (
            <div className="space-y-4">
              {results.map((result, index) => (
                <Card key={index}>
                  <CardHeader className="flex flex-row items-center justify-between pb-2">
                    <CardTitle className="text-sm font-medium">Similarity: {(result.similarity_score * 100).toFixed(2)}%</CardTitle>
                    <Button variant="ghost" size="sm" onClick={() => copyToClipboard(result.text)}>
                      <Copy className="h-4 w-4" />
                    </Button>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">{result.text}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}