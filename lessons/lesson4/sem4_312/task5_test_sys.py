from testcases import testcases

class test_arg:
    def __init__(self, string, val_pairs, ans):
        self.string = string
        self.val_pairs = val_pairs
        self.ans = ans



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






########################################################
if __name__ == "__main__":
    success_count = 0
    testcases_list = testcases["parser"]
    for case in testcases_list:
        string = case["input"][0]
        valid_pairs = case["input"][1]
        case_ans = case["output"]

        print(f"string: {string}")
        print(f"val_pairs: {valid_pairs}")
        
        output = parser(string, valid_pairs)
        print(f"\texpected: {case_ans}")
        print(f"\tgot: {output}")

        if  output == case_ans:
            print("OK".center(20,"="), end="\n\n")
            success_count += 1
        else:
            print("NOT".center(20,"~"), end="\n\n")
    
    print(f"tests passed: {success_count}/{len(testcases_list)}")
