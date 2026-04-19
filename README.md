# Static-Routing-using-SDN-with-POX-Controller-in-Mininet
---

## Problem Statement

This project implements static routing using Software Defined Networking (SDN) in a Mininet environment. A POX controller is used to install flow rules using the OpenFlow protocol, demonstrating controller–switch interaction, match–action rule design, and network behavior.

---

## Objective

* To understand SDN architecture and centralized control
* To implement static routing using a POX controller
* To design match–action flow rules
* To handle PacketIn events in controller logic
* To analyze network behavior using tools like ping, iperf, and Wireshark

---

## SDN Overview

Software Defined Networking (SDN) separates the control plane from the data plane:

* **Controller (POX)** → makes decisions
* **Switches (s1, s2, s3)** → execute forwarding rules
* **OpenFlow** → communication protocol between controller and switches

---

## Network Topology

```
h1 — s1 — s2 — s3 — h3
           |
           h2
```

* **h1, h2, h3** → hosts
* **s1, s2, s3** → switches
* **s2** → central switch

---

## Implementation Details

###  Controller Logic

* Listens for **PacketIn** events
* Uses **match–action** rules
* Installs flow entries in switches using OpenFlow

###  Flow Rule Structure

* **Match** → identifies packet (MAC/IP)
* **Action** → forward / drop / flood

---

## Test Scenarios

### Scenario 1: Normal (Flooding)

* Switch s2 floods packets
* All hosts can communicate

**Expected Output:**

```
pingall → 0% dropped
```

---

### Scenario 2: Static Routing (Blocked)

* Only h1 ↔ h2 communication allowed
* Traffic from h3 is blocked

**Expected Output:**

```
h1 ↔ h2 → Success
h3 → Failed
```

---

##  Setup & Execution

###  Step 1: Clean environment

```bash
sudo mn -c
pkill -f pox
```

---

### Step 2: Run Normal Version

```bash
cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 ext.myrouter
```

```bash
sudo mn --topo linear,3 --controller=remote
```

---

### Step 3: Run Blocked Version

```bash
cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 ext.myrouter_block
```

```bash
sudo mn --topo linear,3 --controller=remote
```

---

## Testing & Validation

### Connectivity Test

```bash
mininet> pingall
```

---

### Latency Test (ICMP)

```bash
mininet> h1 ping -c 5 h2
```

---

### Throughput Test (iperf)

```bash
mininet> h2 iperf -s &
mininet> h1 iperf -c h2
```

---

### Flow Table Inspection

```bash
mininet> dpctl dump-flows
```

---

## Regression Testing

Flow rules are deleted and reinstalled to ensure consistent behavior:

```bash
mininet> sh ovs-ofctl del-flows s1
mininet> sh ovs-ofctl del-flows s2
mininet> sh ovs-ofctl del-flows s3
mininet> pingall
```

Behavior remains unchanged → Validation successful

---

## Performance Analysis

| Metric     | Tool  | Description                 |
| ---------- | ----- | --------------------------- |
| Latency    | ping  | Measures round-trip delay   |
| Throughput | iperf | Measures data transfer rate |
| Flow Rules | dpctl | Displays installed rules    |

---

## Packet Analysis (Wireshark)

Captured packets include:

* **ARP** → Address resolution
* **ICMP** → Ping request/reply

This confirms correct packet flow and routing behavior.

---

## Proof of Execution

Screenshots included:

* pingall (normal & blocked)
* Flow table entries
* iperf output
* Controller logs
* Wireshark capture

---

## Tools Used

* Mininet
* POX Controller
* OpenFlow Protocol
* Wireshark
* iperf

---

## Results

* Successfully demonstrated SDN-based routing
* Implemented static routing using flow rules
* Verified controller–switch interaction
* Demonstrated controlled network behavior

---

## References

* POX Documentation
* Mininet Documentation
* OpenFlow Specification

---

## Conclusion

This project demonstrates the power of SDN in controlling network behavior using a centralized controller. By implementing static routing and access control, we showed how network policies can be enforced dynamically using software-defined logic.

---
