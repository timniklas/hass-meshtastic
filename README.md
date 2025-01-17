# Meshtastic Integration for Home Assistant 🏠

[![GitHub Release](https://img.shields.io/github/v/release/timniklas/hass-meshtastic?sort=semver&style=for-the-badge&color=green)](https://github.com/timniklas/hass-meshtastic/releases/)
[![GitHub Release Date](https://img.shields.io/github/release-date/timniklas/hass-meshtastic?style=for-the-badge&color=green)](https://github.com/timniklas/hass-meshtastic/releases/)
![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/timniklas/hass-meshtastic/latest/total?style=for-the-badge&label=Downloads%20latest%20Release)
![HA Analytics](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.meshtastic.total&style=for-the-badge&label=Active%20Installations&color=red)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/timniklas/hass-meshtastic?style=for-the-badge)
[![hacs](https://img.shields.io/badge/HACS-Integration-blue.svg?style=for-the-badge)](https://github.com/hacs/integration)

## Overview

The Meshtastic Home Assistant Custom Integration allows you to integrate your local Meshtastic devices with your Home Assistant setup.

### Currently supported connection types
* TCP/IP

### Currently supported features
#### Sensors:
|Sensor|Unit|Example Value|Enabled by default|
|------|-------------|------|------|
|Battery|percent|80 %|yes|
|Operating voltage|volt|3.78 V|no|
|Channel utilization|percent|2.1%|no (debug information)|
|TX utilisation|percent|0.01%|no (debug information)|

#### Device tracker:
|Variable|Example Value|Enabled by default|
|-------------|-------------|------------------|
|latitude|59.340266|yes|
|longitude|-28.336112|yes|
|source_type|LOC_MANUAL|yes|

#### Notify:
|Notify|Enabled by default|
|------|------------------|
|Send private message|yes|

## Installation

### HACS (recommended)

This integration is available in HACS (Home Assistant Community Store).

1. Install HACS if you don't have it already
2. Open HACS in Home Assistant
3. Go to any of the sections (integrations, frontend, automation).
4. Click on the 3 dots in the top right corner.
5. Select "Custom repositories"
6. Add following URL to the repository `https://github.com/timniklas/hass-meshtastic`.
7. Select Integration as category.
8. Click the "ADD" button
9. Search for "meshtastic"
10. Click the "Download" button

### Manual

To install this integration manually you have to download [_meshtastic.zip_](https://github.com/timniklas/hass-meshtastic/releases/latest/) and extract its contents to `config/custom_components/meshtastic` directory:

```bash
mkdir -p custom_components/meshtastic
cd custom_components/meshtastic
wget https://github.com/timniklas/hacs_meshtastic/releases/latest/download/meshtastic.zip
unzip meshtastic.zip
rm meshtastic.zip
```

## Configuration

### Using UI

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=meshtastic)

From the Home Assistant front page go to `Configuration` and then select `Devices & Services` from the list.
Use the `Add Integration` button in the bottom right to add a new integration called `meshtastic`.

## Help and Contribution

If you find a problem, feel free to report it and I will do my best to help you.
If you have something to contribute, your help is greatly appreciated!
If you want to add a new feature, add a pull request first so we can discuss the details.

## Disclaimer

This custom integration is not officially endorsed or supported by meshtastic.
Use it at your own risk and ensure that you comply with all relevant terms of service and privacy policies.
