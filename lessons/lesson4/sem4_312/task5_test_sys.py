class test_arg:
    def __init__(self, string, val_pairs, ans):
        self.string = string
        self.val_pairs = val_pairs
        self.ans = ans



def parser(string, valid_pairs):
    pass


if __name__ == "__main__":
    print()

    test_cases = [
        test_arg(string='</p><p><a>float</b></p><p><b>frozenset</b></p><p><c>list</c></p><p><b>list</b>',
                 val_pairs=[("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")],
                 ans=["frozenset", "list"]),
        
        test_arg(string='<\a>float<\b>double<\c>complex<c><b><a>',
                 val_pairs=[("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")],
                 ans=['complex']),

        test_arg(string="</p>this_is_float<p>",
                 val_pairs=[("</p>", "<p>")],
                 ans=["this_is_float"]),
    ]

    for case in test_cases:
        print(f"string: {case.string}")
        print(f"val_pairs: {case.val_pairs}")
        
        output = parser(case.string, case.val_pairs)
        print(f"\texpected: {case.ans}")
        print(f"\tgot: {output}")

        if  output == case.ans:
            print("OK".center(20,"="), end="\n\n")
        else:
            print("NOT".center(20,"~"), end="\n\n")
            
