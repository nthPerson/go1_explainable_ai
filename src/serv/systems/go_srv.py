from go import Go1
from services import ServiceNames, ServicePorts
from gen_srv import start_generic_server

if __name__ == "__main__":
    start_generic_server(ServiceNames.GO, ServicePorts[ServiceNames.GO], Go1)