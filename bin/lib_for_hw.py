import os
import platform


def get_cpu_load(system_type):
    """
        Получает информацию о загрузке CPU на операционных системах Linux и macOS.

        Args:
            system_type (str): Тип операционной системы, "linux" или "mac".

        Returns:
            str: Информация о загрузке CPU.

        Raises:
            ValueError: Если передан неподдерживаемый тип операционной системы.

        Example:
            cpu_load_data = get_cpu_load(system_type)
        """
    if system_type == "linux":
        try:
            with open('/proc/loadavg', 'r') as loadavg_file:
                cpu_load_data = loadavg_file.read()
            return cpu_load_data
        except FileNotFoundError:
            return "File /proc/loadavg not found (Linux)"
    elif system_type == "mac":
        try:
            # Проверяем, что мы работаем на macOS
            if platform.system() == "Darwin":
                load_data = os.popen("top -l 1 | grep 'CPU usage:'").read()
                return load_data.strip()
            else:
                return "macOS not detected"
        except Exception as e:
            return str(e)
    else:
        return "Unsupported system_type"