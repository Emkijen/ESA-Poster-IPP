import os
import sys
import numpy as np

sys.path.append('C:/Source/Rocket-Catch')
from dev.src.analysis.ipp_mc_figures import load_mc, horizontal_stats, along_cross_stats
from src.simulation.fetch_data import fetch

def main():
    date = '12_11_2024'
    print(f"Extracting MC data for {date}...")
    
    try:
        d_f = load_mc(date, 'gnss_baro_mag', sigma=1.5, n=100)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
        
    t_h, med_h, _, p95_h = horizontal_stats(d_f)
    
    data = fetch(date, verbose=False)
    ac = along_cross_stats(d_f, data)
    
    t = ac['t']
    e_along = ac['along_med']
    sigma_along = ac['along_p95'] / 3.0  # we want 1-sigma since plot script multiplies by 3
    
    e_cross = ac['cross_med']
    sigma_cross = ac['cross_p95'] / 3.0
    
    sigma_h = p95_h / 3.0
    
    out_csv = 'C:/Source/ESA-Poster-IPP/data/ipp_sim.csv'
    
    # Check lengths
    print(f"Lengths: t={len(t)}, e_h={len(med_h)}, sigma_h={len(sigma_h)}")
    
    # Save to csv
    header = "t,e_h,sigma_h,e_along,sigma_along,e_cross,sigma_cross"
    stacked = np.column_stack((t, med_h, sigma_h, e_along, sigma_along, e_cross, sigma_cross))
    np.savetxt(out_csv, stacked, delimiter=',', header=header, comments='')
    print(f"Saved MC medians to {out_csv}")

if __name__ == "__main__":
    main()
