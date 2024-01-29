ARG FUNCTION_DIR="/function"
ARG LAMBDA_TASK_ROOT="/function"

FROM python:3.11-bookworm as build-image
ARG FUNCTION_DIR
ARG LAMBDA_TASK_ROOT
WORKDIR ${FUNCTION_DIR}
RUN mkdir -p ${FUNCTION_DIR}
# ENV PIP_INDEX_URL=http://localhost:7070/root/pypi/+simple/
# ENV PIP_INDEX_URL=https://pypi.org/simple
# ENV PIP_EXTRA_INDEX_URL=http://localhost:7070/testuser/dev/

# COPY setup.py ${LAMBDA_TASK_ROOT}
COPY pyproject.toml README.md LICENSE ${LAMBDA_TASK_ROOT}
# COPY titiler_pds/ ${LAMBDA_TASK_ROOT}/titiler_pds/

# COPY rio_tiler-6.2.7a1-py3-none-any.whl rio_tiler_pds-0.10.1a2-py3-none-any.whl ${LAMBDA_TASK_ROOT}
# pip3 install . rasterio==1.3a2 -t ${LAMBDA_TASK_ROOT}
# Install dependencies
RUN echo FALSE pip3 install -t ${LAMBDA_TASK_ROOT} rio_tiler-6.2.7a1-py3-none-any.whl   rio_tiler_pds-0.10.1a2-py3-none-any.whl && \
    echo "=== rio_tiler-6.2.7a1-py3-none-any.whl DONE" && \
    echo pip3 install -t ${LAMBDA_TASK_ROOT} rio_tiler_pds-0.10.1a2-py3-none-any.whl && \
    echo "=== rio_tiler_pds-0.10.1a2-py3-none-any.whl DONE"

RUN pip3 install -t ${LAMBDA_TASK_ROOT} . --no-binary numpy,pydantic && \
    echo "Leave module precompiles for faster Lambda startup"

# RUN pip3 install tilebench -t ${LAMBDA_TASK_ROOT}
# RUN pip3 install rio_tiler_pds -t ${LAMBDA_TASK_ROOT}

RUN cd ${LAMBDA_TASK_ROOT} && find . -type f -name '*.pyc' | \
    while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-[2-3][0-9]//'); cp $f $n; done && \
    \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf && \
    cd ${LAMBDA_TASK_ROOT} && find . -type f -a -name '*.py' -print0 | grep -v handler.py | xargs -0 rm -f && \
    cd ${LAMBDA_TASK_ROOT} && find . -type d -a -name 'tests' -print0 | xargs -0 rm -rf && \
    rm -rdf ${LAMBDA_TASK_ROOT}/numpy/doc/ && \
    rm -rdf ${LAMBDA_TASK_ROOT}/stack

COPY titiler_pds/ ${LAMBDA_TASK_ROOT}/titiler_pds/

RUN pip install "uvicorn[standard]"
COPY .env ${LAMBDA_TASK_ROOT}/

# ENV AWS_PROFILE=default
ENV AWS_REQUEST_PAYER=requester
ENV AWS_DEFAULT_REGION=eu-north-1
ENV AWS_REGION=eu-north-1

# FROM python:3.11-slim-bookworm

# # Include global arg in this stage of the build
# ARG FUNCTION_DIR

# RUN mkdir -p ${FUNCTION_DIR}
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "titiler_pds.handler.handler" ]
