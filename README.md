# ESPHome for Sonoff Zigbee Bridge
ESPHome custom component and configuration for the Sonoff Zigbee Bridge with serial-over-tcp.
Allows you to use the ZBBridge with e.g. ZHA or Zigbee2MQTT, in the same way as [tasmota-zbbridge](https://zigbee.blakadder.com/Sonoff_ZBBridge.html).

Requires special firmware for the EFR32MG21 Zigbee chip to work: <https://github.com/arendst/Tasmota/tree/development/tools/fw_SonoffZigbeeBridge_ezsp>.

Loading the firmware onto the Zigbee chip is technically possible via ESPHome, by flipping GPIOs to put the chip into bootloader mode and uploading over tcp-serial. I will add more information about this later, but for now it's easiest to do this through Tasmota. Once the ZB firmware is flashed, it will stay like that regardless of the ESP firmware, so you can install ESPHome the normal way and it will use the up-to-date ZB firmware without issues.

Please note that, even though the concept of a Wifi-based serial-to-IP bridge sounds great, it is not without issues. A quote from [Zigbee2MQTT](https://www.zigbee2mqtt.io/information/supported_adapters.html):

> WiFi-based Serial-to-IP bridges are not recommended for Silicon Labs EZSP adapters as the serial protocol does not have enough fault-tolerance to handle packet loss or latency delays that can normally occur over WiFi connections. If cannot use a locally connected USB or UART/GPIO adapter then the recommendation is to use remote adapter that connected via Ethernet (wired) to avoid issues with EZSP caused by WiFi connections.

And some more discussion here: [Consider removing the ITEAD Sonoff ZBBridge from ZHA integration list of hardware as EZSP over WiFi-based bridges is often not stable #17170](https://github.com/home-assistant/home-assistant.io/issues/17170)

If anything, you need a _very_ stable Wifi connection, and even then, EZSP, the protocol used by the EFR32MG21 Zigbee chip, just isn't very suited to run over a Wifi connection. YMMV.

## How to use

- Put `sonoff_zbbridge.yaml` in your ESPHome configuration directory, alongside your other `.yaml` configuration files.
- Put the `custom_components/` directory with its contents in that same directory, so that you end up with:
```
my_esphome_configs/
├── custom_components/
│   ├── serial-server/
├── sonoff_zbbridge.yaml
├── my_other_esp.yaml
├── yet_another_esp.yaml
├── ...
```
- Edit `sonoff_zbbridge.yaml` as needed (Wifi credentials, etc.). By default, the configuration mirrors _tasmota-zbbridge_: same port, same baud rate, etc.
- Compile and upload as you normally would

## ZHA Configuration
- In Home Assistant, go to `Configuration > Integrations` and choose `ADD INTEGRATION`
- Scroll all the way down to select `Zigbee Home Automation`
- Select `Enter manually` as serial port
- Select _Radio Type_ `EZSP = Silicon Labs EmberZNet protocol:...`
- Set _Serial device path_ to `socket://[zbbridge_address]:[port]`, fill in appropriately (e.g. `socket://sonoff_zbbridge.local:8888`, `socket://10.0.0.11:4321`)
- Set _port speed_ to `115200` (this should be set according to the firmware present on your ZB chip, e.g. `ncp-uart-sw-6.7.8_115200.ota` -> `115200`)
- Set _data flow control_ to `software` (this should be set according to the firmware present on your ZB chip, e.g. `ncp-uart-sw-6.7.8_115200.ota` -> `sw`)
- Click `Submit` and if all goes well, you should see `Success!`

Note that ZHA does not add your device to Home Assistant through the ESPHome integration. A discovery notification should appear separately in HA, allowing you to add your Bridge as a regular ESPHome node. That way you can monitor it, add sensors like `status`, `wifi_status`, etc., like normal. This, however, is not _required_ for ZHA to function. If you decide not to add your device through the integration, be aware that ESPHome sets a reboot timer for 15 minutes by default, which will cause your device to [reboot automatically](https://esphome.io/components/api.html#configuration-variables) if `api:` was set in `sonoff_zbbridge.yaml` and no Home Assistant API connection was established. You can add `reboot_timeout: 0s` to the `api:` entry to prevent this behavior.

Credits to: [Oxan van Leeuwen](https://github.com/oxan) for the [original implementation](https://gist.github.com/oxan/4a1a36e12ebed13d31d7ed136b104959) and [tube0013](https://github.com/tube0013) for additional information.
