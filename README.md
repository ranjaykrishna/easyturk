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


## Easy Check to make sure everything is in place.

Run python in your terminal. Let's see if we can access your account information.
```
from amt import AMT
amt = AMT()
print(amt.get_account_balance())
```

This should print out how much balance you have left in your account. If you do not see the amount, then there setup was not successful.


## Launching an example image-captioning task on AMT.

Coming soon.

## Designing your own AMT task.

Coming soon.
