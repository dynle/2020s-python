TASK_INIT = 0 
TASK_STARTED = 1 
TASK_IN_PROGRESS = 2 
TASK_DONE = 3 
TASK_STATE_STR = ['Defined', 'Started', 'Progressing', 'Done']

class Task:
    def __init__(self, action, dependency=None):
        self.__action = action
        self.__state = TASK_INIT
        self.__progress = 0 # Integer between 0-100 is progress: done = 100
        self.__dependency = dependency # dependency is a task or None
        '''
        T1 Check that dependency, if not None, is an instance of Task
        '''
        if self.__dependency != None and not isinstance(self.__dependency,Task):
            raise TypeError("%s is not an instance of Task"%self.__dependency)        
    
    @property
    def state(self):
        return self.__state

    @property
    def progress(self):
        return self.__progress

    @progress.setter
    def progress(self, progress):
        '''
        T2 modify this method where state and progress follow these rules:
        1. state may only change from TASK_INIT to TASK_STARTED to TASK_IN_PROGRESS to TASK_DONE
        2. if task has a dependency, the state never changes from TASK_INIT unless the dependency state is TASK_DONE
        3. if state is TASK_INIT, the next state must be TASK_STARTED and progress is set to 0 regardless of the value of progress
        4. the value of progress must be non-decreasing
        5. if progress is 100, the state changes to TASK_DONE
        '''
        #the value of progress should be increased
        if self.__progress < progress:
            self.__progress = progress

        #if there is no dependency
        if not self.__dependency:
            if self.__state == TASK_INIT:
                self.__state = TASK_STARTED
                self.__progress = 0
            elif (self.__state == TASK_STARTED or self.__state == TASK_IN_PROGRESS) and self.__progress != 100:
                self.__state = TASK_IN_PROGRESS
            else:
                self.__state = TASK_DONE
        #if there is a dependency
        else:
            if self.__dependency.progress == 100:  
                if self.__state == TASK_INIT:
                    self.__state = TASK_STARTED
                    self.__progress = 0
                elif (self.__state == TASK_STARTED or self.__state == TASK_IN_PROGRESS) and self.__progress != 100:
                    self.__state = TASK_IN_PROGRESS
                else:
                    self.__state = TASK_DONE   


    def __str__(self):
        return '{}/{}'.format(self.__action, self.__progress if self.__state == TASK_IN_PROGRESS else TASK_STATE_STR[self.__state] )
    
if __name__ == "__main__":
    print('Basic task: task1')
    t1 = Task('task1')
    print(t1) # task1/Defined
    t1.progress = 0
    print(t1) # task1/Started
    t1.progress = 50
    print(t1) # task1/50
    t1.progress = 40
    print(t1) # task1/50
    t1.progress = 100
    print(t1) # task1/Done

    print('\nDependency: task3 depends on task2')
    t2 = Task('task2')
    t3 = Task('task3', t2)
    t3.progress = 0
    print(t3) # task3/Defined
    t2.progress = 10
    t2.progress = 100
    print(t2) # task2/Done
    t3.progress = 10
    print(t3) # task3/Started
    t3.progress = 60
    print(t3) #task3/60
    t3.progress = 100
    print(t3) #task3/Done
    


