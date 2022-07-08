from functions_cms_feature import *
import json
from config_parsing import configJsonParsing

def singleChannelFeatureExtraction(rawdata,fs,gain,offset,vib_sensitivity,n_bands,RPM,gear_ratio):
	nyquist_freq = fs//2
	## DC remove
	data_dc_removed = makeDCRemovedData(rawdata)
	## Calibration
	data_calibrated = ADCLinearCalibrationFromIntegerToVoltage(data_dc_removed,gain,offset)
	data_calibrated = sensorCalibrationFromVoltageToPhysicalValue(data_calibrated,vib_sensitivity)
	## FFT
	faxis, data_fft = realFFT(data_calibrated,fs)

	## Frequency analysis
	## 1. band energy
	band_rms = bandEnergyCalculation(data_fft,n_bands)
	## 2. overall RMS
	overall_rms = rmsCalculation(data_fft)
	## 3. Harmonics RMS
	base_frequency, harmonics_rms = harmonicsRMS(data_fft,nyquist_freq,RPM,gear_ratio)
	
	## Statistics
	## 4. standard deviation
	std = np.std(data_calibrated)
	## 5. skewness
	skew = stats.skew(data_calibrated)
	## 6. kurtosis
	kurt = stats.kurtosis(data_calibrated)

	return band_rms, overall_rms, base_frequency, harmonics_rms, std, skew, kurt

def multiChannelFeatureEXtraction(rawdata_nchannels,fs,gain_list,offset_list,vib_sensitivity_list,n_bands_list,RPM_list,gear_ratio_list):
	band_rms_result = []
	overall_rms_result = []
	base_frequency_result = []
	harmonics_rms_result = []
	std_result = []
	skew_result = []
	kurt_result = []
	for k,rawdata in enumerate(rawdata_nchannels):
		band_rms, overall_rms, base_frequency, harmonics_rms, std, skew, kurt = \
		singleChannelFeatureExtraction(rawdata,fs,gain_list[k],offset_list[k],vib_sensitivity_list[k],n_bands_list[k],RPM_list[k],gear_ratio_list[k])
		band_rms_result.append(band_rms)
		overall_rms_result.append(overall_rms)
		base_frequency_result.append(base_frequency)
		harmonics_rms_result.append(harmonics_rms)
		std_result.append(std)
		skew_result.append(skew)
		kurt_result.append(kurt)
	return band_rms_result, overall_rms_result, base_frequency_result, harmonics_rms_result, std_result, skew_result, kurt_result

def concatenateResult(config_parsing_result,anomaly_score_result,band_rms_result,overall_rms_result,base_frequency_result,harmonics_rms_result,std_result,skew_result,kurt_result,N_channels=8):	
	output_result = {}
	output_result['HAEcms'] = [{}]
	output_result['HAEcms'][0]['fr'] = 'CMS_ALG'
	output_result['HAEcms'][0]['to'] = 'CMS_DMC'
	output_result['HAEcms'][0]['rt'] = 'algo_result'
	output_result['HAEcms'][0]['si'] = ''
	output_result['HAEcms'][0]['ct'] = config_parsing_result[4]
	output_result['HAEcms'][0]['con'] = {}
	output_result['HAEcms'][0]['con']['algoVersion'] = 'v0.0.1'
	output_result['HAEcms'][0]['con']['portInfo'] = [{},{},{},{},{},{},{},{}]
	for k in range(N_channels):
		print(k)
		output_result['HAEcms'][0]['con']['portInfo'][k]['portNum'] = (config_parsing_result[5])[k]
		ai_score_channel = ('/').join([ str(i) for i in anomaly_score_result[k] ])
		output_result['HAEcms'][0]['con']['portInfo'][k]['aiscore'] = ai_score_channel
		output_result['HAEcms'][0]['con']['portInfo'][k]['installedSite'] = (config_parsing_result[6])[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['sensorOpt'] = (config_parsing_result[7])[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['algoType'] = (config_parsing_result[12])[k]
		band_num_channel = str(len(band_rms_result[k]))
		band_rms_str = ('/').join([ str(i) for i in band_rms_result[k] ])
		band_rms_channel = band_num_channel+'/'+band_rms_str
		output_result['HAEcms'][0]['con']['portInfo'][k]['freqBandEnergy'] = str(band_rms_channel)
		output_result['HAEcms'][0]['con']['portInfo'][k]['overallRMS'] = overall_rms_result[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['baseFreq'] = base_frequency_result[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['freqHarmonicsRMS'] = harmonics_rms_result[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['standardDeviation'] = std_result[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['Skewness'] = skew_result[k]
		output_result['HAEcms'][0]['con']['portInfo'][k]['Kurtosis'] = kurt_result[k]

	return output_result

if __name__=='__main__':

	configjsonfilename = '2_cms_config.json'
	with open(configjsonfilename,'r') as f:
		config_json_data = json.load(f)

	config_parsing_result = configJsonParsing(config_json_data)
	print( (config_parsing_result[5])[1] )
	anomaly_score_result = [[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8,0.9,1.0]]
	band_rms_result = [ [0.5]*32,[0.6]*32,[0.7]*32,[0.8]*32,[0.9]*32,[1.0]*32,[1.1]*32,[1.2]*64 ]
	overall_rms_result = [ 10,11,12,13,14,15,16,17 ]
	base_frequency_result = [ 20,21,22,23,24,25,26,27 ]
	harmonics_rms_result = [ 30,31,32,33,34,35,36,37 ]
	std_result = [ 40,41,42,43,44,45,46,47 ]
	skew_result = [ 50,51,52,53,54,55,56,57 ]
	kurt_result = [ 60,61,62,63,64,65,66,67 ]

	output_result = concatenateResult(config_parsing_result,anomaly_score_result,band_rms_result,overall_rms_result,base_frequency_result,harmonics_rms_result,std_result,skew_result,kurt_result,N_channels=8)
	
	with open('3_output.json','w') as f:
		json.dump(output_result,f,indent=4)

	output_result = str(output_result)
	print(type(output_result))
	print(output_result)