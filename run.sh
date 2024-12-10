# usage: GOOGLE_CLOUD_PROJECT=XXXXX bash run.sh

docker build -t cloud-profiler-python-example:latest --platform=linux/amd64 --build-arg GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT .
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py sleep
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py python
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py native
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py thread
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py async
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py gc
docker run --rm -v ~/.config/gcloud:/root/.config/gcloud cloud-profiler-python-example:latest python main.py digest
