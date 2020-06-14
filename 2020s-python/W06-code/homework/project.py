import pickle
from task import Task

class Project:
    def __init__(self, project_name):
        self.__project_name = project_name
        self.__task = []
        self.__task_weight = []

    def add_task(self, task, weight):
        '''
        Add a task.
        Check that task is a Task type.
        task weight is a number between 0 and 100 to determine the relative weight of a task; weight will be used to calculate the project progress
        '''
        if task and not type(task) is Task:
            raise TypeError('task is wrong type')
        if not (weight > 0 and weight <= 100):
            raise TypeError('weight is wrong')
        self.__task.append(task)
        self.__task_weight.append(weight)

    def set_task_progress(self, task_idx, progress):
        '''
        Set the progress of a task whose index in is task_idx.
        '''
        self.__task[task_idx].progress = progress
        pass

    @property
    def progress(self):
        '''
        This 'property' shows the project progress according to task progress and relative weight of each task.
        The return value is between 0 and 100.
        '''
        project_progress = 0
        task_total_weight = 0
        for i,t in enumerate(self.__task):
            project_progress += t.progress*self.__task_weight[i]
            task_total_weight += self.__task_weight[i]

        return project_progress/task_total_weight

    def __str__(self):
        '''
        Return the project name, progress, and task list.
        '''
        return "project name: %s\nprogress: %s\ntask list: %s\n"%(self.__project_name,self.progress,','.join(map(str, self.__task)))
    
    def save(self, filename = None):
        if filename:
            self.__filename = filename
        with open(self.__filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self, filename = None):
        if filename:
            self.__filename = filename
        with open(self.__filename, 'rb') as f:
            loaded_path = pickle.load(f)
            if not type(loaded_path) is Project:
                raise TypeError('loaded object is not a Project')

if __name__ == "__main__":
    pa = Project('Project A')

    t1 = Task('T1')
    t2 = Task('T2', t1)
    t3 = Task('T3')

    pa.add_task(t1, 100)
    pa.add_task(t2, 100)
    pa.add_task(t3, 50)

    pa.set_task_progress(0, 0)
    pa.set_task_progress(0, 50)
    pa.set_task_progress(0, 100)
    # print(pa)
    
    pa.set_task_progress(1, 0)
    pa.set_task_progress(1, 50)
    pa.set_task_progress(1, 100)
    # print(pa)
    
    pa.set_task_progress(2, 0)
    pa.set_task_progress(2, 50)
    pa.set_task_progress(2, 100)
    # print(pa)

    
    # pa.save("project_test.pck")

