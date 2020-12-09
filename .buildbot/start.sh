rm master/twistd.log
rm worker/twistd.log
export $(grep -v '^#' .env | xargs)
buildbot start master
buildbot-worker start worker

