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
    print()

    test_cases = [
        test_arg(string='</p><p><a>float</b></p><p><b>frozenset</b></p><p><c>list</c></p><p><b>list</b>',
                 val_pairs=[("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")],
                 ans=["frozenset", "list"]),
        
        test_arg(string='<\a>float<\b>double<\c>complex<c><b><a>',
                 val_pairs=[("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")],
                 ans=[]),

        test_arg(string="</p>this_is_float<p>",
                 val_pairs=[("</p>", "<p>")],
                 ans=["this_is_float"]),

        test_arg(string="</a>this<a></b>is<b><a>good</a><c>example</c>",
                 val_pairs=[("<a>", "</a>"),("</a>", "<a>"),("</b>", "<b>"),("<c>", "</c>")],
                 ans=["this", "is", "good", "example"]),
        
        test_arg(string="</a>this<c></b>is<b><a>good</a><a>example</c>",
                 val_pairs=[("<a>", "</a>"),("</a>", "<a>"),("</b>", "<b>"),("<c>", "</c>")],
                 ans=["is", "good"]),
    ]

    success_count = 0
    for case in test_cases:
        print(f"string: {case.string}")
        print(f"val_pairs: {case.val_pairs}")
        
        output = parser(case.string, case.val_pairs)
        print(f"\texpected: {case.ans}")
        print(f"\tgot: {output}")

        if  output == case.ans:
            print("OK".center(20,"="), end="\n\n")
            success_count += 1
        else:
            print("NOT".center(20,"~"), end="\n\n")
    
    print(f"tests passed: {success_count}/{len(test_cases)}")
