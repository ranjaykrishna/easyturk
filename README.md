# EasyTurk: A Wrapper for Custom AMT Tasks

EasyTurk is an easy to use wrapper to launch and get responses for custom Amazon Mechanical Turk tasks.

If you are using this repository for your research, please use the following citation:

```
@misc{krishna2019easyturk,
  author = {Krishna, Ranjay},
  title = {EasyTurk: A Wrapper for Custom AMT Tasks},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ranjaykrishna/easyturk}}
}
```

#### Why should you use EasyTurk?

EasyTurk is meant for Amazon Mechanical Turk requestors who want to programmatically create, launch and retrieve Amazon Mechanical Turk microtasks. EasyTurk allows you to build custom html/javascript tasks and control your tasks using an easy python wrapper.


#### Dependencies

EasyTurk requires jinja2 to compile your custom html and javascript tasks. It requires python2.7 or higher to use the API. It also requires that you have boto3 (AMT's python interface) installed.


## Installing EasyTurk

First let's install the code.
```
# Clone the repository.
git clone git@github.com:ranjaykrishna/easyturk.git
cd easyturk

# Create a virtual environment.
# You might want to use -p python3 option 
# if you want to use EasyTurk with python 3. 
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


#### Easy check to make sure everything is in place.

Run python in your terminal. Let's see if we can access your account information.
```
from easyturk import EasyTurk
et = EasyTurk(sandbox=False)
print(et.get_account_balance())
```
This should print out how much balance you have left in your account. If you do not see the amount, then there setup was not successful.

#### Example tasks that you can use out of the box:

1. Image captioning: `easyturk/templates/write_caption.html` contains a image captioning task where workers are asked to write captions for each image.
2. Verification: `easyturk/templates/verify_caption.html` contains a verification task that asks users to verify that a certain caption is correct for a given image.
3. Bounding box: `easyturk/templates/annotate_bbox.html` contains a bounding box task that asks users to annotate multiple objects per image.
3. Verify bounding box: `easyturk/templates/verify_bbox.html` contains a bounding box task that asks users verify whether a bounding box has been annotated correctly.
4. Verify visual relationships: `easyturk/templates/verify_relationship.html` contains a task that asks users to verify whether a visual relationship has been annotated correctly.

In the remainer of this tutorial, we will explain how you can launch the captioning task and how you can create your own tasks. The same workflow can be used for the other tasks as well.


## Launching an example image-captioning task on AMT.

In `easyturk/templates/write_caption.html`, there is an example image-captioning task I have already created for you. You can use that task as a reference to create your own task later. For now, let's try and see if we can render the task, launch it to AMT, then retrieve the results, and approve the assignment.

#### Step 1: Render the task.
The following command should render the template you built. This should allow you to locally open the task in your browser and check to make sure the functionality works. Of course, when you press the submit button, nothing will happen as you are running the task locally. But once we launch this task on AMT, the submit button will pull the worker's responses to your task and send them to AMT. We will later be able to retrieve those results.
```
python easyturk/render.py --template write_caption.html --output rendered_template.html
open rendered_template.html
```

#### Step 2: Launching the task.
The following block of code will launch the task to AMT. We start by creating a list of image urls we want to caption. The example task expects the data to be in a list of objects, where each element in the list is a dictionary containing a `url` field. Once a worker finishes the task, the task will return a similar list, except each element will contain a `caption` field. Run the following in your python interpretor:
```
from easyturk import interface
data = [
           {
               'url': 'http://visualgenome.org/static/images/collect_sentences/dogs-playing.jpg',
           },
           {
               'url': 'http://visualgenome.org/static/images/collect_sentences/computer.png',
           }
       ]
hit_ids = interface.launch_caption(data, reward=1, tasks_per_hit=10)
print(hit_ids)
```
The above code will launch one HIT that will pay a reward of $1 and caption the two images in the list. Once the HIT is launched, it will return and print out the HITId. This HITId will be used to later retrieve and approve worker's responses. So make sure to NOT lose it. It's good practice to save your HITIds in a database or logfile. But if you do lose it, you can always get it back by queries for all the active HITs you have on AMT.

`launch_caption` is a custom launch script that sets the title, description, keywords, tasks_per_hit fields. When you later write your own HIT, I recommend create a custom launch function like this one. You can see the source code for the function in `easyturk/interface.py`.


#### Step 3: Tracking your task's progress.
You can query for your HIT's progress with the following:
```
from easyturk import EasyTurk
et = EasyTurk(sandbox=False)
progress = et.show_hit_progress(hit_ids)
print(progress[hit_ids[0]])
```
The above will print out the progress made for the first HIT in the list. It should print something like:
```
{'completed': 0, 'max_assignment': 1}
```


#### Step 4: Retrieving worker responses.
You can retrieve the work done by workers for the submitted assignments to a HIT using the following code:
```
from easyturk import interface

# approve is set to False because right now we are only fetching the results. You can set it to True to auto-approve the assignments.
results = interface.fetch_completed_hits(hit_ids, approve=False)
print(results[hit_ids[0]])
```
The above code will parse out the responses made by the worker and show you something like the following:
```
[
    {
       'url': 'http://visualgenome.org/static/images/collect_sentences/dogs-playing.jpg',
       'caption': 'Two dogs playing with a stick.'
    },
    {
       'url': 'http://visualgenome.org/static/images/collect_sentences/computer.png',
       'caption': 'A cluttered room',
    }
]
```

#### Step 5: Approving their work.
If you are happy with the work, you can approve and pay your workers by issuing the following command:
```
from easyturk import EasyTurk
et = EasyTurk(sandbox=False)
for hit_id in hit_ids:
    et.approve_hit(hit_id)
```

## Designing your own AMT task.
The best way to learn to create your own tasks is to mimic the high level interface of `easyturk/templates/write_caption.html`. The main contraint to adhere to is making sure that you are using the API provided by `easyturk/templates/easyturk.html`. Currently, EasyTurk assumes that all your tasks you design will reside in one single HTML files in the `easyturk/templates/` directory


#### Importing EasyTurk into your custom task.
Simply add the following line before your custom javascript to use the EasyTurk API:
```
{% include "easyturk.html" %}
```

#### Loading the data from EasyTurk.
The task contains a `DEFAULT_INPUT` variable that should be set when designing your task such that it follows the input schema you expect. In our example captioning task, that variable is a random list of image urls. It allows us to render and test the functionality of the task locally before launching it. When launched, make sure to call:
```
var input = easyturk.getInput(DEFAULT_INPUT);
```
This API call will update the input variable with the actual input for the given task. So, each worker will see a specific input, based on the `data` variable you set in Step 2 above.

#### Enabling the task.
The following API call allows workers to preview the HIT without being able to submit it. Make sure to include it so that when the HIT is accepted by a worker, the task will be enabled.
```
if (!easyturk.isPreview()){
    enableTask();
}
```

#### Setup submission and submit.
To make sure that the task is submittable, keep the `enableTask()` function and make sure it includes the `easyturk.setupSubmit()` call and the `easyturk.setOutput(output)` calls within.  Any python object you set the `output` variable to will be the response you get back from the worker.

#### Overall.
When making your custom task, make sure to import EasyTurk's APIs. Get the input from EasyTurk, enable the hit, setup submission and then set the output that you want returned to you. It's easy!


#### More customization.
There is a lot more you can do. Check out the fully documented code in `easyturk.py`. There are more complicated workflows you can create by using those functions. Have fun.


## Contributing to this repository.

This wrapper is by no means a complete list of functionality offered by AMT. If you feel inclined to contribute and enable more functionality, please send me a message over email (firstnamelastname [at] gmail [dot] com) or twitter ([@RanjayKrishna](https://twitter.com/RanjayKrishna)). Feel free to also send me pull requests.
