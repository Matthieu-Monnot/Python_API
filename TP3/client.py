import grpc
import taskmanager_pb2
import taskm_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = taskm_pb2_grpc.TaskServiceStub(channel)
        response1 = stub.MoneyFlowClassique(taskmanager_pb2.MoneyFlowClassiqueRequest())
        print(f"La valeur de l'indicateur Money Flow Classique est: {response1.value}")
        response2 = stub.MoneyFlowTempore(taskmanager_pb2.MoneyFlowTemporeRequest())
        print(f"La valeur de l'indicateur Money Flow Tempore est: {response2.value}")
        response3 = stub.Rendement(taskmanager_pb2.RendementRequest())
        print(f"La valeur de l'indicateur Rendement est: {response3.value}")
        response4 = stub.Vwap(taskmanager_pb2.VwapRequest())
        print(f"La valeur de l'indicateur VWAP est: {response4.value}")
        response5 = stub.Twap(taskmanager_pb2.TwapRequest())
        print(f"La valeur de l'indicateur TWAP est: {response5.value}")


if __name__ == '__main__':
    run()
