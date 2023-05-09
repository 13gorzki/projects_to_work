import logging


def write_log(file_name, level, message):
    logger = logging.getLogger(file_name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )  # Ustawienia loggera

    file_handler = logging.FileHandler(f"log/{file_name}.log", encoding="utf-8")
    file_handler.setLevel(level)  # 10-debug; 20-info; 30-warning; 40-error; 50-critical
    file_handler.setFormatter(formatter)  # Ustawienia handlera

    logger.addHandler(file_handler)  # Dodanie handlera do loggera
    if level >= 30:
        logger.log(level, message, exc_info=True)  # Logowanie wiadomości
    else:
        logger.log(level, message)
