# Flow

## phase 1: getting into setup
 - case 1: btn7 connected >> phase 2
     - arduino: print("StartDataWrite-->")
 - case 2: btn7 not connected >> default

## phase 2: setting basic data
> there are 3 data to be set
> 1. nodeId
> 2. groupId
> 3. memberNum
> after getting message "StartDataWrite-->", python starts to write data into arduino through pyserial