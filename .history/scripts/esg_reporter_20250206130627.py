import pandas as pd

def generate_report(input_file='../data/energy_data.csv'):
    """
    Generate an ESG compliance report.
    """
    df = pd.read_csv(input_file)
    total_power = df['total_power'].sum()
    average_power = df['total_power'].mean()

    report = {
        "Total Energy Consumption (W)": total_power,
        "Average Power Usage (W)": average_power,
        "Compliance Recommendation": "Reduce idle power consumption."
    }

    print("=== ESG Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    generate_report()
