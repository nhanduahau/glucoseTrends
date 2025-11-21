# Glucose Trends Analyzer

A professional glucose data analysis tool that reads CSV files and generates comprehensive reports with 7-day trend charts and daily statistics.

## Features

- 📊 **7-Day Trend Analysis**: Displays hourly average glucose levels with smooth trend lines
- 📈 **Daily Statistics**: Summarizes min, max, and average values for each day
- 🎯 **Target Zones**: Clear visualization of low, target, and high glucose ranges
- 📉 **mmol/L Units**: Automatic conversion from mg/dL to mmol/L
- 🖼️ **High-Quality Reports**: Exports professional charts (PNG, 150 DPI)

## Requirements

- Python 3.7+
- Required libraries:
  - pandas
  - matplotlib

## Installation

1. Clone the repository or download the source code:

```bash
git clone https://github.com/nhanduahau/glucoseTrends.git
cd glucoseTrends
```

2. Install dependencies:

```bash
pip install pandas matplotlib
```

## Usage

### Data Preparation

Place your glucose CSV file in the same directory as `glucoseTrends.py`. The CSV file should have this format:

```csv
Time of Glucose Reading [T=(local time) +/- (time zone offset)], Measurement(mg/dL)
2025-11-06T01:36:00-06:00,164
2025-11-06T01:41:00-06:00,187
...
```

**Note**: The script will automatically detect the first `.csv` file in the directory.

### Running the Script

```bash
python glucoseTrends.py
```

### Output

The script generates an image file named:

```
Glucose_Report_DD-MM-YYYY_to_DD-MM-YYYY.png
```

The report contains 2 charts:

1. **7-Day Glucose Trends (Hourly Average)**

   - Hourly average trend line
   - Color-coded zones: Low (< 3.9 mmol/L), Target (3.9-10.0), High (> 10.0)
   - Weekly average line (purple dashed)

2. **Daily Summary**
   - Max (▲ red), Min (▼ blue), Average (● green) values per day
   - Daily range bars showing min-max variation

## Project Structure

```
glucoseTrends/
├── glucoseTrends.py           # Main script
├── fake_glucose_2weeks.csv    # Sample data (2 weeks)
└── README.md                  # This document
```

## Example

Run with sample data:

```bash
python glucoseTrends.py
```

Output:

```
--> Processing file: fake_glucose_2weeks.csv
Weekly Average Calculated: 6.85 mmol/L
--> Report generated successfully: Glucose_Report_14-11-2025_to_20-11-2025.png
```

## How It Works

1. **Find CSV File**: Automatically detects CSV file in current directory
2. **Data Processing**:
   - Parses time and measurement columns
   - Converts mg/dL → mmol/L (÷ 18.0)
   - Filters last 7 days based on data timestamps
3. **Calculate Statistics**:
   - Hourly averages (for smooth trend line)
   - Weekly average
   - Daily min/max/mean
4. **Generate Charts**: Creates 2-panel visualization with matplotlib and exports to PNG

## Customization

### Change Analysis Period

In `glucoseTrends.py`, line 39:

```python
start_date = last_date - pd.Timedelta(days=6)  # Change number of days here
```

### Adjust Target Glucose Ranges

Lines 62-64:

```python
ax1.axhspan(0, 3.9, ...)      # Low zone
ax1.axhspan(3.9, 10.0, ...)   # Target zone
ax1.axhspan(10.0, 20.0, ...)  # High zone
```

### Modify Export Quality

Line 135:

```python
plt.savefig(output_filename, dpi=150)  # Increase DPI for higher quality
```

## Troubleshooting

- **"No CSV file found"**: Ensure a `.csv` file exists in the directory
- **"Required columns not found"**: Verify CSV has `Time` and `Measurement` columns
- **"No data found for the analysis period"**: CSV file may not contain sufficient 7-day data

## Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is released under the MIT License.

## Author

**nhanduahau**

- GitHub: [@nhanduahau](https://github.com/nhanduahau)

## Notes

- Data in `fake_glucose_2weeks.csv` is for demonstration purposes only
- Standard unit used: mmol/L (international medical standard)
- Target glucose ranges based on standard medical guidelines (may vary per individual)
