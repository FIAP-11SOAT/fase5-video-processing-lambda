FROM public.ecr.aws/lambda/python:3.12

RUN dnf install -y git gcc python3-devel \
    && dnf clean all \
    && rm -rf /var/cache/dnf /tmp/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY ./requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY src ${LAMBDA_TASK_ROOT}/src

ENV PYTHONPATH=$PYTHONPATH:${LAMBDA_TASK_ROOT}

CMD [ "src.auth_lambda.lambda_handler" ]
