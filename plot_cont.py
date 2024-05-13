
import numpy as np
from hrv import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from utils import *
from scipy.signal import medfilt, decimate
import csv

plt.ion()
bvp_data = np.load('pulse.npy')  # BVP measurements
time_data = np.load('hrs.npy')  # Time measurements
hrv_calculator = HRVCalculator(bvp_data, time_data)
rmssd = hrv_calculator.calculate_rmssd()
stress_level = hrv_calculator.determine_stress()

class DynamicPlot():    
    def __init__(self, signal_size, bs):
        self.batch_size = bs
        self.signal_size = signal_size
        self.launched = False
        

    def launch_fig(self):
        self.fig, (self.pulse_ax, self.hr_axis)= plt.subplots(2, 1)
        
        self.pulse_to_plot = np.zeros(self.signal_size)
        self.hrs_to_plot = np.zeros(self.signal_size)

        self.hr_texts = self.pulse_ax.text(0.5, 0.9,'0', ha='center', va='center', transform=self.pulse_ax.transAxes, fontsize= 16, fontweight='bold', color='blue')
        self.pulse_ax.set_title('Blood Volume')
        self.hr_axis.set_title('Heart Rate')
        self.pulse_ax.set_autoscaley_on(True)

        self.pulse_ax.plot(self.pulse_to_plot)
        self.hr_axis.plot(self.hrs_to_plot)

        self.pulse_ax.set_ylim(-3,3)
        self.hr_axis.set_ylim(0,180)
        self.launched = True
        
        plt.tight_layout()
        plt.show()
    
    def __call__(self, pipe):
        if self.launched == False: self.launch_fig()
        self.pipe = pipe
        self.call_back()

    def call_back(self):
        while True:
            data = self.pipe.recv()
            if data is None:
                self.terminate()
                break
            elif data == 'no face detected':
                self.update_no_face()
            else:    
                self.update_data(data[0], data[1])

    def update_no_face(self):
        hr_text = 'HR: NaN'
        self.hr_texts.set_text(hr_text)

        scaled = np.zeros(10)
        for i in range(0, len(scaled)):
            self.pulse_to_plot[0:self.signal_size-1] = self.pulse_to_plot[1:]
            self.pulse_to_plot[-1] = scaled[i]
            self.update_plot(self.pulse_ax, self.pulse_to_plot)
        
            self.hrs_to_plot[0:self.signal_size-1] = self.hrs_to_plot[1:]
            self.hrs_to_plot[-1] = 0
            self.update_plot(self.hr_axis, self.hrs_to_plot)
            self.re_draw()

    def update_data(self, p, hrs):
        self.hr_fft = moving_avg(hrs, 3)[-1] if len(hrs) > 5 else hrs[-1]
        hr_text = 'HR: ' + str(int(self.hr_fft))  
        # + ',   Stress: ' + stress_level + ',   HRV :' + str(rmssd)
        # hr_text = 'HR: ' + str(int(hr_fft))
        self.hr_texts.set_text(hr_text)

        # ma = moving_avg(p[-self.batch_size:], 6)
        batch = p[-self.batch_size:]
        decimated_p = decimate(batch, 3)
        scaled = scale_pulse(decimated_p)
        # self.blood_vol = np.max(scaled)
        for i in range(0, len(scaled)):
            self.pulse_to_plot[0:self.signal_size-1] = self.pulse_to_plot[1:]
            self.pulse_to_plot[-1] = scaled[i]
            self.update_plot(self.pulse_ax, self.pulse_to_plot)
            self.hrs_to_plot[0:self.signal_size-1] = self.hrs_to_plot[1:]
            self.hrs_to_plot[-1] = self.hr_fft
            self.update_plot(self.hr_axis, self.hrs_to_plot)
            self.re_draw()


    def update_plot(self, axis, y_values):
        line = axis.lines[0]
        line.set_xdata(np.arange(len(y_values)))
        line.set_ydata(y_values)
        axis.relim()
        axis.autoscale_view()
    def re_draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def terminate(self):
        """
        saves numpy array of rPPG signal as pulse
        """
        np.save('pulse', self.pulse_to_plot)
        
        # with open('vitalsReport.csv', mode='a+') as file:
        #     col_list=['Heart_rate','Blood_volume','Stress','HRV']
        #     writer = csv.DictWriter(file,fieldnames=col_list)
        #     writer.writerow({'Stress':stress_level , 'HRV' :rmssd , 'Heart_rate': self.hr_fft})
        with open('vitalsReport.csv', mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)

    # Modify the last row to append new data
        last_row = data[-1]
        last_row.append(str(self.hr_fft))
        last_row.append(str(self.pulse_to_plot[-1] *100))
        
        if len(data)==1:
            print("Stress and HRV will be appended after you test the next person")
        else :
            second_row =data[-2]
            second_row.append(stress_level)
            second_row.append(str(rmssd))

    # Rewrite the modified data to the file
        with open('vitalsReport.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


        plt.close('all')

    # def terminate1(self, event):
    #     if event.key() == ' ':
    #         self.terminate()




        


