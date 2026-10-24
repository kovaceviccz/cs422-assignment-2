# CS 422 Assignment 2

This repository contains the code and report for the second CS 422 assignment on iPerf, TCP statistics, and congestion control.

## Setup

Linux with CUBIC, Reno, and BBR available to TCP sockets, Python 3.12 or later, and Typst are required. If BBR is missing, load it with `sudo modprobe tcp_bbr`. On Ubuntu:

```bash
sudo apt-get install python3-venv
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

[Typst](https://github.com/typst/typst#installation) must also be installed and available as `typst`.

## Run

From the repository root:

```bash
.venv/bin/python assignment2.py listed_iperf3_servers.json \
  --destinations 10 --duration 15 --interval 0.5 --repetitions 2
```

Destination count, transfer duration, sampling interval, and repetitions are command-line options. Each run overwrites `results/`.

## Docker

```bash
docker build -t cs422-assignment2 .
mkdir -p results
docker run --rm --network host --user "$(id -u):$(id -g)" \
  -v "$PWD/results:/work/results" cs422-assignment2
```

Docker uses the host kernel, so CUBIC, Reno, and BBR must be available on the host.

## Files

```text
assignment2.py                  main script
iperf_client.py                 iperf3 client
tcp_stats.py                    TCP_INFO decoding
plots.py                        plot generation
listed_iperf3_servers.json      input downloaded from iperf3serverlist.net
report.typ                      report source
requirements.txt                Python dependencies
Dockerfile                      Ubuntu 24.04 environment
results/                        generated plots, raw measurements, and report
```

`report-data.json` supplies values to the [Typst report](results/assignment-2-report.pdf).
