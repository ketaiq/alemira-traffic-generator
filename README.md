# alemira-test

## 1. Environment

Exporting an environment file across platforms
```sh
conda env export --from-history > environment.yml
```

Creating an environment
```sh
conda env create -f environment.yml
```

Updating an environment
```sh
conda env update --file environment.yml  --prune
```

Start mongodb, see Mongo Express at http://localhost:8081
```sh
docker-compose up -d
```

## 2. Quick Start

Start experiment
```sh
sh start.sh
```

Clean up
```sh
sh cleanup.sh
```

## 3. Resources

Courses from https://waf.cs.illinois.edu/discovery/course-catalog.csv

Images from https://www.pexels.com/search/fruit/

Attachments from https://www.bbc.co.uk/learningenglish/punjabi/course/newsreview-2022/unit-1/downloads and https://www.sampletemplates.com/business-templates/plan-templates/sample-advertising-plan-pdf-word.html