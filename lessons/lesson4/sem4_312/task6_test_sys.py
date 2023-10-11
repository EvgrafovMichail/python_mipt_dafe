from testcases import testcases

def check_comand(user_comand: str, comands: list[str]) -> bool:
    cnt = 0

    #ошибка №1: недостаточный ввод
    for i in range(len(comands)):
        for j in range(len(comands[i])):
            check_str = ''
            for k in range(len(comands[i])):
                if k != j:
                    check_str += comands[i][k]
            if user_comand == check_str:
                cnt += 1
    if cnt > 1:
        return False
    
    #ошибка №2: чрезмерный ввод
    for i in range(len(user_comand)):
        check_str = ''
        for j in range(len(user_comand)):
            if i != j:
                check_str += user_comand[j]
        if check_str in comands:
            cnt += 1
    if cnt > 1:
        return False
    
    #ошибка №3: замена символа
    for i in range(len(user_comand)):
        check_str_1 = ''
        for j in range(len(user_comand)): # смотрим, после удаления какого символа
            if j != i:                    # записиь пользователя будет недостаточной, как в ошибке №1
                check_str_1 += user_comand[j]
        for j in range(len(comands)):
            for k in range(len(comands[j])):
                check_str_2 = ''
                for s in range(len(comands[j])):
                    if k != s:
                        check_str_2 += comands[j][s]
                if check_str_1 == check_str_2:
                    cnt += 1
                    if cnt > 1:
                        return False
    return cnt == 1



testcases_list = testcases["check_comand"]
work_function = check_comand


########################################################
if __name__ == "__main__":
    success_count = 0
    cases_faild = []

    for case_num, case in enumerate(testcases_list):
        args = case["input"].copy()
        case_ans = case["output"]

        print(f"case {case_num+1}/{len(testcases_list)}")
        for i, arg in enumerate(args):
            print(f"arg_{i+1}: {arg}")
        
        output = work_function(*args)
        print(f"\texpected: {case_ans}")
        print(f"\tgot: {output}")

        if  output == case_ans:
            print("OK".center(20,"="), end="\n\n")
            success_count += 1
        else:
            print("NOT".center(20,"~"), end="\n\n")
            cases_faild.append(case_num+1)
    
    print(f"tests passed: {success_count}/{len(testcases_list)}")
    print(f"cases faild: {cases_faild}")