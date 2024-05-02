import numpy as np
from scipy.signal import find_peaks
from scipy.stats import zscore

class HRVCalculator:
    def __init__(self, bvp_data, time_data):
        self.bvp_data = bvp_data
        self.time_data = time_data
        min_length = min(len(bvp_data), len(time_data))
        self.combined_data = np.column_stack((time_data[:min_length], bvp_data[:min_length]))

    def calculate_rr_intervals(self):
        # Normalize BVP data
        bvp_data_normalized = zscore(self.combined_data[:, 1])
        
        # Peaks in the BVP waveform
        peaks, _ = find_peaks(bvp_data_normalized, height=0)
        
        # R-R intervals (time between successive peaks)
        rr_intervals = np.diff(self.combined_data[peaks, 0])
        return rr_intervals

    def calculate_rmssd(self):
        rr_intervals = self.calculate_rr_intervals()
        # RMSSD (Root Mean Square of the Successive Differences)
        rmssd = np.sqrt(np.mean(np.square(np.diff(rr_intervals))))
        return rmssd

    def determine_stress(self):
        rmssd = self.calculate_rmssd()
        stress_threshold = 50  # Example threshold, adjust as needed (0.05)
        if rmssd < stress_threshold:
            return "Stressed"
        else:
            return "Not Stressed"
        
# if __name__ == "__main__":
#     bvp_data = np.load('pulse.npy')  # BVP measurements
#     time_data = np.load('hrs.npy')  # Time measurements
#     hrv_calculator = HRVCalculator(bvp_data, time_data)
#     rmssd = hrv_calculator.calculate_rmssd()
#     print("RMSSD (Root Mean Square of the Successive Differences):", rmssd)
    
#     # Determine stress
#     stress_level = hrv_calculator.determine_stress()
#     print("Stress Level:", stress_level)
