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

## 3. Resources

Courses from iCorsi3 history

Images from https://www.pexels.com/search/fruit/

Attachments from https://www.bbc.co.uk/learningenglish/punjabi/course/newsreview-2022/unit-1/downloads and https://www.sampletemplates.com/business-templates/plan-templates/sample-advertising-plan-pdf-word.html