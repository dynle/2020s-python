import argparse
import pickle
from task import Task
from project import Project


parser = argparse.ArgumentParser()

parser.add_argument("-ap","--add_project",help="Add a project",type=str)
parser.add_argument("-a","--add",help="Add a task (task, weight)",nargs=2)
parser.add_argument("-ad","--add_dependency",help="Add a task with dependency (task, weight, dependency",nargs=3)
parser.add_argument("-s","--set_progress",help="Set progress of a task (task_idx, progress)",nargs=2,type=int)
parser.add_argument("-p",'--pathfile', help='Pickle file for path')

args = parser.parse_args()

if args.add_project:
    new_project = Project(args.add_project)
    new_project.save("%s.pck"%args.add_project)

else:
    try:
        with open(args.pathfile,"rb+") as f:
            this_project = pickle.load(f)

    except FileNotFoundError:
        print("Non existing file")
        exit()

    if not args.add is None:
        this_task = args.add
        this_task[0] = Task(this_task[0].upper())
        this_project.add_task(this_task[0],int(this_task[1]))
        this_project.save()

    if not args.add_dependency is None:
        this_task = args.add_dependency
        this_task[2] = Task(this_task[2].upper())
        this_task[0] = Task(this_task[0].upper(),this_task[2])
        this_project.add_task(this_task[0],int(this_task[1]))
        this_project.save()

    if not args.set_progress is None:
        this_set = args.set_progress
        this_project.set_task_progress(this_set[0],this_set[1])
        this_project.save()

    print(this_project)
