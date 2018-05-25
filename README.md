# HyperGrid Tools & Quick Start Guides

# HyperCloud Portal Automated System Settings Tool

This tool will read from a file, systemSettings.txt, and apply those to a running HyperCloud instance for reliable and programmatic configuration. 

Populate the values in systemSettings.txt and execute the script with the username, password, and instance IP. 

`./setSystemSettings.sh admin@hypercloud.io admin123 10.0.8.47`

Currently supported configuratino fields:

* RabbitMQ IP
* RabbitMQ Port
* Linux Agent Location
* Windows Agent Location
* Proxy Location
* UI Custom Title

### Demo

![demo video](https://raw.githubusercontent.com/mascij/HyperCloud-AutoSystemSettings/master/demo.gif)

# HyperGrid Blueprint Backup Tool

This is an easy tool for backing up your library of Blueprints from HyperCloud Portal. It will download all entitled Blueprints for the user, date/time stamp and store them for future import.

Clone the repo & run:

`./BackupBlueprints.sh <username> <password> <url body for HyperCloud Portal>`
  
For example:

`./BackupBlueprints.sh admin@tenant.com password myurl.com`

### Demo

![alt text](https://raw.githubusercontent.com/mascij/hypergrid-blueprint-backup/master/Blueprintbackup.gif)

# HyperGrid API Quick Start Guide

### Simple Steps to Begin using the REST API in Minutes

This document provides a quick start guide for implementing the HyperGrid API. 

It will allow users to begin interfacing with the HyperCloud API for automation, practical scripting, and reporting within hours and not days. 

In addition to providing foundational background it includes practical samples, and simple cut & paste command line examples to enable users to quickly interface with the API. 

This document will cover:

* Authentication with the APIs
* Provisioning applications and VMs through the API
* Fetching data in a clean and easily manageable format
    o Searching through results to collect & return individual values 
