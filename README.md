# Azure Configuration


## Blob Storage
- Create the blob storage as you want, depending on the amount of data.

## Azure IoT Central
1. ... (Create IoT Central)
2. *Connect the Blob Storage to IoT Central*
- In IoT Central, go to 'Data export' on the left bar.
-  Press New export
Define an export name, select type of data as telemetry and choose the destination (if you do not have, go to the next steps)
- Press create a new one
You can find the credentials in: Storage Account/Access Keys.
- Go to data transformation:
In 'Add your input message, choose your device template.
In 'Build transformation query', copy the query that you want to save in Blob Storage, for example:
```json
import "iotc" as iotc;    
{
    leftWheelSpeed: .telemetry | iotc::find(.name == "leftWheelSpeed").value,
    rightWheelSpeed: .telemetry | iotc::find(.name == "rightWheelSpeed").value,
    sonarDistance: .telemetry | iotc::find(.name == "sonarDistance").value,
    detectedObject: .telemetry | iotc::find(.name == "detectedObject").value,
    deviceId: .device.id,
    Timestamp: .enqueuedTime,
}
```
reference: https://learn.microsoft.com/en-us/azure/iot-central/core/howto-transform-data-internally

- press Save and wait for 'Export status' to change to healthy. 
- Reference:
https://learn.microsoft.com/en-us/azure/iot-central/core/howto-export-to-blob-storage?tabs=connection-string%2Cjavascript