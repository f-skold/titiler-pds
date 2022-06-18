ARG FUNCTION_DIR="/function"
ARG LAMBDA_TASK_ROOT="/function"

FROM python:3.11-bookworm as build-image
ARG FUNCTION_DIR
ARG LAMBDA_TASK_ROOT
WORKDIR ${FUNCTION_DIR}
RUN mkdir -p ${FUNCTION_DIR}

# COPY setup.py ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}
COPY titiler_pds/ ${LAMBDA_TASK_ROOT}/titiler_pds/

# pip3 install . rasterio==1.3a2 -t ${LAMBDA_TASK_ROOT}
# Install dependencies
RUN pip3 install . -t ${LAMBDA_TASK_ROOT}  --no-binary numpy,pydantic && \
    echo "Leave module precompiles for faster Lambda startup"

RUN cd ${LAMBDA_TASK_ROOT} && find . -type f -name '*.pyc' | \
    while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[2-3][0-9]//'); cp $f $n; done && \
    \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf && \
    cd ${LAMBDA_TASK_ROOT} && find . -type f -a -name '*.py' -print0 | grep -v handler.py | xargs -0 rm -f && \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf && \
    rm -rdf ${LAMBDA_TASK_ROOT}/numpy/doc/ && \
    rm -rdf ${LAMBDA_TASK_ROOT}/stack

FROM python:3.11-slim-bookworm

# Include global arg in this stage of the build
ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "titiler_pds.handler.handler" ]
