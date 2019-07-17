# EasyTurk: A easy to use wrapper to launch and get responses for custom Amazon Mechanical Turk tasks.

If you are using this repository for your research, please use the following citation:

```
@inproceedings{krishna2019easyturk,
  title={EasyTurk},
  author={Krishna, Ranjay},
  booktitle={GitHub},
  year={2019}
}
```

## Why should you use EasyTurk?

EasyTurk is meant for Amazon Mechanical Turk requestors who want to programmatically create, launch and retrieve Amazon Mechanical Turk microtasks. EasyTurk allows you to build custom html/javascript tasks and control your tasks using a easy python wrapper.


## Dependencies

EasyTurk requires jinja2 to compile your custom html and javascript tasks. It requires python2.7 or higher to use the API. It also requires that you have boto3 (AMT's python interface) installed.


## Installing EasyTurk

First let's install the code.
```
# Clone your repository.
git clone git@github.com:ranjaykrishna/easyturk.git
cd easyturk

# Create a virtualenv. You might want to use -p python3 option if you want to use EasyTurk with python 3. 
virtualenv env

# Activate your environment.
source env/bin/activate

# Install all the requirements.
pip install -r requirements
```


Now, let's install your AMT access keys.
```
aws configure --profile mturk
```

This will prompt you to enter your access key and secret key for your AMT account.
If you don’t have an AWS account already, visit [this website](https://aws.amazon.com) and create an account.
If you don’t have an MTurk Requester account already, visit [this website](https://requester.mturk.com) and create a new account.


## Easy Check to make sure everything is in place.

Run python in your terminal. Let's see if we can access your account information.
```
from amt import AMT
amt = AMT()
print(amt.get_account_balance())
```

This should print out how much balance you have left in your account. If you do not see the amount, then there setup was not successful.


## Launching an example image-captioning task on AMT.

In `templates/example.html`, there is an example image-captioning task I have already created for you. You can use that task as a reference to create your own task later. For now, let's try and see if we can render the task, launch it to AMT, then retrieve the results, and approve the assignment.

### Step 1: Render the task.
The following command should render the template you built. This should allow you to locally open the task in your browser and check to make sure the functionality works. Of course, when you press the submit button, nothing will happen as you are running the task locally. But once we launch this task on AMT, the submit button will pull the worker's responses to your task and send them to AMT. We will later be able to retrieve those results.
```
python scripts/render.py --template templates/example.html --output rendered_template.html
open rendered_template.html
```

### Step 2: Launching the task.
The following block of code will launch the task to AMT. We start by creating a list of image urls we want to caption. The example task expects the data to be in a list of objects, where each element in the list is a dictionary containing a `url` field. Once a worker finishes the task, the task will return a similar list, except each element will contain a `caption` field. Run the following in your python interpretor:
```
from interface import launch_example
data = [
           {
               'url': 'http://visualgenome.org/static/images/collect_sentences/dogs-playing.jpg',
           },
           {
               'url': 'http://visualgenome.org/static/images/collect_sentences/computer.png',
           }
       ]
hit_ids = launch_example(data, reward=1, tasks_per_hit=10)
print(hit_ids)
```
The above code will launch one HIT that will pay a reward of $1 and caption the two images in the list. Once the HIT is launched, it will return and print out the HITId. This HITId will be used to later retrieve and approve worker's responses. So make sure to NOT lose it. It's good practice to save your HITIds in a database or logfile. But if you do lose it, you can always get it back by queries for all the active HITs you have on AMT.

`launch_example` is a custom launch script that sets the title, description, keywords, tasks_per_hit fields. When you later write your own HIT, I recommend create a custom launch function like this one. You can see the source code for the function in `interface.py`.


### Step 3: Tracking your task's progress.


### Step 4: Retrieving worker responses.

### Step 5: Approving their work.

## Designing your own AMT task.

Coming soon.


## Contributing to this repository.

This wrapper is by no means a complete list of functionality offered by AMT. If you feel inclined to contribute and enable more functionality, please send me a message over email (firstnamelastname [at] gmail [dot] com) or twitter ([@RanjayKrishna](https://twitter.com/RanjayKrishna)). Feel free to also send me pull requests.
