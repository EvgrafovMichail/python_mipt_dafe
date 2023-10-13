""" 
Задача 3: Раздача стипендий

В университете царит бюрократия и ведётся множество различных списков студентов. 
За выдающиеся результаты в учёбе и отсутствие выговоров студентов включают в список лучших студентов, 
а за активную социальную деятельность - в список социально активных студентов. 
Также ведутся список студентов, получающих плохие оценки, и список студентов, 
получивших дисциплинарные взыскания.

Каждый год студентам этого университета раздаётся стипендия, назначаемая специальной комиссией. 
При этом члены комиссии выбирают стипендиатов на своё усмотрение, но есть несколько правил:

    1) Все лучшие студенты обязаны получить стипендию
    2) Среди социально активных студентов, которые не являются при этом лучшими, получить стипендию может не больше половины
    3) Среди студентов с дисциплинарными взысканиями стипендию может получить не больше одного человека
    4) Студенты с плохими оценками не могут получить стипендию
    5) Среди студентов, не включенных в списки лучших, худших или социально активных, получить стипендию могут не более трёх человек

Ваша задача проверить, соответствует ли предоставленный стипендиальной комиссией список правилам университета.
"""

def is_scolarship_correct(best_students, active_students, delinquent_studens, lagging_students, all_students, scolarships):
    active_students_counter=0
    delinquent_studens_counter=0
    all_students_counter=0
    kolvo_active=0
    for i in active_students:
        if i not in best_students:
            kolvo_active+=1



    for i in scolarships:
        if i in lagging_students:
            return False
        if i in best_students:
            continue
        if i in active_students:
            active_students_counter+=1
            if active_students_counter>(kolvo_active/2):  
                return False
        if i in delinquent_studens:
            delinquent_studens_counter+=1
            if delinquent_studens_counter>1:
                return False
        if i in all_students:
            all_students_counter+=1
            if all_students_counter>3:
                return False
            
    return True


if __name__ == "__main__":
    pass
