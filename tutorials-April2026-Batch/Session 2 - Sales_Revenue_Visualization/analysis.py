import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration & Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'sales.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'revenue_chart.png')

def run_sales_analysis():
    """
    Reads sales data, performs monthly aggregation, and generates a premium visualization.
    """
    print("Starting Analysis...")
    print(f"Loading data from: {CSV_PATH}")

    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found!")
        return

    # 1. Load Data
    try:
        df = pd.read_csv(CSV_PATH)
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 2. Process Monthly Revenue
    # Set Date as index and resample by Month End ('ME' for Pandas 3.0+)
    df.set_index('Date', inplace=True)
    monthly_revenue = df['Amount'].resample('ME').sum()

    print("\nMonthly Revenue Summary:")
    print(monthly_revenue)

    # 3. Create Premium Visualization
    plt.style.use('seaborn-v0_8-muted')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

    # Plot data
    bars = ax.bar(
        [d.strftime('%b %Y') for d in monthly_revenue.index], 
        monthly_revenue.values,
        color='#4A90E2',
        edgecolor='#2C3E50',
        linewidth=1,
        alpha=0.8,
        width=0.6
    )

    # Add data labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2., 
            height + 20,
            f'${int(height):,}',
            ha='center', va='bottom', 
            fontsize=10, fontweight='bold', color='#2C3E50'
        )

    # Aesthetics
    ax.set_title('Monthly Sales Revenue Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12, labelpad=10)
    ax.set_ylabel('Total Revenue (USD)', fontsize=12, labelpad=10)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=.3)

    plt.tight_layout()

    # 4. Save and Finish
    plt.savefig(OUTPUT_PATH, bbox_inches='tight')
    print("\nAnalysis Complete!")
    print(f"Chart saved successfully to: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_sales_analysis()
