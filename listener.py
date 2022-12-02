#python snmp trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from config import LISTENER_IP, LISTENER_PORT
from actions.windows_machine import execute_shutdown



def listerner_func(*args, **kwagrs):
    print(f"Trap recieved as (*args, **kwagrs) len: {len(args)} {len(kwagrs)}")
    # print(f"Trap recieved as (*args, **kwagrs) --- {args} {kwagrs}")

    # #args available variables as: 
    # snmpEngine, contextEngineId, contextName, varBinds, self.__cbCtx
    # snmpEngine, stateReference, contextEngineId, contextName, varBinds, self.__cbCtx
    
    # taking 4 variable to explore
    varBinds = args[3]
    mapper = {}
    for key, val in varBinds:        
        print('%s = %s' % (key.prettyPrint(), val.prettyPrint()))
        mapper[key.prettyPrint()] = val.prettyPrint()

    if mapper.get("1.3.6.1.6.3.1.1.4.1.0"):
        # checking for specific key and value
        # check as per your request
        # from pysnmp.proto.rfc1902 import ObjectName
        # from pyasn1.type.univ import ObjectIdentifier
        ###### upsTrapsOnBattery
        # Trap recieved as (*args, **kwagrs) len: 5 0
        # 1.3.6.1.2.1.1.3.0 = 0
        # 1.3.6.1.6.3.1.1.4.1.0 = 1.3.6.1.4.1.935
        # 1.3.6.1.2.1.33.1.2.3.0 = 0
        # 1.3.6.1.2.1.33.1.2.2.0 = 0
        # 1.3.6.1.2.1.33.1.9.7.0 = 0
        ###### lowBattery
        # Trap recieved as (*args, **kwagrs) len: 5 0
        # 1.3.6.1.2.1.1.3.0 = 0
        # 1.3.6.1.6.3.1.1.4.1.0 = 1.3.6.1.4.1.935.0.7
        # 1.3.6.1.6.3.18.1.3.0 = 127.0.0.1
        # 1.3.6.1.6.3.18.1.4.0 = public
        # 1.3.6.1.6.3.1.1.4.3.0 = 1.3.6.1.4.1.935
        if mapper.get("1.3.6.1.6.3.1.1.4.1.0") == "1.3.6.1.4.1.935.0.7":
            print(f"======================================")
            print(f"calling handler function for this case")
            execute_shutdown()



class SNMPListener:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.engine = self.initialize()
    
    def initialize(self):
        snmpEngine = engine.SnmpEngine()
        config.addTransport(
            snmpEngine,
            udp.domainName + (1,),
            udp.UdpTransport().openServerMode((self.ip, self.port))
        )
        config.addV1System(snmpEngine, 'my-test', 'public')
        ntfrcv.NotificationReceiver(snmpEngine, cbFun=listerner_func)
        return snmpEngine

    def run(self):
        self.engine.transportDispatcher.jobStarted(1) 
        try:
            self.engine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt as exc:
            print(f"Existing...")
        except Exception as exc:
            self.engine.transportDispatcher.closeDispatcher()
            raise exc




if __name__ == '__main__':
    print(f"--------------------------------------------")
    print(f"Trap listener started on {LISTENER_IP}:{LISTENER_PORT}")
    print(f"...")
    l = SNMPListener(LISTENER_IP, LISTENER_PORT)
    l.run()

