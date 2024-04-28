from math import log
from numpy import mean

from lsm_project.lsm.functions import get_lsm_lines, get_lsm_description, get_report
from lsm_project.visualization import switch_to_ggplot, visualize_lines
from lsm_project.lsm.enumerations import MismatchStrategies


if __name__ == '__main__':
    abscissa = [1/(22.10 + 273), 1/(28.70 + 273), 1/(33.70 + 273), 1/(38.70 + 273)]
    ordinates = list(map(log, [
        mean([1.185268, 1.082487, 1.07551, 1.011286, 1.003048]), 
        mean([0.643865, 0.718753, 0.580713, 0.619726, 0.576198]),
        mean([0.441662, 0.465684, 0.441564, 0.439569, 0.464127]),
        mean([0.291069, 0.308168, 0.259957, 0.234406, 0.295354])
    ]))

    # получаем зависимость с помощью МНК
    lsm_description = get_lsm_description(abscissa, ordinates, MismatchStrategies.CUT)
    lines = get_lsm_lines(abscissa, ordinates)

    # визуализируем результаты
    with switch_to_ggplot():
        visualize_lines(lines)

    # сохраняем отчет в текстовый файл
    get_report(lsm_description, 'report.txt')
