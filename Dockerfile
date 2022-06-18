FROM public.ecr.aws/lambda/python:3.9

WORKDIR /tmp

# Install dependencies
# RUN pip install . rasterio==1.3a2 -t /var/task  --no-binary numpy,pydantic
RUN pip install rasterio==1.3a2  titiler==0.7.0 rio-tiler-pds==0.7.0 mangum==0.10  -t /var/task  --no-binary numpy,pydantic
COPY setup.py setup.py
COPY titiler_pds/ titiler_pds/
RUN pip install . -t /var/task  --no-binary numpy,pydantic

# Leave module precompiles for faster Lambda startup
RUN cd /var/task && find . -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[2-3][0-9]//'); cp $f $n; done;
RUN cd /var/task && find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN cd /var/task && find . -type f -a -name '*.py' -print0 | xargs -0 rm -f
RUN cd /var/task && find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf
RUN rm -rdf /var/task/numpy/doc/
RUN rm -rdf /var/task/stack
RUN du -h /tmp /var/task > /tmp/diskusage.txt && cat /tmp/diskusage.txt
