import { useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { UploadCloud, File, X } from 'lucide-react';
import toast from 'react-hot-toast';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const onDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setFile(event.dataTransfer.files[0]);
    }
  }, []);

  const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };
  
  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${API_URL}/upload`, true);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentComplete = (event.loaded / event.total) * 100;
        setUploadProgress(percentComplete);
      }
    };

    xhr.onload = () => {
      setIsUploading(false);
      if (xhr.status === 200) {
        toast.success('File uploaded successfully!');
        setFile(null);
      } else {
        const errorResponse = JSON.parse(xhr.responseText);
        toast.error(`Upload failed: ${errorResponse.error || 'Server error'}`);
      }
    };
    
    xhr.onerror = () => {
      setIsUploading(false);
      toast.error('Upload failed. Check console for details.');
    };

    xhr.send(formData);
  };

  return (
    <div className="space-y-8">
        <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight">Upload Document</h2>
            <p className="text-muted-foreground mt-2">Upload documents to make them searchable</p>
        </div>
        <Card className="max-w-2xl mx-auto">
            <CardContent className="p-6">
                {!file ? (
                    <div
                        onDrop={onDrop}
                        onDragOver={onDragOver}
                        className="flex flex-col items-center justify-center p-12 border-2 border-dashed rounded-lg cursor-pointer hover:border-primary"
                        onClick={() => document.getElementById('file-input')?.click()}
                    >
                        <UploadCloud className="w-12 h-12 text-muted-foreground" />
                        <p className="mt-4 font-semibold">Click or drag file to this area to upload</p>
                        <p className="text-sm text-muted-foreground">Supports: PDF, DOCX, JSON, TXT</p>
                        <Input id="file-input" type="file" className="hidden" onChange={handleFileChange} accept=".pdf,.docx,.json,.txt" />
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 border rounded-lg">
                            <div className="flex items-center space-x-3">
                                <File className="w-6 h-6" />
                                <div>
                                    <p className="font-medium">{file.name}</p>
                                    <p className="text-sm text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
                                </div>
                            </div>
                            <Button variant="ghost" size="icon" onClick={() => setFile(null)}>
                                <X className="w-4 h-4" />
                            </Button>
                        </div>


                        <Button onClick={handleUpload} disabled={isUploading || !file} className="w-full">
                            {isUploading ? 'Uploading...' : 'Upload File'}
                        </Button>
                    </div>
                )}
            </CardContent>
        </Card>
    </div>
  );
}