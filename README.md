# alemira-test

## 1. Environment

Install conda and docker

Install chrome if you want to run it on Linux
```
curl -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
sudo apt install google-chrome-stable
```

Create an environment
```sh
conda env create -f environment.yml
```

Activate conda environment
```sh
conda activate alemira
```

Start mongodb, see Mongo Express at http://localhost:8081
```sh
docker compose up -d
```

Change open file limit
```sh
ulimit -Sn 20000
```

Useful commands
```sh
conda env export --from-history > environment.yml
conda env update --file environment.yml  --prune
```

## 2. Quick Start

Step 1: initialize users and courses
```sh
nohup python -m app.utils.data_sync_init &
```

Step 2: start experiment
```sh
nohup locust --config=app/locust.conf &
```

Step 3: restart deployments
```sh
kubectl rollout restart deploy -n alms
```

## 3. Configuration

The experiment is separated into 14 days. The first two days are considered as the first stage and the other days
are considered as the second stage. We use corresponding weights for different days and stages. So users should change weights and tasks in *InstructorUser* and *StudentUser* for different days of workload. To do this, you can simply modify `EXPT_CONFIG` and `WORKLOAD_FILE`
in `locustfile.py`.

The desired configuration is:
| Week | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |
| ---- | ------ | ------- | --------- | -------- | ------ | -------- | ------ |
|   1  | DAY_1  |  DAY_2  | DAY_OTHER | DAY_OTHER|DAY_OTHER|DAY_OTHER|DAY_OTHER|
|   2  |DAY_OTHER|DAY_OTHER|DAY_OTHER | DAY_OTHER|DAY_OTHER|DAY_OTHER|DAY_OTHER|

## 3. Resources

Courses from iCorsi3 history