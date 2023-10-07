class test_arg:
    def __init__(self, user_comand, comands, ans):
        self.user_comand = user_comand
        self.comands = comands
        self.ans = ans

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



####################################################################
if __name__ == "__main__":
    print()

    test_cases = [
        test_arg(user_comand="gt",
                 comands=['cd', 'ls', 'git'],
                 ans=True),

        test_arg(user_comand="gt",
                 comands=['cd', 'ls', 'git', 'get'],
                 ans=False),
    ]

    success_count = 0
    for case in test_cases:
        print(f"user_comand: {case.user_comand}")
        print(f"comands: {case.comands}")
        
        output = check_comand(case.user_comand, case.comands)
        print(f"\texpected: {case.ans}")
        print(f"\tgot: {output}")

        if  output == case.ans:
            print("OK".center(20,"="), end="\n\n")
            success_count += 1
        else:
            print("NOT".center(20,"~"), end="\n\n")
    
    print(f"tests passed: {success_count}/{len(test_cases)}")