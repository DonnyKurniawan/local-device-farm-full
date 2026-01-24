# Tiny Project for Device Farm
## Create Your Home Lab Server for Device Farm (and its cheap... hopefully)

This is an experimental project for creating Local Device Farm. Running on local PC as Device Farm Server. For now only supports Android Devices.

## Backend Done for BETA
- Upload APK to local servers storage
- Install APK to Devices
- Monitoring connected device
    
## Features in development backend and frontend
- Dashboard for Test Summary (Success rate, Failed, Need to Improve)
- Monitoring your Device Status 
- Device Controlling (Run Individualy, Run All)
- APK Versioning (Upload to Device Farm Server, APK Versioning)
- Discord Integration for webhook report
- Reporter file for test
- Log of previous run result

## Setup on my personal farm

Lenovo M715Q as Server
- [Ubuntu Server 24.04 LTS](https://ubuntu.com/download/server)
- AMD Ryzen 5 2400GE
- 8GB of RAM (2x 4GB DDR4)
- 256GB of SSD
- Wifi Network

## How to Run Backend
- instal venv

for windows user
go to directory folder using cmd. makesure you have python installed in your system
run by typing start_windows.cmd

for linux
- run this first chmod +x run_server.sh
- type linux.sh

## Tech Stack
- FastAPI
- Uvicorn

## Testing Device For Now

| Device | Specs |
| ------ | ------ |
| Tecno Pova 7 5G |  STOCK ROM |


## Screenshots
![Donny Kurniawan](/screenshoots/1.png)