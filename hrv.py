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
        bvp_data1= self.combined_data[:,1]
        bvp_data_normalized = np.where(bvp_data1< 0.00, -bvp_data1 , bvp_data1)
        # print("normalized data", bvp_data_normalized)
        # print ("raw data " ,self.combined_data[:, 1])
        
        # indices of peak bvp data 
        peaks, _ = find_peaks(bvp_data_normalized, height=0) 
        # print ( "peaks ", self.combined_data[peaks,0])
        
        # R-R intervals (time between successive peaks)
        rr_intervals = np.diff(self.combined_data[peaks, 0])
        # print ( "rr interval ", rr_intervals)
        return rr_intervals

    def calculate_rmssd(self):
        rr_intervals = self.calculate_rr_intervals()
        # RMSSD
        rmssd = round(np.sqrt(np.mean(np.square(np.diff(rr_intervals)))),3)
        return rmssd

    def determine_stress(self):
        rmssd = self.calculate_rmssd()
        stress_threshold = 35  # Example threshold, adjust as needed (0.035)
        if rmssd < stress_threshold:
            return "Stressed"
        else:
            return "Not Stressed"
        
# if __name__ == "__main__":
#     bvp_data = np.load('pulse.npy')
#     time_data = np.load('hrs.npy')
#     hrv_calculator = HRVCalculator(bvp_data, time_data)

#     rmssd = hrv_calculator.calculate_rmssd()

#     print("RMSSD (Root Mean Square of the Successive Differences):", rmssd)
#     stress_level = hrv_calculator.determine_stress()
#     print("Stress Level:", stress_level)
