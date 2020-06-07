from task import Task

class Project:
    def __init__(self, project_name):
        self.__project_name = project_name
        self.__task = []
        self.__task_weight = []
        self.__task_progress = [0] * 100 #up to 100 tasks
        

    def add_task(self, task, weight):
        '''
        Add a task.
        Check that task is a Task type.
        task weight is a number between 0 and 100 to determine the relative weight of a task; weight will be used to calculate the project progress
        '''
        if not type(task) is Task:
            raise TypeError("Error")

        self.__task.append(task)
        self.__task_weight.append(weight)
            

    def set_task_progress(self, task_idx, progress):
        '''
        Set the progress of a task whose index in is task_idx.
        '''
        self.__task_progress[task_idx] = progress


    @property
    def progress(self):
        '''
        This 'property' shows the project progress according to task progress and relative weight of each task.
        The return value is between 0 and 100.
        '''
        weight_sum = 0
        product_sum = 0
        for i in range(len(self.__task)):
            weight_sum += self.__task_weight[i]
            product_sum += self.__task_weight[i]*self.__task_progress[i]
        project_progress = product_sum/weight_sum
        self.__project_progress = project_progress
        return project_progress


    def __str__(self):
        '''
        Return the project name, progress, and task list.
        '''
        return 'project name: {}\nprogress: {}\ntask list: {}'.format(self.__project_name,self.__project_progress,','.join(map(str,self.__task)).replace("/Defined",""))


if __name__ == "__main__":
    '''
    Write a short code here to test your class
    '''
    p1 = Project("project1")
    t1 = Task("task1")
    t2 = Task("task2")
    p1.add_task(t1,70)
    p1.add_task(t2,10)
    p1.set_task_progress(0,100)
    p1.set_task_progress(1,50)
    p1.progress
    print(p1) #project name: project1 \n progress: 93.75 \n task list: task1,task2