import json
import os

# from python_mipt_dafe.homeworks.hw1.lsm_project.lsm.functions_dabizha_vadim_313 import get_lsm_lines
# from python_mipt_dafe.homeworks.hw1.lsm_project.lsm.functions_dabizha_vadim_313 import get_lsm_description
# from python_mipt_dafe.homeworks.hw1.lsm_project.lsm.functions_dabizha_vadim_313 import get_report

from lsm_project.lsm.functions_Vadim_Dabizha_fixed import get_lsm_lines
from lsm_project.lsm.functions_Vadim_Dabizha_fixed import get_lsm_description
from lsm_project.lsm.functions_Vadim_Dabizha_fixed import get_report

from lsm_project.visualization import switch_to_ggplot, visualize_lines

if __name__ == '__main__':
    path_to_data = os.path.join('.', 'measurments.json')

    # загружаем данные эксперимента из json-файла
    with open(path_to_data, 'r') as file:
        measurments: dict = json.load(file)
        abscissa = measurments.get('abscissa', [])
        ordinates = measurments.get('ordinates', [])

    # получаем зависимость с помощью МНК
    lsm_description = get_lsm_description(abscissa, ordinates)
    lines = get_lsm_lines(abscissa,ordinates,)

    # визуализируем результаты
    with switch_to_ggplot():
        visualize_lines(lines)

    # сохраняем отчет в текстовый файл
    get_report(lsm_description, '')
