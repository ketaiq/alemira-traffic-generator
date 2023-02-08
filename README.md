# alemira-test

## 1. Environment

Creating an environment
```sh
conda env create -f environment.yml
```

Start mongodb, see Mongo Express at http://localhost:8081
```sh
docker-compose up -d
```

Useful commands
```sh
conda env export --from-history > environment.yml
conda env update --file environment.yml  --prune
```

## 2. Quick Start

Start experiment
```sh
locust --config=app/locust.conf
```

Run `init_data.py` to initialize users and courses.

## 3. Configuration

The experiment is separated into 14 days. The first two days are considered as the first stage and the other days
are considered as the second stage. We use corresponding weights for different days and stages. So users should change weights and tasks in *InstructorUser* and *StudentUser* for different days of workload.

### Day 1

1. Set `InstructorUser.weight` as `weights.DAY_1_INSTRUCTOR_WEIGHTS`
2. Set `StudentUser.weight` as `weights.DAY_1_STUDENT_WEIGHTS`

### Day 2

1. Set `InstructorUser.weight` as `weights.DAY_2_INSTRUCTOR_WEIGHTS`
2. Set `StudentUser.weight` as `weights.DAY_2_STUDENT_WEIGHTS`

### Day 3 and other days

1. Set `InstructorUser.weight` as `weights.DAY_OTHER_INSTRUCTOR_WEIGHTS`
2. Set `StudentUser.weight` as `weights.DAY_OTHER_STUDENT_WEIGHTS`
3. Set `InstructorUser.tasks` as `generate_instructor_tasks(Stage.SECOND)`
4. Set `StudentUser.tasks` as `generate_student_tasks(Stage.SECOND)`

## 3. Resources

Courses from iCorsi3 history

Images from https://www.pexels.com/search/fruit/

Attachments from https://www.bbc.co.uk/learningenglish/punjabi/course/newsreview-2022/unit-1/downloads and https://www.sampletemplates.com/business-templates/plan-templates/sample-advertising-plan-pdf-word.html