from codecarbon import EmissionsTracker
import pandas as pd

def calculate_emissions(input_file='../data/energy_data.csv'):
    """
    Calculate carbon emissions using CodeCarbon and energy data.
    """
    tracker = EmissionsTracker()
    tracker.start()

    data = pd.read_csv(input_file)
    total_power = data['total_power'].sum()  # Total power usage in Watts
    print(f"Total Power Consumption: {total_power:.2f} W")

    tracker.stop()
    emissions = tracker.final_emissions
    print(f"Estimated Carbon Emissions: {emissions:.4f} kg CO2")

if __name__ == "__main__":
    calculate_emissions()
