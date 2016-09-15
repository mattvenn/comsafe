# compliance test

test was run for 10 hours

## hit generation

generate_hit.py from [bbb-r2rdac](https://github.com/mattvenn/bbb-r2rdac) used for generating hits

./generate_hit.py --hit-max 3000 --hit-len 100 --hit-slope 100 

creates the [data](data.txt) file with following characteristics:

* 3v max hit voltage 
* hit len between start of rise and start of fall is 100uS
* slope of rise and fall is 100uV/uS

load_data from bbb-r2rdac loads the data file into the DAC and is captured
by calibrated Tektronix MSO2004B scope and the fpga-adc.

[scope](TEK00010.PNG)

load_data was run on a cronjob every minute.

## hit capture

On the [fpga-adc](https://github.com/mattvenn/fpga-adc) system this command was run:

while true; do date >> hits; ./capture -n 600000000 | ./a.out -b 1024 -s 1000 -e 500  >> hits; done

This command runs a loop that captures 5 minutes of samples and  pipes them to the hit processor.
Hit processor arguments:

* start threshold of 1000 (1.22v)
* end threshold of 500 (0.61v)
* channel zeros both set to 0
* process data in 1024 sample size chunks

Screen was used to capture the session [screenlog.0](screenlog.0)

results were captured in the [hits](hits) file.

# tests

## buffer overflow

buffer should never overflow:

    grep '^    .*diff' screenlog.0 | cut -d' ' -f18 | sort -rn | head -3
    354676
    251008
    84432

shows maximum difference between read and write pointer is 354676 bytes.

## consistency of measurements

integral and hit length, hit max should not vary by more than 0.01%

    grep len hits | sort | uniq -c
        657 len    115.5(us)
       1071 len    116(us)

shows hit length is accurate to 0.005%

    grep integ hits  | cut -d'.' -f1  | sort | uniq -c
      30 integ  206
     886 integ  207
     812 integ  208

shows integral has very low variance, but scope shows integral as 288uVs so there is some discrepancy here.

    grep max hits  | sort -rn | ( head -n1 && tail -n1 )
    max    3(v)
    max    2.9916(v)

shows difference between min and max detected is 0.0084v. biggest deviation from 3v (target) is 0.0028%

## channel synchronisation

    grep 'hit started.*channel 0' hits | cut -d' ' -f 4 > chan0.start
    grep 'hit started.*channel 1' hits | cut -d' ' -f 4 > chan1.start

start by getting the start time of all hits into 2 files:

    diff -y chan0.start chan1.start | sed -ne 's/|/-/p' | wc -l 
    115

shows 115 of 860 hits were not synchronised to the sample

     diff -y chan0.start chan1.start | sed -ne 's/|/-/p' | bc | sort | uniq 
     1

shows that channels are out of synchronisation by maximum of 1 sample (0.5uS).

## no missing hits

every hit should be captured (10 hits per 5 minute recording)

number of tests run:

    grep Sep hits | wc -l
    172

so expected hits = 172 * 5 * 2 = 1720

    grep found.*hits hits | sort | uniq -c
    162 found 10 hits:
      5 found 12 hits:
      5 found 8 hits:

162 * 10 + 5 * 12 + 5 * 8 = 1720, no hits missed.

## linux stability

captured all kernel log messages during the test to [screenlog.1](screenlog.1), which shows no messages logged during the test.
