# Comsafe Data Acquisition Software Requirements

## Data acquisition

* Samples must be taken from the ADCs at a rate of at least 2MHz.
* The sample resolution must be at least 12 bits over a 5V range.
* Two channels need to be samples simultaneously. 

## Hit processing

* Hits must be started a configurable time/number of samples before the signal passes above a configurable threshold.
* Hits last until the signal has been below another configurable threshold for at least some configurable time/number of samples
* If there a continuous noise situation then hit should be stopped at 100mS and trigger again immediately.
* The software must provide the start time, channel, peak amplitude and integrated signal for a hit as well as whether it was cut off because of the maximum hit length or, because it fell below the threshold.

## Interfacing to analysis software

* The software must interface to analysis software written in Lua to run on the BeagleBone Black. 
