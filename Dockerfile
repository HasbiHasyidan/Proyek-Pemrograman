# Gunakan base image Airflow
FROM apache/airflow:2.7.0-python3.9

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH=$AIRFLOW_HOME/dags

# Install dependensi tambahan (pandas, dll.)
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

USER airflow
RUN pip install --no-cache-dir pandas

# Copy DAGs ke folder Airflow
COPY dags/ $AIRFLOW_HOME/dags/

# Jika ada file data, copy ke container
COPY data/ $AIRFLOW_HOME/data/

# Pastikan Airflow menggunakan folder data yang benar
RUN mkdir -p $AIRFLOW_HOME/data && chmod -R 755 $AIRFLOW_HOME/data

# Expose port default Airflow
EXPOSE 8080

# Inisialisasi database Airflow
RUN airflow db init

# Masukkan command default untuk menjalankan standalone Airflow
CMD ["airflow", "standalone"]
