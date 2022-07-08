import json
import numpy as np

def configJsonParsing(config_json_data,N_channels=8):
	result = []

	messege_fr = config_json_data['HAEcms'][0]['fr']
	messege_to = config_json_data['HAEcms'][0]['to']
	messege_rt = config_json_data['HAEcms'][0]['rt']
	messege_si = config_json_data['HAEcms'][0]['si']
	messege_ct = config_json_data['HAEcms'][0]['ct']
	result.extend( [messege_fr] )
	result.extend( [messege_to] )
	result.extend( [messege_rt] )
	result.extend( [messege_si] )
	result.extend( [messege_ct] )

	messege_contents = config_json_data['HAEcms'][0]['con']['portInfo']

	portnum_channels = ['']*N_channels
	installedsite_channels = ['']*N_channels
	sensoropt_original = ['']*N_channels
	sensor_sensitivity_channels = ['']*N_channels
	gear_ratio_channels = ['']*N_channels
	gain_channels = ['']*N_channels
	offset_channels = ['']*N_channels
	algorithm_type_channels_original = ['']*N_channels
	algorithm_type_channels = ['']*N_channels
	bandnum_channels = ['']*N_channels

	for k in range(len(messege_contents)):
		portnum_channels[k] = int(messege_contents[k]['portNum'])
		installedsite_channels[k] = messege_contents[k]['installedSite']

		sensoropt_original[k] = messege_contents[k]['sensorOpt']
		sensoropt_split = sensoropt_original[k].split('/')
		
		sensor_sensitivity_channels[k] = np.float32(sensoropt_split[0])

		gear_ratio_channels[k] = np.float32(sensoropt_split[1])

		gain_channels[k] = np.float32(sensoropt_split[2])

		offset_channels[k] = np.float32(sensoropt_split[3])

		algorithm_type_channels_original[k] = messege_contents[k]['algoType']
		algorithm_type_channels_num = int((algorithm_type_channels_original[k])[0])
		algorithm_type = ['']*algorithm_type_channels_num
		for kk in range(algorithm_type_channels_num):
			algorithm_type[kk] = algorithm_type_channels_original[k][kk+1]
		algorithm_type_channels[k] = algorithm_type

		bandnum_channels[k] = int(messege_contents[k]['bandNum'])

	result.append( portnum_channels )
	result.append( installedsite_channels )
	result.append( sensoropt_original )
	result.append( sensor_sensitivity_channels )
	result.append( gear_ratio_channels )
	result.append( gain_channels )
	result.append( offset_channels )
	result.append( algorithm_type_channels_original )
	result.append( algorithm_type_channels )
	result.append( bandnum_channels )

	return result

if __name__=='__main__':

	jsonfilename = '2_cms_config.json'
	with open(jsonfilename,'r') as json_file:
		config_json_data = json.load(json_file)

	result = configJsonParsing(config_json_data,N_channels=8)

	messege_fr = result[0]
	messege_to = result[1]
	messege_rt = result[2]
	messege_si = result[3]
	messege_ct = result[4]
	portnum_channels = result[5]
	installedsite_channels = result[6]
	sensoropt_original = result[7]
	sensor_sensitivity_channels = result[8]
	gear_ratio_channels = result[9]
	gain_channels = result[10]
	offset_channels = result[11]
	algorithm_type_channels_original = result[12]
	algorithm_type_channels = result[13]
	bandnum_channels = result[14]
	
	print('messege_fr :',messege_fr)
	print('messege_to :',messege_to)
	print('messege_rt :',messege_rt)
	print('messege_si :',messege_si)
	print('messege_ct :',messege_ct)
	print('   portNum :',portnum_channels)
	print('   installedSite :',installedsite_channels)
	print('   sensoropt_original :',sensoropt_original)
	print('       sensor_sensitivity_channels :',sensor_sensitivity_channels)
	print('       gear_ratio_channels :',gear_ratio_channels)
	print('       gain_channels :',gain_channels)
	print('       offset_channels :',offset_channels)
	print('   algorithm_type_channels_original :',algorithm_type_channels_original)
	print('       algorithm_type_channels :',algorithm_type_channels)
	print('   bandnum_channels :',bandnum_channels)