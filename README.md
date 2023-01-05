# kxi-microservices-data-services
- [kxi-microservices-data-services](#kxi-microservices-data-services)
  - [Architecture](#architecture)
  - [Quick Links](#quick-links)
  - [Prerequisites](#prerequisites)
  - [Features](#features)
  - [Get started](#get-started)

## Architecture
![Architecture](img/arch_diagram.png)

## Quick Links
* [Microservices](https://code.kx.com/insights/microservices)
  * [Storage Manager](https://code.kx.com/insights/microservices/storage-manager/introduction.html)
  * [Data Access](https://code.kx.com/insights/microservices/data-access/introduction.html)
  * [Service Gateway](https://code.kx.com/insights/microservices/data-access/introduction_sg.html)
  * [Stream Processor](https://code.kx.com/insights/microservices/stream-processor/index.html)

## Prerequisites
* Valid kdb license including feature flags
* Access to KX Docker repo ([nexus.dl.kx.com](https://nexus.dl.kx.com) / [registry.dl.kx.com](registry.dl.kx.com))
* [PyKX](https://code.kx.com/pykx) installed

## Features
This application demonstrates how you can use kdb Insights Microservices to do the following:

- Create a data ingestion pipeline using python code subscribing to Kafka topics.
- Write and query data in q.
- Write and query data in Python.
- Generate data visualizations in Jupyter Notebooks.

## Get started
Choose you preferred orchestration:
* [Docker](docker)
* [Kubernetes](kubernetes)