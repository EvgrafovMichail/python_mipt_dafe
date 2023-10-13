from testcases import testcases

def parser(string, valid_pairs):
    corr_str = string.replace('>', '> ')
    corr_str = corr_str.replace('<', ' <')
    msv_str = corr_str.split()
    ans = []
    for i in range(len(msv_str)-2):
        if (msv_str[i], msv_str[i+2]) in valid_pairs:
            if msv_str[i+1] not in ans:
                ans.append(msv_str[i+1])
    return ans



testcases_list = testcases["parser"]
work_function = parser


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
