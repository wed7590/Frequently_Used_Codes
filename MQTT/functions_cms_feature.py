import numpy as np
from scipy import signal, stats

def firstOrderDCRemovalFilter(data,R,xn=0):
	num = [ 1,-1 ]
	den = [ 1,-R ]
	zi = signal.lfilter_zi(num,den)
	z,_ = signal.lfilter(num,den,data,zi=zi*xn)
	return z

def makeDCRemovedData(data,n_sample_remove=1000,R=0.99,xn=0,past_data=None):
	data_np = np.array(data)
	if not past_data:
		padded_value = data_np[0]
		padded_vector = data_np[0]*np.ones(n_sample_remove)
		data_temp = np.append(padded_vector,data_np)
	else:
		past_data_np = np.array(past_data)
		data_temp = np.append(past_data_np,data_np)
	data_dc_removed = firstOrderDCRemovalFilter(data_temp,R,xn)
	return data_dc_removed[n_sample_remove:]

def ADCLinearCalibrationFromIntegerToVoltage(data_int_list,gain,offset):
	data_int_np = np.array(data_int_list)
	data_volt = (data_int_np-offset)/gain
	return data_volt

def sensorCalibrationFromVoltageToPhysicalValue(data_list,sensor_sensitivity):
	data_np = np.array(data_list)
	data_calibrated = data_np/sensor_sensitivity
	return data_calibrated

def realFFT(data, fs, freq_resolution=1):
	bandwidth = fs/2
	N_fft = np.int(fs/freq_resolution)
	len_f = np.int( ( N_fft/2+1 )*(N_fft%2==0) + ( (N_fft+1)/2 )*(N_fft%2==1) )
	f = np.linspace(0,bandwidth,len_f)
	#data_fft = np.fft.rfft( data, n=N_fft ) / np.sqrt(fs)
	data_fft = np.fft.rfft( data, n=N_fft ) / N_fft*2
	return list(f),data_fft

def rmsCalculation(data):
	return np.sqrt( np.mean( np.square( np.abs(data) ) ) )


def bandEnergyCalculation(data_fft,n_bands):
	bandwidth = (len(data_fft)-1)//n_bands
	band_rms = []
	for k in range(n_bands):
		band_segment = data_fft[(k)*bandwidth:(k+1)*bandwidth]
		rms_band_segment = rmsCalculation(band_segment)
		band_rms.append(rms_band_segment)
	return np.array(band_rms)

def harmonicsRMS(data_fft,nyquist_freq,RPM,gear_ratio):
	base_frequency = (RPM/60)/gear_ratio
	n_harmonics = int(nyquist_freq//base_frequency)
	harmonics_frequency = [ int((i+1)*base_frequency) for i in range(n_harmonics)]
	data_fft_harmonics = np.zeros(len(data_fft))
	data_fft_harmonics[harmonics_frequency] = np.abs(data_fft[harmonics_frequency])
	harmonics_rms = rmsCalculation(data_fft_harmonics)

	return base_frequency, harmonics_rms