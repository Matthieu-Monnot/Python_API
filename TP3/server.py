from concurrent import futures
import grpc
import taskmanager_pb2
import taskm_pb2_grpc


class TaskService(taskm_pb2_grpc.TaskServiceServicer):
    def MoneyFlowClassique(self, request, context):
        value = 0
        return taskmanager_pb2.AddTaskResponse(value=value)

    def MoneyFlowTempore(self, request, context):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'description': request.description,
            'completed': False
        }
        return taskmanager_pb2.AddTaskResponse(success=True, id=task_id)

    def Rendement(self, request, context):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'description': request.description,
            'completed': False
        }
        return taskmanager_pb2.AddTaskResponse(success=True, id=task_id)

    def Vwap(self, request, context):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'description': request.description,
            'completed': False
        }
        return taskmanager_pb2.AddTaskResponse(success=True, id=task_id)

    def Twap(self, request, context):
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'description': request.description,
            'completed': False
        }
        return taskmanager_pb2.AddTaskResponse(success=True, id=task_id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    taskm_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
