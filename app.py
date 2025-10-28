# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 18:13:00 2025

@author: dhfra
"""

# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from solar_model import calculate_bond_principal, calculate_cash_flows, calculate_funding_mix, calculate_metrics

st.title("National Solar Array Bond Initiative")

# Define default inputs
default_inputs = {
    'project_lifespan': 30,
    'initial_capacity': 230 * 10**6,  # kWp
    'target_capacity': 5498 * 10**6,  # kWp
    'capacity_factor': 0.27,
    'revenue_per_kwh': 0.16,
    'avoided_fuel_per_kwh': 0.03,
    'efficiency_downgrade': 44 / 77,
    'capital_cost_per_kwp': 1.73 * 10**3,
    'om_rate': 0.01,
    'grid_maintenance': 50 * 10**9,
    'discount_rate': 0.04,
    'degradation_rate': 0.007,
    'reinvestment_percentage': 0.5,
    'investment_return_rate': 0.03,
    'bond_interest_rate': 0.025,
    'bond_issuance_flat_fee': 0.857 * 10**9,
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
    'displaceable_proportion': 1.0
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
    'grid_maintenance': 'Grid Maintenance ($B)',
    'discount_rate': 'Discount Rate',
    'degradation_rate': 'Degradation Rate',
    'reinvestment_percentage': 'Reinvestment Percentage',
    'investment_return_rate': 'Investment Return Rate',
    'bond_interest_rate': 'Bond Interest Rate',
    'bond_issuance_flat_fee': 'Bond Issuance Flat Fee ($B)',
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
    'displaceable_proportion': 'Displaceable Proportion'
}

# Sidebar for inputs
st.sidebar.header("Input Parameters")
inputs = {}
for param, value in default_inputs.items():
    label = input_labels.get(param, param.replace('_', ' ').title())
    if isinstance(value, int):
        step = 1 if param in ['project_lifespan', 'bond_term', 'carbon_tax_rate'] else 1000 if 'investment' in param else 10**6 if 'capacity' in param or 'population' in param else 10**9
        inputs[param] = st.sidebar.number_input(label, min_value=0, value=value, step=step)
    elif isinstance(value, float):
        step = 0.0001 if param in ['degradation_rate', 'om_rate'] else 0.001 if param == 'capacity_factor' else 0.01
        max_val = value * 2 if param not in ['capacity_factor', 'carbon_tax_effective_rate', 'displaceable_proportion'] else 1.0
        format_str = "%.4f" if param in ['degradation_rate', 'om_rate'] else "%.2f"
        inputs[param] = st.sidebar.slider(label, min_value=0.0, max_value=max_val, value=value, step=step, format=format_str)

# Calculate results
bond_principal, carbon_tax_10yr = calculate_bond_principal(inputs)
cash_flows_df = calculate_cash_flows(inputs, bond_principal, project_lifespan=inputs['project_lifespan'])
funding_mix_df = calculate_funding_mix(inputs, bond_principal)
metrics = calculate_metrics(inputs, cash_flows_df, bond_principal, project_lifespan=inputs['project_lifespan'])

# Display results
st.header("Bond Principal")
st.write(f"Calculated Bond Principal: ${bond_principal / 10**9:.2f}B")
st.write(f"Total Carbon Tax Revenue (10 years): ${carbon_tax_10yr / 10**9:.2f}B")
st.write("Carbon tax revenue applied as cash flow to reduce bond principal.")

st.header("Financial Metrics")
st.dataframe(cash_flows_df.round(2))

st.header("Funding Mix")
st.write("Shows funding sources for the reduced bond principal (after carbon tax revenue).")
st.dataframe(funding_mix_df.round(2))

st.header("Key Metrics")
metrics_df = pd.DataFrame([metrics]).round(2)
st.dataframe(metrics_df)

# Plot 1: Financial Metrics
fig1 = px.line(cash_flows_df, x='Year', y=['Cash Flow Pre-Debt ($B)', 'Total Costs ($B)', 'Total Inflows ($B)', 'Interest Payment ($B)', 'Principal Payment ($B)', 'Dividends ($B)', 'Amount Paid Out ($B)'],
               title="Financial Metrics Over Time")
st.plotly_chart(fig1)

# Plot 2: Balance Trends
fig2 = px.line(cash_flows_df, x='Year', y=['Reinvested Balance ($B)', 'Outstanding Principal ($B)'],
               title="Balance Trends")
st.plotly_chart(fig2)
