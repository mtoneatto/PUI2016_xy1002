
import urllib.request as urllib
import sys
import json
import numpy as np
import csv


def get_jsonparsed_data(url):
    """
    sys.argv[2]
    from http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """

    response = urllib.urlopen(url)
    return json.loads(response.read().decode("utf-8"))

apikey = sys.argv[1]
busline = sys.argv[2]
csv =  sys.argv[3]

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(apikey,busline)

jsonData = get_jsonparsed_data(url)






num = np.size(jsonData['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'])
print ('Bus Line : {}'.format(busline))
print ('Number of Active Buses : {}'.format(num))

if not len(sys.argv) == 4:
    print("Invalid number of arguments. Run as: python get_bus_info.py xxxx-xxxx-xxxx-xxxx-xxxx <BUS_LINE> <BUS_LINE>.csv")
    sys.exit()
fout = open(csv, "w")
fout.write('Latitude,Longitude,Stop Name,Stop Status\n')

for i in range(0,num):
   Latitude = get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
   Longitude = get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
   if np.size(get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']) < 1:
        StopName = 'N/A'
   else:
        StopName = get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall']['StopPointName']
   if np.size(get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']) < 1:
       StopStatus = 'N/A'
   else:
       StopStatus = get_jsonparsed_data(url)['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity'][i]['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']

   fout.write('{},{},{},{}\n'.format(Latitude,Longitude,StopName,StopStatus))


