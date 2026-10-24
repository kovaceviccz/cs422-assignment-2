FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl fonts-dejavu-core python3 python3-pip python3-venv xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/typst/typst/releases/download/v0.14.2/typst-x86_64-unknown-linux-musl.tar.xz \
    -o /tmp/typst.tar.xz \
    && tar -xJf /tmp/typst.tar.xz -C /tmp \
    && install /tmp/typst-x86_64-unknown-linux-musl/typst /usr/local/bin/typst \
    && rm -rf /tmp/typst.tar.xz /tmp/typst-x86_64-unknown-linux-musl

WORKDIR /work
COPY requirements.txt .
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PATH="/opt/venv/bin:$PATH" HOME=/tmp MPLCONFIGDIR=/tmp/matplotlib
CMD ["python3", "assignment2.py", "listed_iperf3_servers.json"]
