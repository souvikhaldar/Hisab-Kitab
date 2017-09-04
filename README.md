This is an efficient expense journal application which lets you enlist your expenditures easily and consecutively draw critical insights enabling us to save in a better way.

"Money saved is money earned"

This is the principle that we have been following since ages but how efficiently we do it makes all the difference! Generally I’ve seen people write down their daily expenses in the pocket dairy to keep track of it. But is it a good way? Of course not!
Diary might get misplaced, writing down is troublesome, need to carry extra pen or pencil, need to calculate manually,organising issue and many more difficulties we face. So to beat these issues here is my app where you can easily insert your expenses (just like writing it down but without pencil or pen), edit them and at the end a given period of time (chosen by you) it will show the total expenditure, where maximum expense occurred and many more useful information.
All these information put together can even help you plan your budget well. Recognise the mistake in the pattern you spend and consecutively you’ll be able to rectify it and adopt a better budget plan. Hence, it will act as the saviour for the commoners by helping save their hard earned money!



# Quickstart - Build your own Docker image#

Build the Docker image using the following command

```bash
$ docker build -t python-flask:<tag> .
```

Run the Docker container using the command below.

```bash
$ docker run -d -p 8080:8080 python-flask:<tag>
```

# Quickstart - git based pipeline

Follow the steps mentioned below for git based pipeline

1. Ensure that you have a git project
2. Edit `app/src/server.py`
3. Commit your changes

    ```bash
    $ git add .
    $ git commit -m "message"
    ```

4. Push the changes to git

    ```bash
    $ git push <remote> master
    ```

# Advanced usage

### **Port**

Default Port for application is `8080` .

Application port can be changed by modifying the variable `bind` in  `app/conf/gunicorn_config.py` or setting Environment Variable

```python
bind = "0.0.0.0:" + os.environ.get("APP_PORT", "<NEW_PORT>")
```

```bash
$ docker run -d -p 8080:<NEW_PORT> python-flask:<tag>
```

### **Environment Variables**

* `APP_PORT` - Application port can also be specified by setting APP_PORT ENV

  ```bash
  $ docker run -d -p 8080:<NEW_PORT> -e APP_PORT='<NEW_PORT>' python-flask:<tag>
  ```
