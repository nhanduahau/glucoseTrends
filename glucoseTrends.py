import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import glob
import os

def generate_glucose_report():
    """
    Analyzes glucose data from a CSV file, calculates statistics,
    and generates a professional report chart.
    """
    # --- 1. FIND CSV FILE ---
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("Error: No CSV file found in the current directory.")
        return
    file_path = csv_files[0]
    print(f"--> Processing file: {file_path}")

    try:
        # --- 2. DATA PROCESSING ---
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        
        # Identify columns dynamically
        time_col = next((c for c in df.columns if 'Time' in c), None)
        measure_col = next((c for c in df.columns if 'Measurement' in c), None)

        if not time_col or not measure_col:
            print("Error: Required columns (Time/Measurement) not found.")
            return

        # Convert Time & Sort
        df[time_col] = pd.to_datetime(df[time_col])
        df = df.sort_values(by=time_col)

        # Convert measurement to numeric, replacing invalid values with NaN
        df[measure_col] = pd.to_numeric(df[measure_col], errors='coerce')
        
        # Remove rows with invalid measurements
        original_count = len(df)
        df = df.dropna(subset=[measure_col])
        removed_count = original_count - len(df)
        if removed_count > 0:
            print(f"--> Removed {removed_count} invalid measurement(s) (e.g., 'Out of range')")

        # Convert Unit (mg/dL -> mmol/L)
        df['Glucose_mmol'] = df[measure_col] / 18.0

        # Filter Last 7 Days (Based on data, not system time)
        last_date = df[time_col].max()
        start_date = last_date - pd.Timedelta(days=6)
        
        mask = (df[time_col] >= start_date) & (df[time_col] <= last_date)
        df_week = df.loc[mask].copy()

        if df_week.empty:
            print("No data found for the analysis period.")
            return

        # --- 3. CALCULATE STATISTICS ---
        
        # A. Hourly Average (For Smoother Trend Line)
        df_hourly = df_week.set_index(time_col).resample('h')['Glucose_mmol'].mean().reset_index().dropna()

        # B. Weekly Average (Based on Raw Data)
        weekly_avg = df_week['Glucose_mmol'].mean()

        # C. Daily Summary (Based on Raw Data)
        df_week['Date_Only'] = df_week[time_col].dt.date
        daily_stats = df_week.groupby('Date_Only')['Glucose_mmol'].agg(['max', 'min', 'mean']).reset_index()

        print(f"Weekly Average Calculated: {weekly_avg:.2f} mmol/L")

        # --- 4. PLOTTING REPORT ---
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

        # === CHART 1: 7-DAY TRENDS (HOURLY AVG) ===
        # Define Target Zones
        ax1.axhspan(0, 3.9, color='#FFCCCC', alpha=0.5, label='Low (< 3.9)')
        ax1.axhspan(3.9, 10.0, color='#E8F8F5', alpha=1.0, label='Target (3.9 - 10.0)')
        ax1.axhspan(10.0, 20.0, color='#FCF3CF', alpha=0.5, label='High (> 10.0)')

        # Plot Trend Line (Smooth curve)
        ax1.plot(df_hourly[time_col], df_hourly['Glucose_mmol'], 
                 color='#2980B9', linewidth=3, linestyle='-', label='Hourly Avg Glucose')
        
        # Plot Weekly Average Line
        ax1.axhline(y=weekly_avg, color='purple', linestyle='--', linewidth=2)
        
        # Label Weekly Average directly on the line
        ax1.text(df_week[time_col].max(), weekly_avg, f'  {weekly_avg:.2f}', 
                 va='center', ha='left', color='purple', fontweight='bold', fontsize=12, 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.2'))

        # Chart Settings
        ax1.set_ylim(3, 11.5)
        ax1.set_title(f'7-Day Glucose Trends (Hourly Average)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Glucose (mmol/L)')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m\n%H:%M'))
        ax1.legend(loc='upper left', frameon=True)
        ax1.grid(True, alpha=0.5)

        # === CHART 2: DAILY SUMMARY (RAW DATA) ===
        dates = daily_stats['Date_Only']
        
        # Plot Range Bars (Min to Max)
        ax2.vlines(dates, daily_stats['min'], daily_stats['max'], color='gray', alpha=0.5, linewidth=3)
        
        # Plot Markers
        ax2.scatter(dates, daily_stats['max'], color='red', marker='^', s=100, label='Max', zorder=5)
        ax2.scatter(dates, daily_stats['min'], color='blue', marker='v', s=100, label='Min', zorder=5)
        ax2.scatter(dates, daily_stats['mean'], color='green', marker='o', s=120, label='Daily Avg', zorder=5)

        # Annotate Values
        for idx, row in daily_stats.iterrows():
            # Max
            ax2.annotate(f"{row['max']:.1f}", (row['Date_Only'], row['max']), 
                         xytext=(0, 8), textcoords='offset points', ha='center', 
                         fontsize=9, color='red', fontweight='bold')
            # Min
            ax2.annotate(f"{row['min']:.1f}", (row['Date_Only'], row['min']), 
                         xytext=(0, -12), textcoords='offset points', ha='center', 
                         fontsize=9, color='blue', fontweight='bold')
            # Average
            ax2.annotate(f"{row['mean']:.1f}", (row['Date_Only'], row['mean']), 
                         xytext=(12, 0), textcoords='offset points', ha='left', va='center', 
                         fontsize=10, color='green', fontweight='bold')

        # Chart Settings
        ax2.set_ylim(2, 12)
        ax2.set_title('Daily Summary: Min, Max, and Average', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Glucose (mmol/L)')
        ax2.set_xticks(dates)
        ax2.set_xticklabels([d.strftime('%d/%m') for d in dates])
        
        # Legend layout
        handles, labels = ax2.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax2.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)
        ax2.grid(True, alpha=0.5)

        # --- 5. EXPORT REPORT ---
        plt.tight_layout()
        
        # Generate Filename
        s_str = df_week[time_col].min().strftime('%d-%m-%Y')
        e_str = df_week[time_col].max().strftime('%d-%m-%Y')
        output_filename = f"Glucose_Report_{s_str}_to_{e_str}.png"
        
        plt.savefig(output_filename, dpi=150)
        print(f"--> Report generated successfully: {output_filename}")

    except Exception as e:
        print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    generate_glucose_report()