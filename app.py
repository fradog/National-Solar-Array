# -*- coding: utf-8 -*-
"""
Created on Tues Oct 28 15:03:29 2025

@author: dhfra
"""

# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from solar_model import target_total_energy, calculate_bond_principal, calculate_cash_flows, calculate_funding_mix, calculate_metrics

st.title("National Solar Array Bond Initiative")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "Welcome to my National Solar Array (with battery storage) financial simulation. \
         It's purpose is to illustrate that such a massive effort to achieve Net Zero in the US by around 2035-2037 (depending on how soon we can start), \
             has a significant positive financial impact with no one left behind. The premise is that the array is part of a nationalized grid project and the energy produced is \
                 consistent with national security goals. As such it is funded by either a portion of our national budget or by a Bond initiative, or a \
                     combination of both. Another key premise is that the energy is sold to users at the current national average price for electricity.\
                         At this price this simulation shows how the revenues generated over the lifetime of the Array are indeed massive and exceed most \
                             competitive investment opportunities in any arena. See for yourself, play with the inputs and observe their effects. Enjoy \
                                 the realization that we can actually solve the Climate Crisis and enjoy not only an improvement in our children's futures \
                                     but become financially secure and energy independent."
                                     "</span>",
                                unsafe_allow_html=True)

# Define default inputs
default_inputs = {
    'project_lifespan': 30,
    'initial_capacity': 230 * 10**6,  # kWp
    'target_capacity': 5498 * 10**6,  # kWp
    'capacity_factor': 0.2700,
    'revenue_per_kwh': 0.16,
    'avoided_fuel_per_kwh': 0.03,
    'efficiency_downgrade': 44.7 / 74.7, #from my spreadsheet evaluation (quads) of 2023 end use sector energy consumption
    'capital_cost_per_kwp': 1.73 * 10**3,
    'om_rate': 0.01,
    'grid_maintenance': 50 * 10**9,
    'discount_rate': 0.04,
    'degradation_rate': 0.007,
    'reinvestment_percentage': 0.5,
    'investment_return_rate': 0.03,
    'bond_interest_rate': 0.025,
    'bond_term': 10,
    'dividend_percentage': 0.5,
    'individual_investment': 10000,
    'us_adult_population': 258 * 10**6,
    'participation_rate_low': 0.05,
    'participation_rate_mid': 0.10,
    'participation_rate_high': 0.15,
    'carbon_tax_rate': 100,
    'us_emissions_tons': 4.7 * 10**9,
    'carbon_tax_effective_rate': 0.75,
    'displaceable_proportion': 1.0,
    'panel_rating': 700 / 2.57,
    'coverage_ratio': 0.4
}

# Define labels with units
input_labels = {
    'project_lifespan': 'Project Lifespan (years)',
    'initial_capacity': 'Initial Capacity (kWp)',
    'target_capacity': 'Target Capacity (kWp)',
    'capacity_factor': 'Capacity Factor',
    'revenue_per_kwh': 'Revenue per kWh ($/kWh)',
    'avoided_fuel_per_kwh': 'Avoided Fuel Cost per kWh ($/kWh)',
    'efficiency_downgrade': 'Fossil Fuel Combustion Efficiency downgrade',
    'capital_cost_per_kwp': 'Capital Cost per kWp ($/kWp)',
    'om_rate': 'O&M Rate',
    'grid_maintenance': 'Grid Maintenance ($)',
    'discount_rate': 'Discount Rate',
    'degradation_rate': 'Degradation Rate',
    'reinvestment_percentage': 'Reinvestment Percentage',
    'investment_return_rate': 'Investment Return Rate',
    'bond_interest_rate': 'Bond Interest Rate',
    'bond_term': 'Bond Term (years)',
    'dividend_percentage': 'Dividend Percentage',
    'individual_investment': 'Individual Investment ($)',
    'us_adult_population': 'US Adult Population (M)',
    'participation_rate_low': 'Participation Rate Low',
    'participation_rate_mid': 'Participation Rate Mid',
    'participation_rate_high': 'Participation Rate High',
    'carbon_tax_rate': 'Carbon Tax Rate ($/ton)',
    'us_emissions_tons': 'US Emissions (tons)',
    'carbon_tax_effective_rate': 'Carbon Tax Effective Rate',
    'displaceable_proportion': 'Displaceable Proportion',
    'panel_rating': 'Panel Rating (W/m^2)',
    'coverage_ratio': 'Coverage Ratio'
}

# Sidebar for inputs
st.sidebar.header("Input Parameters")
inputs = {}

for param, value in default_inputs.items():
    label = input_labels.get(param, param.replace('_', ' ').title())

    if isinstance(value, int):
        # Determine step size based on parameter type
        step = (
            1 if param in ['project_lifespan', 'bond_term', 'carbon_tax_rate']
            else 1000 if 'investment' in param
            else 10**6 if 'capacity' in param or 'population' in param
            else 10**9
        )

        # Display formatted value with commas in the text input
        formatted_value = f"{value:,}"
        user_input = st.sidebar.text_input(label, formatted_value)

        # Remove commas and convert to int safely
        try:
            cleaned_value = int(user_input.replace(',', '').strip())
            inputs[param] = cleaned_value
        except ValueError:
            # Fall back to the default if input is invalid
            st.sidebar.warning(f"Invalid value for {label}. Using default: {value:,}")
            inputs[param] = value

    elif isinstance(value, float):
        # Define step and range based on parameter type
        step = (
            0.0001 if param in ['capacity_factor', 'degradation_rate', 'om_rate']
            else 0.001
        )
        max_val = (
            value * 1.5 if param in ['capacity_factor']
            else value * 2 if param not in ['carbon_tax_effective_rate', 'displaceable_proportion']
            else 1.0
        )
        format_str = (
            "%.4f" if param in ['capacity_factor', 'degradation_rate', 'om_rate']
            else "%.3f"
        )

        inputs[param] = st.sidebar.slider(
            label,
            min_value=0.0 if param not in ['capacity_factor'] else 0.15,
            max_value=max_val,
            value=value,
            step=step,
            format=format_str
        )

# Calculate results
annual_energy_goal, required_area = target_total_energy(inputs)
bond_principal, carbon_tax_10yr = calculate_bond_principal(inputs)
cash_flows_df = calculate_cash_flows(inputs, bond_principal, project_lifespan=inputs['project_lifespan'])
funding_mix_df = calculate_funding_mix(inputs, bond_principal)
metrics = calculate_metrics(inputs, cash_flows_df, bond_principal, project_lifespan=inputs['project_lifespan'])

# Display results
st.header("System Size")
st.write("System Target Energy Production: 13,100 teraWatthours")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "In 2023 end use sectors in the U.S. consumed 74.7 quads (21,877 tWh) of energy in the forms of heat and electricity. After the efficiency improvement of \
         direct transmission from solar PV conversion, I estimate that to do the same work at the end user would require 44.7 quads (13,100 tWh) of electrical energy."
         "</span>",
    unsafe_allow_html=True)
st.write(f"Annual Energy: {annual_energy_goal:,.0f} teraWatthours")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "Note: if Annual Energy is different than target energy, adjust capacity factor or Target Capacity"
         "</span>",
    unsafe_allow_html=True)
st.write(f"Area Required: {required_area:,.0f} Sq.Mi. with coverage ratio of {inputs['coverage_ratio']:.2f}")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "Note: typical coverage ratio for commercial bifacial single axis tracking panel installation is 0.40 to prevent self shading losses.\
         Increasing this will have a detrimental effect on Capacity Factor. I estimate a change in coverage ratio from 0.40 to 0.50 to reduce \
             capcity factor by about 3.7%."
         "</span>",
    unsafe_allow_html=True)

st.header("Bond Principal")
st.write(f"Calculated Bond Principal: ${bond_principal / 10**9:.2f}B")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "This prinsipal is essentially how much we would need to build the array and its associated storage and grid upgrades and maintenance.\
         It is roughly on the order of magnitude of one year's of defense budget. Investors in this bond will see compound annual growth rates \
         competitive with other much higher risk investments. \
         This simulation divides the net cash flow in into a mix of an amount paid out to investors as dividends to bond holders \
         and an amount paid out for other purposes. Those could be to pay unforeseen bills, for reinvestment, or any other creative\
         purpose in the interest of the nation."
         "</span>",
    unsafe_allow_html=True)
st.write(f"Total Carbon Tax Revenue (10 years): ${carbon_tax_10yr / 10**9:.2f}B")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "Note: Carbon tax revenue applied as cash flow to reduce bond principal."
         "</span>",
    unsafe_allow_html=True)

st.header("Financial Metrics")
st.dataframe(cash_flows_df.round(2))

st.header("Funding Mix")
st.write("<span style='font-size:0.85rem; font-style:italic;'>"
         "Shows funding sources for the reduced bond principal (after carbon tax revenue)."
         "</span>",
    unsafe_allow_html=True)
st.dataframe(funding_mix_df.round(2))

#st.header("Key Metrics")
#metrics_df = pd.DataFrame([metrics]).round(2)
#st.dataframe(metrics_df)
st.header("Key Metrics")

# Create dataframe and round values
metrics_df = pd.DataFrame([metrics]).round(2)

# Define your last column exactly as it appears
last_col = "Individual Bond Investor Ending Balance ($)"

# Build formatting dictionary for all numeric columns
format_dict = {
    col: "{:,.0f}" if col == last_col else "{:,.2f}"
    for col in metrics_df.select_dtypes(include="number").columns
}

# Build styled DataFrame
styled = (
    metrics_df.style
    .format(format_dict)
    .set_properties(**{"text-align": "right"}, subset=[last_col])
    .set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("white-space", "normal"),
                    ("word-wrap", "break-word"),
                    ("max-width", "150px"),
                    ("text-align", "center"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("white-space", "normal"),
                    ("text-align", "right"),
                ],
            },
        ]
    )
    # <<< NEW LINE – hides the index column >>>
    .hide(axis="index")          # Streamlit ≥ 1.27
)

# Render styled DataFrame as HTML (fully respects CSS)
st.write(
    f'<div style="overflow-x:auto;">{styled.to_html()}</div>',
    unsafe_allow_html=True
)



# Plot 1: Financial Metrics
fig1 = px.line(cash_flows_df, x='Year', y=['Cash Flow Pre-Debt ($B)', 'Cash Flow Post-Debt ($B)', 'Total Costs ($B)', 'Total Inflows ($B)', 'Interest Payment ($B)', 'Principal Payment ($B)', 'Dividends ($B)', 'Amount Paid Out ($B)'],
               title="Financial Metrics Over Time")
st.plotly_chart(fig1)

# Plot 2: Balance Trends
fig2 = px.line(cash_flows_df, x='Year', y=['Reinvested Balance ($B)', 'Outstanding Principal ($B)'],
               title="Balance Trends")
st.plotly_chart(fig2)

# Plot 3: Emissions Reduction
emissions_data = []
displaceable_emissions = inputs['us_emissions_tons'] * inputs['displaceable_proportion']
non_displaceable_emissions = inputs['us_emissions_tons'] * (1 - inputs['displaceable_proportion'])
for t in range(10):
    remaining_emissions = displaceable_emissions * (1 - t / 10) + non_displaceable_emissions
    emissions_data.append({
        'Year': t + 1,
        'Total Emissions (B tons)': remaining_emissions / 10**9
    })
emissions_df = pd.DataFrame(emissions_data)
fig3 = px.line(emissions_df, x='Year', y=['Total Emissions (B tons)'], 
               title='CO2 Emissions Reduction Over Time')
st.plotly_chart(fig3)



