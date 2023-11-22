import grpc
import taskmanager_pb2
import taskm_pb2_grpc


def display_menu():
    print("1. Money Flow Classique")
    print("2. Money Flow Tempore")
    print("3. Rendement")
    print("4. VWAP")
    print("5. TWAP")
    print("0. Quitter")


def run():
    symbol = 'BTCUSDT'
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = taskm_pb2_grpc.TaskServiceStub(channel)

        while True:
            display_menu()
            user_choice = input("Choisissez une option (0-5): ")

            if user_choice == '0':
                print("Au revoir!")
                break
            elif user_choice == '1':
                response = stub.MoneyFlowClassique(taskmanager_pb2.MoneyFlowClassiqueRequest())
                print(f"La valeur de l'indicateur Money Flow Classique est: {response.value}")
            elif user_choice == '2':
                response = stub.MoneyFlowTempore(taskmanager_pb2.MoneyFlowTemporeRequest())
                print(f"La valeur de l'indicateur Money Flow Tempore est: {response.value}")
            elif user_choice == '3':
                response = stub.Rendement(taskmanager_pb2.RendementRequest())
                print(f"La valeur de l'indicateur Rendement est: {response.value}")
            elif user_choice == '4':
                response = stub.Vwap(taskmanager_pb2.VwapRequest())
                print(f"La valeur de l'indicateur VWAP est: {response.value}")
            elif user_choice == '5':
                response = stub.Twap(taskmanager_pb2.TwapRequest())
                print(f"La valeur de l'indicateur TWAP est: {response.value}")
            else:
                print("Option invalide. Veuillez choisir une option valide.")


if __name__ == '__main__':
    run()
