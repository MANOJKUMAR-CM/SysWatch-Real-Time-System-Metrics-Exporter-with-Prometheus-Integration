# 🖥️ SysWatch: Real-Time System Metrics Exporter with Prometheus Integration

SysWatch is a lightweight Python-based metrics exporter designed to provide **real-time monitoring of Linux system performance**. It collects essential **CPU**, **memory**, and **disk I/O** statistics using native system tools like `iostat` and `/proc/meminfo`, and exposes them through a Prometheus-compatible `/metrics` endpoint for seamless integration with **Prometheus** and **Grafana**.

---

## 🚀 Features

- 📡 **Prometheus-Compatible Exporter**
- 📊 **Live CPU Usage** by mode (user, system, idle, etc.)
- 💾 **Disk I/O Stats** (read/write rate, IOPS, bytes transferred)
- 🧠 **Memory Metrics** from `/proc/meminfo`
- 📝 **Structured Logging** to `pipeline.log`
- ⏱️ **Custom Scrape Interval Support**
- ⚙️ **Simple, Extensible Python Codebase**

---

## ⚙️ How It Works

SysWatch gathers system metrics using:

- `iostat`: For disk I/O and CPU stats
- `/proc/meminfo`: For real-time memory usage
- `prometheus_client`: To expose metrics on a custom HTTP server

All metrics are available on `http://localhost:18000/metrics` and can be scraped by Prometheus every few seconds.

---
