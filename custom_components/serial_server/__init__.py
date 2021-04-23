import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID, CONF_PORT

DEPENDENCIES = ['uart']

ns = cg.esphome_ns.namespace('serial_server')
cppclass = ns.class_('SerialServer', cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(cppclass),
    cv.Optional(CONF_PORT, default=8888): cv.port,
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    cg.add(var.set_port(config[CONF_PORT]))
    yield uart.register_uart_device(var, config)