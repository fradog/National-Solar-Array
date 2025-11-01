# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 10:07:01 2025

@author: dhfra
"""

import numpy as np
import numpy_financial as npf
import pandas as pd

def calculate_efficiency_downgrade(mix_inputs): 
    
    pet_energy = mix_inputs['total_energy_quads'] * mix_inputs['petroleum_fraction']
    gas_energy = mix_inputs['total_energy_quads'] * mix_inputs['gas_fraction']  # Fixed: asg → gas
    coal_energy = mix_inputs['total_energy_quads'] * mix_inputs['coal_fraction']
    print(pet_energy)
    
    pet_trans_energy = pet_energy * mix_inputs['petroleum_trans_fraction']
    gas_trans_energy = gas_energy * mix_inputs['gas_trans_fraction']
    coal_trans_energy = coal_energy * mix_inputs['coal_trans_fraction']
    pet_heating_energy = pet_energy * mix_inputs['petroleum_heating_fraction']
    gas_heating_energy = gas_energy * mix_inputs['gas_heating_fraction']
    coal_heating_energy = coal_energy * mix_inputs['coal_heating_fraction']
    pet_elec_energy = pet_energy * mix_inputs['petroleum_elec_fraction']
    gas_elec_energy = gas_energy * mix_inputs['gas_elec_fraction']
    coal_elec_energy = coal_energy * mix_inputs['coal_elec_fraction']
    
    pet_ice_downgrade = pet_trans_energy * mix_inputs['vehicle_ice_eff'] / mix_inputs['vehicle_elec_eff']  # Fixed spelling
    pet_heating_downgrade = pet_heating_energy * mix_inputs['petroleum_heating_eff'] / mix_inputs['elec_heating_eff']
    pet_elec_downgrade = pet_elec_energy * mix_inputs['utility_ice_elec_eff'] / mix_inputs['elec_elec_eff']
    gas_ice_downgrade = gas_trans_energy * mix_inputs['vehicle_ice_eff'] / mix_inputs['vehicle_elec_eff']
    gas_heating_downgrade = gas_heating_energy * mix_inputs['gas_heating_eff'] / mix_inputs['elec_heating_eff']
    gas_elec_downgrade = gas_elec_energy * mix_inputs['utility_ice_elec_eff'] / mix_inputs['elec_elec_eff']  # Fixed: utiltiy
    coal_trans_downgrade = coal_trans_energy * mix_inputs['vehicle_ice_eff'] / mix_inputs['vehicle_elec_eff']
    coal_heating_downgrade = coal_heating_energy * mix_inputs['coal_heating_eff'] / mix_inputs['elec_heating_eff']
    coal_elec_downgrade = coal_elec_energy * mix_inputs['utility_ice_elec_eff'] / mix_inputs['elec_elec_eff']  # Fixed key
    print(pet_ice_downgrade)
    
    
    pet_dg = (pet_ice_downgrade + pet_heating_downgrade + pet_elec_downgrade)
    gas_dg = (gas_ice_downgrade + gas_heating_downgrade + gas_elec_downgrade)
    coal_dg = (coal_trans_downgrade + coal_heating_downgrade + coal_elec_downgrade)
    dg = pet_dg + gas_dg + coal_dg
    dg_ratio = dg / mix_inputs['total_energy_quads']
    return dg_ratio

# Add this at the bottom of efficiency_downgrade.py
if __name__ == "__main__":
    # Only runs when you execute the file directly
    test_inputs = {
        'total_energy_quads': 77.10,
        'petroleum_fraction': .459,
        'gas_fraction': .436,
        'coal_fraction': .105,
        'petroleum_trans_fraction': .696,
        'petroleum_heating_fraction': .296,
        'petroleum_elec_fraction': .008,
        'gas_trans_fraction': .040,
        'gas_heating_fraction': .560,
        'gas_elec_fraction': .400,
        'coal_trans_fraction': 0.0,
        'coal_heating_fraction': .114,
        'coal_elec_fraction': .886,
        'vehicle_ice_eff': .200,
        'vehicle_elec_eff': .800,
        'utility_ice_elec_eff': .370,
        'petroleum_heating_eff': 1.000,
        'gas_heating_eff': 1.000,
        'coal_heating_eff': 1.000,
        'elec_heating_eff': 1.000,
        'ele_elec_eff': 1.000
    }
    print("Test result:", calculate_efficiency_downgrade(test_inputs))
    

                                                                                                  


