# ESPHome-zbbridge
ESPHome custom component and configuration for the Sonoff Zigbee Bridge with serial-over-tcp.
Allows you to use the ZBBridge with e.g. ZHA or Zigbee2MQTT, in the same way as [tasmota-zbbridge](https://zigbee.blakadder.com/Sonoff_ZBBridge.html).

Requires special firmware for the EFR32MG21 Zigbee chip to work: <https://github.com/arendst/Tasmota/tree/development/tools/fw_SonoffZigbeeBridge_ezsp>.
Loading the firmware onto the Zigbee chip is technically possible via esphome, by flipping GPIOs to put the chip into bootloader mode and upload over tcp-serial. I will add more information about this later, but for now it's easiest to do this through Tasmota. Once the ZB firmware is flashed, it will stay like that regardless of the ESP firmware, so you can install ESPHome the normal way and it will use the up-to-date ZB firmware without issues.

Please note that, even though the concept of a Wifi-based serial-to-IP bridge sounds great, it is not without issues. A quote from [Zigbee2MQTT](https://www.zigbee2mqtt.io/information/supported_adapters.html):

> WiFi-based Serial-to-IP bridges are not recommended for Silicon Labs EZSP adapters as the serial protocol does not have enough fault-tolerance to handle packet loss or latency delays that can normally occur over WiFi connections. If cannot use a locally connected USB or UART/GPIO adapter then the recommendation is to use remote adapter that connected via Ethernet (wired) to avoid issues with EZSP caused by WiFi connections.

If anything, you need a _very_ stable Wifi connection, and even then, EZSP, the protocol used by the EFR32MG21 Zigbee chip, just isn't very suited to run over a Wifi connection. YMMV.
