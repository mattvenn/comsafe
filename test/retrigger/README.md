# retrigger

Test to satisfy following requirement:

* If there a continuous noise situation then hit should be stopped at 100mS and trigger again immediately.

A 1.6ms (3200 samples) hit was generated:

    ./generate_hit.py --hit-max 3300 --hit-len 1600 --hit-slope 500

With no maximum hit length (only considering channel 1):

    ./capture  | ./hit-proc  -s2500 -e2300

    chan   1
    start  7.41999(s)
    end    7.42159(s)
    max    3.37607(v)
    len    1599.5(us)
    integ  5390.9(uVs)
    cutoff 0

With maximum hit length set to 320 samples:

    ./capture  | ./hit-proc  -s2500 -e2300 -m320 > hits

    grep 'hit started.*channel 1' hits  | wc -l
    10

Shows 10 hits were captured (channel 1).

    grep cutoff hits  | uniq -c
     18 cutoff 1
      2 cutoff 0

Shows first 18 (both channels) hits were cutoff, last 2 weren't.
[Hit file](hits)
