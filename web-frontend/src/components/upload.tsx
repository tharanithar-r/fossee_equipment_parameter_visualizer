import { RefreshCw, Upload } from "lucide-react"
import { Button } from "./ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { useRef, useState } from "react";
import { toast } from "sonner";
import { datasetAPI } from "@/lib/api";

interface UploadCSVProps {
  onUploadSuccess: () => void;  
}


const Upload_CSV = ({onUploadSuccess}: UploadCSVProps) => {

    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.csv')) {
      toast.error('Invalid file type. Please upload a CSV file.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    setUploading(true);
    try {
      await datasetAPI.upload(file);
      toast.success('Dataset uploaded successfully');
      await onUploadSuccess();
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Upload failed';

      // Show detailed error for CSV validation issues
      if (errorMessage.includes('Missing required columns')) {
        toast.error('CSV Validation Error', {
          description: errorMessage,
          duration: 5000,
        });
      } else {
        toast.error(errorMessage);
      }
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

    return (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Upload Dataset</CardTitle>
            <CardDescription>
              Upload a CSV file with equipment data. Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <Button
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
              >
                <Upload className="h-4 w-4 mr-2" />
                {uploading ? 'Uploading...' : 'Upload CSV'}
              </Button>
              <Button variant="outline" onClick={onUploadSuccess}>
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>
          </CardContent>
        </Card>
    )    
}

export {Upload_CSV};