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
