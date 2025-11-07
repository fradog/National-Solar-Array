# National Solar Array Bond Initiative

**A financial and energy modeling tool demonstrating that a massive U.S. solar + storage array can achieve Net Zero by ~2035–2037 with strong economic returns, energy independence, and broad public participation.**

[Live Demo (Streamlit)](https://national-solar-array-ouuqzyhcvnqsmfbmy5cxnm.streamlit.app/) *(replace with actual link after deployment)*

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

## Background and Motivation

This model is highly interactive and all input parameters may be modified via input sliders and numerical text boxes. 
Reload the app to reset back to defaults.

It's primary purpose is to allow a user to explore sensitivies of financial results to the various inputs. 
Chief among these is the price charged for the energy produced by the array, the "Revenue per KWh" slider. 
As of late 2024 the average price of electricity in the U.S. was 16.48 cents per KWh for residential customers. 
Using this as a benchmark for electrical energy, I wanted to see what the cash flow would look like over the 
30 year lifetime for an array sized to produce eneouh electrical energy to replace all fossil fueled energy in the U.S..
The results were staggering, as should be expected from an energy technology which once the conversion devices are in place, 
produces energy for decades with only a small fraction of operation and maintenance cost. 

My goal was to understand whether this solution could be a viable one in terms of its potential to financially benefit all stakeholders.
The answer to that was yes. In addition to this app I actually began with an extensive spreadsheet which explored both the financial results, very similar to the calculations made in this coded version. I have leaned heavily on NREL's 2024 Annual Technology Baseline effort for sanity checks on results and for many input parameters and financial norms. (https://atb.nrel.gov/electricity/2024/about)

In my spreadsheet version I also evaluated raw material resource requirements for both panels and storage batteries, which includes the battery requirements for a fully electrified transport sector. I hope to add that to this app in due time. Suffice it to say for now that the results indicate no significant show stoppers in terms of raw materials.

In terms of worldwide Net Zero energy production, my assumption is that if the U.S. were to pursue a natioanlized array and grid as represented in this hypothetical, the transformational economic results would cancel any doubts other nations may have as to the benefits and prosperity that abundant solar sourced energy offers.

One obvious possible subversion to this hypothetical becoming reality is of course the adverse reaction that would likely come from powerful fossil fuel interests.
The answer to that is in the results. The return on investment here is largely unbeatable by any investment in fossil fuel. Now, current tax incentives, depreciation schedules, debt service, expected returns on equity, subsidies for fossil fuels, etc. of conventional solar projects (i.e. not a nationalized effort) lead to only a small advantage for solar installations currently. If one spends time using NREL's various available calculators to analyze a proposed commercial utility scale solar plus battery storage project this will become apparent. It is an impressive and rigorous set of tools they've created, but a time consuming and complex endeavor. 

In that business as usual context, nothing will change and we will struggle to add 50 GWp of solar arrays each year. This is one order of magnitude too little to achieve net zero by even mid century. This hypothetical explores a different context for the finacials which is obtained by nationalizing our entire grid. Contrary to other efforts to nationalize a sector of the economy, it is maintained here that our grid and the energy it supplies is crucial to our national interest and welfare. Typically, an effort to nationalize anything should be met with apprehension to say the least. Government is inefficient, largely incompetent, riddled with mediocrity, etc.. In this hypothetical we, the people, would literally own the array and the grid. We would commission its construction to the most efficient and highest performing contractors available. There are really only two models of excellence for this today in our country: SpaceX and Tesla.

I would hope that Fossil Fuel giants like Exxon Mobile, who actually contributed significant advancements to the mass production of photovoltaic devices back in th eearly seventies, would bid to help companies like Tesla/SpaceX design and build a new, vertically integrated, fully automated panel and battery production on site in the southwestern U.S.. This tool helps to show scenarios where we could offer such companies handsome returns on their investment into the array at levels that compete with and exceed the returns from their fossil fuel business today. I believe that once fully vetted and detailed hat this National Solar Array initiative will lead to positive outcomes for all. 

I am anxious to share this exploration wit contributors who see the potential of solar energy to transform the economy, as well as safeguard society from the effects of our ongoing and dangerous experiment with our greenhouse gases.


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
| **Individual Investor CAGR** | 6–15% |
| **Payback Period** | ~8–12 years |
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
