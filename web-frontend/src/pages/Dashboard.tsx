import { useState, useEffect } from 'react';
import { useTheme } from '@/contexts/ThemeContext';
import { datasetAPI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { Download, Trash2 } from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { Bar, Doughnut } from 'react-chartjs-2';
import { getDoughnutOptions, getBarOptions, getChartColors } from '@/lib/chartConfig';
import { NavBar } from '@/components/navbar';
import { Upload_CSV } from '@/components/upload';
import { EquipmentDataTable } from '@/components/equipment-data-table';
import { columns } from '@/components/equipment-columns';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, ChartDataLabels);

interface Dataset {
  id: number;
  name: string;
  uploaded_at: string;
  total_count: number;
  equipment_count: number;
}

interface Equipment {
  id: number;
  equipment_name: string;
  equipment_type: string;
  flowrate: number;
  pressure: number;
  temperature: number;
}

interface DatasetDetail {
  id: number;
  name: string;
  uploaded_at: string;
  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;
  min_flowrate: number;
  max_flowrate: number;
  min_pressure: number;
  max_pressure: number;
  min_temperature: number;
  max_temperature: number;
  equipment: Equipment[];
}

interface Summary {
  id: number;
  name: string;
  uploaded_at: string;
  total_count: number;
  statistics: {
    flowrate: { avg: number; min: number; max: number };
    pressure: { avg: number; min: number; max: number };
    temperature: { avg: number; min: number; max: number };
  };
  type_distribution: Array<{ equipment_type: string; count: number }>;
}

export default function Dashboard() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<DatasetDetail | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);
  const { theme } = useTheme();

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await datasetAPI.list();
      setDatasets(response.data);
      if (response.data.length > 0 && !selectedDataset) {
        fetchDatasetDetails(response.data[0].id);
      }
    } catch (error) {
      toast.error('Failed to fetch datasets');
    }
  };

  const fetchDatasetDetails = async (id: number) => {
    setLoading(true);
    try {
      const [detailResponse, summaryResponse] = await Promise.all([
        datasetAPI.get(id),
        datasetAPI.summary(id),
      ]);
      setSelectedDataset(detailResponse.data);
      setSummary(summaryResponse.data);
    } catch (error) {
      toast.error('Failed to fetch dataset details');
    } finally {
      setLoading(false);
    }
  };



  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this dataset?')) return;
    try {
      await datasetAPI.delete(id);
      toast.success('Dataset deleted');
      await fetchDatasets();
      if (selectedDataset?.id === id) {
        setSelectedDataset(null);
        setSummary(null);
      }
    } catch (error) {
      toast.error('Failed to delete dataset');
    }
  };

  const handleDownloadPDF = async () => {
    if (!selectedDataset) return;
    try {
      const response = await datasetAPI.downloadPDF(selectedDataset.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${selectedDataset.name}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('PDF downloaded');
    } catch (error) {
      toast.error('Failed to download PDF');
    }
  };

  // Get chart colors with current theme
  const chartColors = getChartColors(theme);

  const typeDistributionData = summary
    ? {
      labels: summary.type_distribution.map((t) => t.equipment_type),
      datasets: [
        {
          label: 'Equipment Count',
          data: summary.type_distribution.map((t) => t.count),
          backgroundColor: chartColors.colors,
          borderColor: chartColors.borderColors,
          borderWidth: 2,
        },
      ],
    }
    : null;

  const parametersData = summary
    ? {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average',
          data: [
            summary.statistics.flowrate.avg,
            summary.statistics.pressure.avg,
            summary.statistics.temperature.avg,
          ],
          backgroundColor: chartColors.colors[0],
          borderColor: chartColors.borderColors[0],
          borderWidth: 2,
        },
        {
          label: 'Min',
          data: [
            summary.statistics.flowrate.min,
            summary.statistics.pressure.min,
            summary.statistics.temperature.min,
          ],
          backgroundColor: chartColors.colors[1],
          borderColor: chartColors.borderColors[1],
          borderWidth: 2,
        },
        {
          label: 'Max',
          data: [
            summary.statistics.flowrate.max,
            summary.statistics.pressure.max,
            summary.statistics.temperature.max,
          ],
          backgroundColor: chartColors.colors[2],
          borderColor: chartColors.borderColors[2],
          borderWidth: 2,
        },
      ],
    }
    : null;

  return (
    <div className="min-h-screen bg-background">
      <NavBar />

      <div className="pt-28 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <Upload_CSV onUploadSuccess={fetchDatasets} />
        
        {/* Dataset Selection */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Select Dataset</CardTitle>
            <CardDescription>Choose a dataset to view details and analytics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Select
                value={selectedDataset?.id.toString() || ""}
                onValueChange={(value) => fetchDatasetDetails(parseInt(value))}
                disabled={datasets.length === 0}
                
              >
                <SelectTrigger className="flex-1 h-[55px]">
                  <SelectValue placeholder={datasets.length === 0 ? "No datasets available" : "Select a dataset"} />
                </SelectTrigger>
                <SelectContent>
                  {datasets.map((dataset) => (
                    <SelectItem 
                      key={dataset.id} 
                      value={dataset.id.toString()}
                    >
                      <div className="flex flex-col">
                        <span className="font-medium">{dataset.name}</span>
                        <span className="text-xs text-muted-foreground">
                          {new Date(dataset.uploaded_at).toLocaleString()} • {dataset.total_count} items
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button
                variant="outline"
                size="icon"
                onClick={() => selectedDataset && handleDelete(selectedDataset.id)}
                disabled={!selectedDataset}
                title="Delete selected dataset"
              >
                <Trash2 className="h-4 w-4 text-destructive" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {loading && <p className="text-center">Loading...</p>}

        {selectedDataset && summary && !loading && (
          <>
            {/* Summary Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">Total Equipment</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{summary.total_count}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">Avg Flowrate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{summary.statistics.flowrate.avg.toFixed(2)}</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium">Avg Temperature</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">{summary.statistics.temperature.avg.toFixed(2)}°</div>
                </CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <Card>
                <CardHeader>
                  <CardTitle>Equipment Type Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  {typeDistributionData && (
                    <Doughnut
                      key={`doughnut-${theme}`}
                      data={typeDistributionData}
                      options={getDoughnutOptions(theme)}
                    />
                  )}
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Parameter Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                  {parametersData && (
                    <Bar
                      key={`bar-${theme}`}
                      data={parametersData}
                      options={getBarOptions(theme)}
                    />
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Equipment Table */}
            <Card className="mb-6">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Equipment Details</CardTitle>
                  <CardDescription>Showing {selectedDataset.equipment.length} items</CardDescription>
                </div>
                <Button onClick={handleDownloadPDF}>
                  <Download className="h-4 w-4 mr-2" />
                  Download PDF
                </Button>
              </CardHeader>
              <CardContent>
                <EquipmentDataTable columns={columns} data={selectedDataset.equipment} />
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
}
