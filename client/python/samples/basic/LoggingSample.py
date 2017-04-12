from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from modeldb.thrift.modeldb import ModelDBService

# create connection to thrift client
host = "localhost"
port = 6543
transport = TSocket.TSocket(host, port)
# Buffering is critical. Raw sockets are very slow
transport = TTransport.TFramedTransport(transport)
# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)
# Create a client to use the protocol encoder
client = ModelDBService.Client(protocol)
transport.open()


# get relevant project ids with case insensitive keys and case sensitive values
projectIds = client.getProjectIds({'author':'test_user'})
# update projects
for projectId in projectIds:
    client.updateProject(projectId, 'name', "Sample Logging Project")

# get all model ids
allModelIds = client.getModelIds({})
# get relevant model ids with case sensitive key-value pairs
modelIds = client.getModelIds({'TAG':'train', 'TYPE':'Normal distributions'})
# create and update fields of models
for modelId in modelIds:
    # update scalar fields with string values
    client.updateField(modelId, 'PATH', 'new/path/to/model')
    # create vector fields in nested locations using mongodb's dot notation
    # e.g. model[CONFIG][values] = []
    vectorConfig = {} # specify configurations for the vector (this is non-functional for now)
    client.createVector(modelId, 'CONFIG.values', vectorConfig)
    # append to vector fields
    values = ['value1', 'value2', 'value3']
    for i in xrange(len(values)):
        client.addToVectorField(modelId, 'CONFIG.values', values[i])
    # update vector fields at a specific index
    client.updateField(modelId, 'CONFIG.values.0', 'new value')
    # update fields nested within vectors
    client.updateField(modelId, 'METRICS.0.TYPE', 'accuracy')


# close thrift client
transport.close()
