FROM python@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea
RUN pip install --no-cache-dir numpy==2.5.3 pandas==3.0.5 scikit-learn==1.9.1 scipy==1.18.1 joblib==1.6.0 threadpoolctl==3.6.0
ENV PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
WORKDIR /tmp
USER 65534:65534

