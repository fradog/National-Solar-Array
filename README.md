# National Solar Array Bond Initiative

**A financial and energy modeling tool demonstrating that a massive U.S. solar + storage array can achieve Net Zero by ~2035–2037 with strong economic returns, energy independence, and broad public participation.**

[Live Demo (Streamlit)](https://your-streamlit-app-url.streamlit.app) *(replace with actual link after deployment)*

---

## Overview

This project simulates a **national-scale solar photovoltaic (PV) + battery storage system** designed to replace all U.S. fossil fuel energy consumption by the mid-2030s. It models:

- **Energy production** with realistic capacity factor, degradation, and 10-year build-out
- **Financial cash flows** including CAPEX, O&M, grid maintenance, bond financing, carbon tax revenue, avoided fuel costs
- **Investor returns** via bond participation, dividends, and reinvestment
- **Levelized Cost of Energy (LCOE)** with full PV-based calculation and NREL ATB-style benchmark
- **CO₂ emissions phase-out** over the build period
- **Efficiency gains** from electrification (ICE → EV, fossil plants → direct solar)

The model shows that **at current average electricity prices (~$0.16/kWh)**, the system generates **massive surplus cash flows**, enabling:
- Full debt repayment
- High investor returns
- National reinvestment or public dividends

---

## Key Features

| Feature | Description |
|-------|-----------|
| **Interactive Dashboard** | Built with Streamlit — adjust all inputs in real time |
| **LCOE Validation Mode** | Toggle to zero extras and verify `Revenue = LCOE → NPV ≈ 0` |
| **Unlevered NPV** | Exact match with LCOE logic (no debt, no extras) |
| **NREL ATB Comparison** | Side-by-side FCR-based LCOE (no degradation) |
| **Efficiency Downgrade** | Models energy savings from electrifying transport & heating |
| **Bond + Dividend Model** | Public participation via $10k bonds, with CAGR/IRR tracking |
| **Plotly Visualizations** | Cash flows, balances, emissions reduction |
| **No Index Columns** | Clean tables using `.hide_index()` |

---

## File Structure

```
national-solar-array/
├── app.py                  # Main Streamlit dashboard
├── solar_model.py          # Core financial & energy calculations
├── efficiency_downgrade.py # Efficiency gain logic (electrification)
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/national-solar-array.git
cd national-solar-array

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## `requirements.txt`

```txt
streamlit
pandas
numpy
numpy-financial
plotly
```

---

## Model Inputs (Sidebar)

| Category | Key Parameters |
|--------|----------------|
| **System Scale** | Initial/Target Capacity (GWp), Capacity Factor |
| **Costs** | CAPEX ($/kWp), O&M Rate, Grid Maintenance ($B/yr) |
| **Revenue** | Revenue $/kWh, Avoided Fuel $/kWh |
| **Financing** | Bond Rate, Term, Reinvestment %, Dividend % |
| **Emissions** | Carbon Tax $/ton, Displaceable Proportion |
| **Efficiency** | ICE/EV/Utility efficiencies (sliders) |

---

## Validation Mode

Enable **"LCOE Validation Mode"** in the sidebar to:
- Zero: avoided fuel, carbon tax, grid maintenance, degradation, bond costs
- Force `revenue_per_kwh = LCOE`
- Display **Unlevered NPV ≈ $0.00T** → confirms model consistency

---

## LCOE Methodology

- **Your Model**: Full PV of costs ÷ PV of energy (with degradation & build-out)
- **NREL ATB Style**: Fixed Charge Rate (FCR), constant output, no degradation
- **Diagnostic Table**: CAPEX, energy, capacity over time

---

## Sample Results (Default Inputs)

| Metric | Value |
|------|-------|
| **Target Capacity** | 5,498 GWp |
| **LCOE (Your Model)** | ~$58.24/MWh |
| **LCOE (NREL FCR)** | ~$55.10/MWh |
| **Bond Principal** | ~$9.5T |
| **NPV Post-Debt** | +$10–15T |
| **Individual Investor CAGR** | 6–8% |
| **Payback Period** | ~8–10 years |
| **Area Required** | ~21,000 sq mi |

---

## Assumptions & Conservatism

- 10-year linear build-out
- 0.7%/yr panel degradation
- No additional CAPEX to offset degradation
- Grid maintenance: $50B/yr fixed
- Carbon tax applied only during build
- Efficiency gains: ~75–80% reduction in primary energy via electrification
- All values in **real dollars** (no inflation)

---

## Contributing

Contributions welcome! Open an issue or PR for:
- New sensitivity charts
- CSV export
- Multi-scenario comparison
- API integration
- Deployment scripts

---

## License

[MIT License](LICENSE) – Free to use, modify, and distribute.

---

## Author

**Doug Frasher**  
With modeling support from **Grok (xAI)**

> *"We don’t need to choose between climate action and prosperity — this model proves we can have both."*

---

**Deployed on Streamlit Community Cloud** – [Launch App](#) *(update link)*

---

*Last updated: November 06, 2025*
