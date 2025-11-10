# Desktop Application - PyQt5

Native desktop application for the Chemical Equipment Visualizer.

## Features

- 🖥️ Native desktop interface
- 📊 Embedded Matplotlib charts
- 📁 Native file dialogs
- 🔐 JWT authentication
- 📋 Data table with equipment details
- 📄 PDF report download

## Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
```

2. **Activate Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
python main.py
```

## Project Structure

```
desktop-app/
├── main.py           # Application entry point
├── auth_window.py    # Login/Register window
├── main_window.py    # Main application window
├── api_client.py     # API communication
└── requirements.txt  # Python dependencies
```

## Requirements

- Python 3.8+
- PyQt5 5.15+
- requests
- matplotlib
- pandas

## Usage

### First Time Setup

1. Ensure the backend server is running on `http://localhost:8000`
2. Run `python main.py`
3. Register a new account or login
4. Start uploading and analyzing data

### Main Features

#### Upload CSV
1. Click "Upload CSV" button
2. Select a CSV file from your computer
3. Wait for upload confirmation
4. Dataset will appear in the dropdown

#### View Data
1. Select a dataset from the dropdown
2. View summary statistics
3. Explore charts
4. Browse equipment table

#### Download PDF
1. Select a dataset
2. Click "Download PDF"
3. Choose save location
4. PDF report will be generated

## API Configuration

Update the API URL in `api_client.py`:

```python
API_URL = 'http://localhost:8000/api'
```

## Building Executable

### Windows

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="ChemicalEquipmentVisualizer" main.py
```

Executable will be in `dist/` folder.

### Additional Files

If you need to include additional files:

```bash
pyinstaller --onefile --windowed --add-data "icon.ico;." main.py
```

## Styling

The application uses a custom stylesheet defined in the window classes. Colors and styles can be modified in:

- `auth_window.py` - Login/Register window styling
- `main_window.py` - Main window styling

### Color Scheme

Current colors match the web application:
- Primary: `#3b82f6` (Blue)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Orange)
- Danger: `#ef4444` (Red)
- Background: `#f0f4f8` (Light Gray)

## Charts

### Type Distribution Chart
- Pie chart showing equipment type distribution
- Automatically colored
- Percentage labels

### Parameters Chart
- Grouped bar chart
- Shows Average, Min, Max for each parameter
- Color-coded bars

## Troubleshooting

### PyQt5 Installation Issues

**Windows:**
```bash
pip install PyQt5-sip
pip install PyQt5
```

**Linux:**
```bash
sudo apt-get install python3-pyqt5
pip install PyQt5
```

**Mac:**
```bash
brew install pyqt5
pip install PyQt5
```

### Matplotlib Backend Issues

If charts don't display:
```python
import matplotlib
matplotlib.use('Qt5Agg')
```

### API Connection Errors

- Verify backend is running
- Check firewall settings
- Ensure correct API URL
- Check network connectivity

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

## Development

### Adding New Features

1. **New Window:**
   - Create new class inheriting from `QWidget` or `QMainWindow`
   - Define UI in `init_ui()` method
   - Connect signals to slots

2. **New API Endpoint:**
   - Add method to `APIClient` class in `api_client.py`
   - Handle authentication headers
   - Add error handling

3. **New Chart:**
   - Create `FigureCanvas` widget
   - Add to layout
   - Update with data in separate method

### Code Structure

```python
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Setup UI components
        pass
    
    def handle_action(self):
        # Handle user actions
        pass
```

## Testing

### Manual Testing Checklist

- [ ] Login with valid credentials
- [ ] Register new account
- [ ] Upload CSV file
- [ ] View dataset details
- [ ] Switch between datasets
- [ ] Download PDF report
- [ ] Check error handling

### Test Data

Use the sample CSV file in `../sample_data/sample_equipment_data.csv`

## Performance

- Lazy loading of datasets
- Efficient table updates
- Chart caching (can be implemented)
- Background API calls (can be implemented with QThread)

## Packaging

### Create Installer (Windows)

Using Inno Setup:

1. Install Inno Setup
2. Create script file:

```iss
[Setup]
AppName=Chemical Equipment Visualizer
AppVersion=1.0
DefaultDirName={pf}\ChemicalEquipmentVisualizer
DefaultGroupName=Chemical Equipment Visualizer
OutputDir=installer
OutputBaseFilename=ChemicalEquipmentVisualizer_Setup

[Files]
Source: "dist\ChemicalEquipmentVisualizer.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Chemical Equipment Visualizer"; Filename: "{app}\ChemicalEquipmentVisualizer.exe"
```

3. Compile with Inno Setup

## Known Issues

- Large datasets (>1000 rows) may slow down table rendering
- PDF download requires backend to be accessible
- Charts may not render properly on high DPI displays (can be fixed with scaling)

## Future Enhancements

- [ ] Offline mode with local database
- [ ] Export to Excel
- [ ] Advanced filtering and sorting
- [ ] Data comparison between datasets
- [ ] Custom chart types
- [ ] Print functionality
- [ ] Auto-update feature

## Support

For issues or questions:
1. Check this README
2. Review error messages
3. Check backend logs
4. Verify API connectivity
