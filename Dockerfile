FROM python:3.9-slim-buster AS base
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

FROM base AS code
COPY src /app
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

FROM code AS prod
EXPOSE 8501
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
