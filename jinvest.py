#!/usr/bin/env python3
import sys

print('journal reader')

livenessPodState = {

}

readinessPodState = {

}

evictionManager = {
    "data": {},
    "time": {}
}
def addEvictionMetric(name, value, time):
    arr = []
    _time = []
    if name not in evictionManager["data"]:
        evictionManager["data"][name] = arr
        evictionManager["time"][name] = _time
    else: 
        arr = evictionManager["data"][name]
        _time = evictionManager["time"][name]
    arr.append(value)
    _time.append(time)

#with open("/run/media/rvanderp/ssd2/tmp/must-gather.local.40216767327432962/quay-io-openshift-release-dev-ocp-v4-0-art-dev-sha256-a0dbe73b7831a8ddb9a2c58a560461d7c2c23a92231289a2104b93e7723c0eff/host_service_logs/masters/kubelet_service.log", "r") as file:
with open(sys.argv[1], "r") as file:
    for line in file:
        tokens = line.split("]")
        if len(tokens) >= 3:
            token = tokens[2].strip()
            if token.startswith("Liveness probe"):
                parts = token.split("\"")
                name = parts[1]                
                if token.endswith("succeeded"):
                    if name not in livenessPodState or livenessPodState[name] != "Live":
                        print (line[0:15] + "|ALIVE     | " + name)
                    livenessPodState[name] = "Live"
                else:
                    if name not in livenessPodState or livenessPodState[name] != "Dead":
                        print (line[0:15] + "|DEAD      | " + name)
                    livenessPodState[name] = "Dead"

            elif token.startswith("Readiness probe"):
                parts = token.split("\"")
                name = parts[1]
                if token.endswith("succeeded"):
                    if name not in readinessPodState or readinessPodState[name] != "Ready":
                        print (line[0:15] + "|READY     | " + name)
                    readinessPodState[name] = "Ready"
                else:
                    if name not in readinessPodState or readinessPodState[name] != "Not Ready":
                        print (line[0:15] + "|NOT READY | " + name)
                    readinessPodState[name] = "Not Ready"
            
            elif token.startswith("eviction manager"):
                parts = token.split("observations:")
                if len(parts) <=1: 
                    continue;
                parts = parts[1]
                parts = parts.split(",")
                signal = parts[0].split("=")[1]
                availability = parts[1].split(": ")[1]
                addEvictionMetric(signal,availability, line[0:15])
    
    for key in evictionManager["data"]:    
        i=0
        while i < len(evictionManager["data"][key]):        
            print (key+"|"+evictionManager["time"][key][i] + "|" + evictionManager["data"][key][i])
            i += 1


