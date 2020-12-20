FROM python:3.8-slim AS base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install poetry
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config --local virtualenvs.in-project true
RUN poetry install --no-dev


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

# Run the executable
ENTRYPOINT ["python", "-m", "bot_sylwester"]
CMD ["10"]
