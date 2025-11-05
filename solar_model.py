
# -*- coding: utf-8 -*-
"""
Created on Tues Oct 28 14:12:00 2025

@author: dhfra
"""

# solar_model.py
import numpy as np
import numpy_financial as npf
import pandas as pd


def target_total_energy(inputs):
    capacity_factor = inputs['capacity_factor']
    target_capacity = inputs['target_capacity']
    panel_rating = inputs['panel_rating']
    coverage_ratio = inputs['coverage_ratio']
    
    annual_energy_goal = capacity_factor * 8760 * target_capacity / 10**9 # terawatthours
    area_required = target_capacity / (panel_rating / 1000) / coverage_ratio / 2.59e6 # area in sq.mi.

    return annual_energy_goal, area_required

def calculate_bond_principal(inputs, buildout_years=10):
    initial_capacity = inputs['initial_capacity']  # kWp
    target_capacity = inputs['target_capacity']  # kWp
    hours_per_year = inputs['capacity_factor'] * 8760
    capital_cost_per_kwp = inputs['capital_cost_per_kwp']
    om_rate = inputs['om_rate']
    grid_maintenance = inputs['grid_maintenance']
    revenue_per_kwh = inputs['revenue_per_kwh']
    avoided_fuel_per_kwh = inputs['avoided_fuel_per_kwh']
    degradation_rate = inputs['degradation_rate']
    us_emissions_tons = inputs['us_emissions_tons']
    carbon_tax_rate = inputs['carbon_tax_rate']
    carbon_tax_effective_rate = inputs['carbon_tax_effective_rate']
    displaceable_proportion = inputs['displaceable_proportion']
    efficiency_downgrade = inputs['efficiency_downgrade']
    
    # Validation
    if displaceable_proportion < 0 or displaceable_proportion > 1:
        raise ValueError("Displaceable proportion must be between 0 and 1")
    
    annual_addition = (target_capacity - initial_capacity) / buildout_years
    shortfall_sum = 0
    cumulative_capacity = initial_capacity
    effective_capacity = initial_capacity
    displaceable_emissions = us_emissions_tons * displaceable_proportion
    non_displaceable_emissions = us_emissions_tons * (1 - displaceable_proportion)
    carbon_tax_10yr = 0
    
    for t in range(buildout_years):
        planned_capacity = min(initial_capacity + annual_addition * t, target_capacity)
        target_energy_kwh = planned_capacity * hours_per_year
        effective_capacity *= (1 - degradation_rate)
        energy_kwh = effective_capacity * hours_per_year
        energy_shortfall = target_energy_kwh - energy_kwh
        additional_capacity = energy_shortfall / hours_per_year if energy_shortfall > 0 else 0
        total_new_capacity = annual_addition + additional_capacity
        cumulative_capacity += total_new_capacity
        effective_capacity += total_new_capacity
        capital_cost = total_new_capacity * capital_cost_per_kwp
        om_cost = cumulative_capacity * capital_cost_per_kwp * om_rate
        total_costs = capital_cost + om_cost + grid_maintenance
        revenue = energy_kwh * revenue_per_kwh
        avoided_fuel = energy_kwh / efficiency_downgrade * avoided_fuel_per_kwh
        remaining_emissions = displaceable_emissions * (1 - t / buildout_years) + non_displaceable_emissions
        annual_carbon_tax = carbon_tax_rate * remaining_emissions * carbon_tax_effective_rate
        carbon_tax_10yr += annual_carbon_tax
        total_inflows = revenue + avoided_fuel + annual_carbon_tax
        net_cash_flow = total_inflows - total_costs
        if net_cash_flow < 0:
            shortfall_sum += -net_cash_flow
    
    return shortfall_sum, carbon_tax_10yr

def calculate_cash_flows(inputs, bond_principal, project_lifespan=30):
    initial_capacity = inputs['initial_capacity']  # kWp
    target_capacity = inputs['target_capacity']  # kWp
    hours_per_year = inputs['capacity_factor'] * 8760
    revenue_per_kwh = inputs['revenue_per_kwh']
    avoided_fuel_per_kwh = inputs['avoided_fuel_per_kwh']
    capital_cost_per_kwp = inputs['capital_cost_per_kwp']
    om_rate = inputs['om_rate']
    grid_maintenance = inputs['grid_maintenance']
    degradation_rate = inputs['degradation_rate']
    reinvestment_percentage = inputs['reinvestment_percentage']
    investment_return_rate = inputs['investment_return_rate']
    bond_interest_rate = inputs['bond_interest_rate']
    dividend_percentage = inputs['dividend_percentage']
    bond_term = inputs['bond_term']
    individual_investment = inputs['individual_investment']
    efficiency_downgrade = inputs['efficiency_downgrade']
    
    annual_addition = (target_capacity - initial_capacity) / 10
    annual_debt_service = -npf.pmt(bond_interest_rate, bond_term, bond_principal) if bond_term > 0 else 0
    annual_debt_service_list = [annual_debt_service if t < bond_term else 0 for t in range(project_lifespan)]
    
    data = {
        'Year': list(range(1, project_lifespan + 1)),
        'New Capacity (MWp)': [],
        'Cash Flow Pre-Debt ($B)': [],
        'Total Costs ($B)': [],
        'Total Inflows ($B)': [],
        'Interest Payment ($B)': [],
        'Principal Payment ($B)': [],
        'Cash Flow Post-Debt ($B)': [],
        'Outstanding Principal ($B)': [],
        'Reinvested Balance ($B)': [],
        'Dividends ($B)': [],
        'Amount Paid Out ($B)': [],
        'Investor Interest ($)': [],
        'Investor Principal ($)': [],
        'Investor Dividends ($)': [],
        'Investor Total Cash Flow ($)': []
    }
    
    cumulative_capacity = initial_capacity
    effective_capacity = initial_capacity
    reinvested_balance = 0
    current_principal = bond_principal
    investor_share = individual_investment / bond_principal if bond_principal > 0 else 0
    
    for t in range(project_lifespan):
        planned_capacity = min(initial_capacity + annual_addition * t, target_capacity)
        target_energy_kwh = planned_capacity * hours_per_year
        effective_capacity *= (1 - degradation_rate)
        energy_kwh = effective_capacity * hours_per_year
        energy_shortfall = target_energy_kwh - energy_kwh
        additional_capacity = energy_shortfall / hours_per_year if energy_shortfall > 0 else 0
        planned_new_capacity = annual_addition if t < 10 else 0
        total_new_capacity = planned_new_capacity + additional_capacity
        cumulative_capacity += total_new_capacity
        effective_capacity += total_new_capacity
        revenue = energy_kwh * revenue_per_kwh
        avoided_fuel = energy_kwh / efficiency_downgrade * avoided_fuel_per_kwh
        total_annual_inflows = revenue + avoided_fuel
        capital_cost = total_new_capacity * capital_cost_per_kwp
        om_cost = cumulative_capacity * capital_cost_per_kwp * om_rate
        total_annual_costs = capital_cost + om_cost + grid_maintenance
        net_cash_flow_pre_debt = total_annual_inflows - total_annual_costs
        
        debt_service = annual_debt_service_list[t]
        interest_payment = current_principal * bond_interest_rate if t < bond_term else 0
        principal_payment = debt_service - interest_payment if t < bond_term else 0
        net_cash_flow_post_debt = net_cash_flow_pre_debt - debt_service
        current_principal = max(0, current_principal - principal_payment)
        
        reinvested_amount = max(net_cash_flow_post_debt, 0) * reinvestment_percentage
        original_paid_out = net_cash_flow_post_debt * (1 - reinvestment_percentage) if net_cash_flow_post_debt > 0 else net_cash_flow_post_debt
        dividend_amount = original_paid_out * dividend_percentage if original_paid_out > 0 else 0
        amount_paid_out_val = original_paid_out * (1 - dividend_percentage) if original_paid_out > 0 else original_paid_out
        reinvested_balance = reinvested_balance * (1 + investment_return_rate) + reinvested_amount
        
        investor_interest = interest_payment * investor_share
        investor_principal = principal_payment * investor_share
        investor_dividend = dividend_amount * investor_share
        investor_cash_flow = investor_interest + investor_principal + investor_dividend
        
        data['New Capacity (MWp)'].append(total_new_capacity / 10**6)
        data['Cash Flow Pre-Debt ($B)'].append(net_cash_flow_pre_debt / 10**9)
        data['Total Costs ($B)'].append(total_annual_costs / 10**9)
        data['Total Inflows ($B)'].append(total_annual_inflows / 10**9)
        data['Interest Payment ($B)'].append(interest_payment / 10**9)
        data['Principal Payment ($B)'].append(principal_payment / 10**9)
        data['Cash Flow Post-Debt ($B)'].append(net_cash_flow_post_debt / 10**9)
        data['Outstanding Principal ($B)'].append(current_principal / 10**9)
        data['Reinvested Balance ($B)'].append(reinvested_balance / 10**9)
        data['Dividends ($B)'].append(dividend_amount / 10**9)
        data['Amount Paid Out ($B)'].append(amount_paid_out_val / 10**9)
        data['Investor Interest ($)'].append(investor_interest)
        data['Investor Principal ($)'].append(investor_principal)
        data['Investor Dividends ($)'].append(investor_dividend)
        data['Investor Total Cash Flow ($)'].append(investor_cash_flow)
    
    return pd.DataFrame(data)
# ----------------------------------------------------------------------
# Add this function near the other helpers (anywhere in the file)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# LCOE CALCULATION – add this block to solar_model.py
# ----------------------------------------------------------------------
def calculate_lcoe(
    inputs: dict,
    cash_flows_df: pd.DataFrame,
    project_lifespan: int = 30,
    include_battery: bool = True,
    battery_duration_hr: float = 2.0,
) -> dict:
    """
    Compute Levelized Cost of Energy (LCOE) for the solar + optional battery system.
    
    Uses NREL-style methodology:
        LCOE = (PV of total costs) / (PV of total generation)
    
    Returns a dictionary with:
        - LCOE ($/MWh)
        - Total PV Costs ($B)
        - Total PV Energy (TWh)
        - Breakdown components (CAPEX, O&M, Grid, etc.)
    """
    # ------------------------------------------------------------------
    # 1. Pull key inputs
    # ------------------------------------------------------------------
    discount_rate = inputs['discount_rate']
    capital_cost_per_kwp = inputs['capital_cost_per_kwp']      # $/kWp AC (includes battery if flag=True)
    om_rate = inputs['om_rate']
    grid_maintenance = inputs['grid_maintenance']
    capacity_factor = inputs['capacity_factor']
    degradation_rate = inputs['degradation_rate']
    initial_capacity = inputs['initial_capacity'] / 1e3         # MW AC
    target_capacity = inputs['target_capacity'] / 1e3           # MW AC
    buildout_years = 10

    # ------------------------------------------------------------------
    # 2. Build year-by-year arrays (same logic you already use)
    # ------------------------------------------------------------------
    annual_addition_mw = (target_capacity - initial_capacity) / buildout_years
    hours_per_year = capacity_factor * 8760

    capex = np.zeros(project_lifespan)
    om_cost = np.zeros(project_lifespan)
    grid_cost = np.zeros(project_lifespan)
    energy_mwh = np.zeros(project_lifespan)

    cumulative_mw = initial_capacity
    effective_mw = initial_capacity

    for t in range(project_lifespan):
        # --- Capacity build-out ---
        planned_mw = min(initial_capacity + annual_addition_mw * min(t, buildout_years - 1), target_capacity)
        target_energy_mwh = planned_mw * hours_per_year

        # Degradation
        effective_mw *= (1 - degradation_rate)
        actual_energy_mwh = effective_mw * hours_per_year

        # Shortfall → extra capacity (same logic as in your cash flow)
        shortfall_mwh = target_energy_mwh - actual_energy_mwh
        extra_mw = shortfall_mwh / hours_per_year if shortfall_mwh > 0 else 0.0

        new_mw = (annual_addition_mw if t < buildout_years else 0.0) + extra_mw
        cumulative_mw += new_mw
        effective_mw += new_mw

        # --- Costs ---
        capex[t] = new_mw * 1e3 * capital_cost_per_kwp           # $ (kWp → W)
        om_cost[t] = cumulative_mw * 1e3 * capital_cost_per_kwp * om_rate
        grid_cost[t] = grid_maintenance

        # --- Generation ---
        energy_mwh[t] = effective_mw * hours_per_year

    total_costs = capex + om_cost + grid_cost

    # ------------------------------------------------------------------
    # 3. Discount to Present Value
    # ------------------------------------------------------------------
    years = np.arange(1, project_lifespan + 1)
    discount_factors = 1 / (1 + discount_rate) ** years

    pv_costs = np.sum(total_costs * discount_factors)
    pv_energy = np.sum(energy_mwh * discount_factors) / 1e6   # TWh

    # ------------------------------------------------------------------
    # 4. LCOE
    # ------------------------------------------------------------------
    lcoe = (pv_costs / 1e9) / pv_energy * 1e3   # $/MWh  (B$ / TWh → k$/MWh → $/MWh)

    # ------------------------------------------------------------------
    # 5. Optional: Split CAPEX into PV-only vs. Battery (for transparency)
    # ------------------------------------------------------------------
    if include_battery:
        # Use NREL 2024 ATB Advanced average 2025–2035 (2-hr system)
        # From earlier: PV ≈ $780/kW, Battery ≈ $353/kW → total $1,133/kW
        # We'll assume your `capital_cost_per_kwp` already includes both.
        # But we can estimate split:
        avg_pv_capex = 780   # $/kW AC (Advanced avg 2025–2035)
        battery_capex_per_kw = capital_cost_per_kwp - avg_pv_capex
        battery_capex_per_kw = max(battery_capex_per_kw, 0)
    else:
        battery_capex_per_kw = 0.0

    # ------------------------------------------------------------------
    # 6. Return rich results
    # ------------------------------------------------------------------
    return {
        'LCOE ($/MWh)': round(lcoe, 2),
        'Total PV Costs ($B)': round(pv_costs / 1e9, 3),
        'Total PV Energy (TWh)': round(pv_energy, 3),
        'Total CAPEX ($B)': round(np.sum(capex) / 1e9, 3),
        'Total O&M ($B)': round(np.sum(om_cost) / 1e9, 3),
        'Total Grid Maintenance ($B)': round(np.sum(grid_cost) / 1e9, 3),
        'Battery CAPEX per kW ($/kW)': round(battery_capex_per_kw, 0),
        'PV-only CAPEX per kW ($/kW)': round(avg_pv_capex, 0),
        'Assumed Battery Duration (hr)': battery_duration_hr,
        'NREL ATB Reference': '2024 ATB Advanced Scenario (avg 2025–2035)',
    }


def cumulative_post_debt_cash_flow(cash_flows_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame with the cumulative sum of *Cash Flow Post-Debt*.
    Units stay in **$B** (same as the original column).
    """
    df = cash_flows_df[['Year']].copy()
    df['Cumulative Post-Debt Cash Flow ($B)'] = (
        cash_flows_df['Cash Flow Post-Debt ($B)'].cumsum()
    )
    return df


def calculate_funding_mix(inputs, bond_principal, buildout_years=10):
    us_adult_population = inputs['us_adult_population']
    participation_rate_low = inputs['participation_rate_low']
    participation_rate_mid = inputs['participation_rate_mid']
    participation_rate_high = inputs['participation_rate_high']
    individual_investment = inputs['individual_investment']
    
    diverted_funds_annual_mid = (12.5 + 2.5 + 7.5) * 10**9  # Fossil, DOE, DoD
    diverted_funds_10yr_mid = diverted_funds_annual_mid * buildout_years
    
    funding_mix = []
    for pr in [participation_rate_low, participation_rate_mid, participation_rate_high]:
        num_investors = us_adult_population * pr
        bond_proceeds = num_investors * individual_investment
        bond_coverage = bond_proceeds / bond_principal * 100 if bond_principal > 0 else 0
        diverted_funds = diverted_funds_10yr_mid
        tax_revenue_needed = bond_principal - bond_proceeds - diverted_funds
        tax_revenue_percent = tax_revenue_needed / bond_principal * 100 if bond_principal > 0 else 0
        funding_mix.append({
            'Participation Rate (%)': pr * 100,
            'Number of Investors (M)': num_investors / 10**6,
            'Bond Proceeds ($B)': bond_proceeds / 10**9,
            'Bond Coverage (%)': bond_coverage,
            'Diverted Funds ($B)': diverted_funds / 10**9,
            'Diverted Funds Coverage (%)': diverted_funds / bond_principal * 100 if bond_principal > 0 else 0,
            'Tax Revenue Needed ($B)': tax_revenue_needed / 10**9,
            'Tax Revenue Coverage (%)': tax_revenue_percent
        })
    
    return pd.DataFrame(funding_mix)

def calculate_metrics(inputs, cash_flows_df, bond_principal, project_lifespan=30):
    discount_rate = inputs['discount_rate']
    bond_term = inputs['bond_term']
    #bond_issuance_flat_fee = inputs['bond_issuance_flat_fee']
    bond_interest_rate = inputs['bond_interest_rate']
    individual_investment = inputs['individual_investment']
    
    cash_flows_post_debt = cash_flows_df['Cash Flow Post-Debt ($B)'] * 10**9
    npv_post_debt = npf.npv(discount_rate, cash_flows_post_debt) / 10**12
    irr_post_debt = npf.irr(cash_flows_post_debt) * 100 if npf.irr(cash_flows_post_debt) is not None else float('nan')
    payback_year_post_debt = next((i + 1 for i, cf in enumerate(np.cumsum(cash_flows_post_debt)) if cf > 0), project_lifespan) if any(cf > 0 for cf in np.cumsum(cash_flows_post_debt)) else project_lifespan
    cumulative_surplus_post_debt = sum(cash_flows_post_debt) / 10**12
    total_interest_paid = sum(cash_flows_df['Interest Payment ($B)']) * 10**9 / 10**12
    total_dividends_paid = sum(cash_flows_df['Dividends ($B)']) * 10**9 / 10**12
    debt_coverage_ratio_year10 = (cash_flows_df['Cash Flow Pre-Debt ($B)'].iloc[9] * 10**9 / (-npf.pmt(bond_interest_rate, bond_term, bond_principal))) if bond_term > 0 and bond_principal > 0 else float('nan')
    final_reinvested_balance = cash_flows_df['Reinvested Balance ($B)'].iloc[-1] * 10**9 / 10**12
    
    investor_cash_flows = [-individual_investment] + cash_flows_df['Investor Total Cash Flow ($)'].tolist()
    investor_irr = npf.irr(investor_cash_flows) * 100 if npf.irr(investor_cash_flows) is not None else float('nan')
    investor_ending_value = sum(investor_cash_flows[1:])
    investor_cagr = ((investor_ending_value / individual_investment) ** (1 / project_lifespan) - 1) * 100
    return {
        'NPV Post-Debt ($T)': npv_post_debt,
        'IRR Post-Debt (%)': irr_post_debt,
        'Project Payback Period (Years)': payback_year_post_debt,
        'Cumulative Surplus ($T)': cumulative_surplus_post_debt,
        'Total Interest Paid ($T)': total_interest_paid,
        'Total Dividends Paid ($T)': total_dividends_paid,
        'Debt Coverage Ratio Year 10': debt_coverage_ratio_year10,
        'Final Reinvested Balance ($T)': final_reinvested_balance,
        'Individual Bond Investor CAGR (%)': investor_cagr,
        'Individual Bond Investor IRR (%)': investor_irr,
        'Individual Bond Investor Ending Balance ($)': investor_ending_value
    }





