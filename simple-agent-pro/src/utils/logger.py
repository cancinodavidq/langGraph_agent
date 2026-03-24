# src/utils/logger.py

import logging

# 1. Formato de cada línea
FORMAT = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)

# 2. Crear el logger principal del proyecto
logger = logging.getLogger("simple-agent")
logger.setLevel(logging.DEBUG)

# 3. Handler para pantalla
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# 4. Handler para archivo
file_handler = logging.FileHandler("agent.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# 5. Agregar handlers al logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
