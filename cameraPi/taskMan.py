import xmlrpclib
import supervisor.xmlrpc


class TaskManager(object):
    def __init__(self):
        # supervisor has it's xmlrpc interface setup on a unix socket at
        # /var/run/supervisor.sock
        self.proxy = xmlrpclib.ServerProxy(
            'http://127.0.0.1',
            transport=supervisor.xmlrpc.SupervisorTransport(
                None,
                None,
                serverurl='unix://' + '/var/run/supervisor.sock'
            )
        )

    @property
    def supervisor_state(self):
        return self.proxy.supervisor.getState()

    def get_info(self, name=None):
        if name is None:
            process_info = self.xmlrpc.supervisor.getAllProcessInfo()
        else:
            process_info = self.xmlrpc.supervisor.getProcessInfo(name)

        return process_info

    def start(self, name):
        return self.xmlrpc.supervisor.startProcess(name)

    def stop(self, name):
        return self.xmlrpc.supervisor.stopProcess(name)
