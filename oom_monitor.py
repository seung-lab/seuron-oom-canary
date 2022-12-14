from subprocess import PIPE, STDOUT, Popen
import os
import sys
import logging
import requests
from kombu import Connection


def get_hostname():
    METADATA_URL = "http://metadata.google.internal/computeMetadata/v1/instance/"
    METADATA_HEADERS = {"Metadata-Flavor": "Google"}

    data = requests.get(METADATA_URL + "hostname", headers=METADATA_HEADERS).text
    return data.split(".")[0]


def run_oom_canary():
    total_mem = int(os.popen("free -b").readlines()[1].split()[1])
    alloc_mem = total_mem // 10  # Allocate 10% of the total memory
    logging.info(f"Alloca {alloc_mem} out of {total_mem} bytes")
    proc = Popen(("./oom_canary", str(alloc_mem)), stdout=PIPE, stderr=STDOUT)
    with open(f"/proc/{proc.pid}/oom_score_adj", "w") as f:
        f.write("1000")
    proc.wait()


def notify_oom(qurl, queue):
    logging.info(f"Message {queue} at {qurl}")
    with Connection(qurl) as conn:
        queue = conn.SimpleQueue(queue)
        queue.put(get_hostname())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_oom_canary()
    logging.warning("canary died")
    notify_oom(sys.argv[1], sys.argv[2])
