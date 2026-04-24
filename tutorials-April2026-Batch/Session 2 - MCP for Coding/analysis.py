import pandas as pd
import matplotlib.pyplot as plt

def analyze_sales(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Convert 'Date' to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate revenue per transaction
    df['Revenue'] = df['Quantity'] * df['Price']
    
    # Set Date as index for easy resampling
    df.set_index('Date', inplace=True)
    
    # Calculate monthly revenue
    monthly_revenue = df['Revenue'].resample('ME').sum()
    
    # Print the monthly revenue
    print("Monthly Revenue Summary:")
    print(monthly_revenue)
    
    # Create a chart
    plt.figure(figsize=(10, 6))
    monthly_revenue.plot(kind='line', marker='o', color='teal', linewidth=2)
    
    plt.title('Monthly Sales Revenue (2025)', fontsize=14, pad=15)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Revenue ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the chart
    output_image = 'monthly_revenue_chart.png'
    plt.savefig(output_image)
    print(f"\nChart saved as {output_image}")
    
    plt.show()

if __name__ == "__main__":
    analyze_sales('sales.csv')
