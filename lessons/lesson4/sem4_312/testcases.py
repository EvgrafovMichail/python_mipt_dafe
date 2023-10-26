testcases = {
    "parser": [
        {
            "input": [
                "</p><p><a>float</b></p><p><b>frozenset</b></p><p><c>list</c></p><p><b>list</b>",
                [("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")]
            ],
            "output": ["frozenset", "list"]
        },
        {
            "input": [
                "<\\a>float<\\b>double<\\c>complex<c><b><a>",
                [("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")]
            ],
            "output": []
        },
        {
            "input": [
                "<a>float<b>double<c>complex</c></b></a>",
                [("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")]
            ],
            "output": ["complex"]
        },
        {
            "input": [
                "<a>float<b>double<c>complex</a></b></c>",
                [("<a>", "</a>"), ("<b>", "</b>"), ("<c>", "</c>")]
            ],
            "output": []
        },
        {
            "input": [
                "</p>this_is_float<p>",
                [("</p>", "<p>")]
            ],
            "output": ["this_is_float"]
        },
        {
            "input": [
                "<p>this_is_float</p>",
                [("</p>", "<p>")]
            ],
            "output": []
        },
        {
            "input": [
                "</a>this<a></b>is<b><a>good</a><c>example</c>",
                [("<a>", "</a>"), ("</a>", "<a>"), ("</b>", "<b>"), ("<c>", "</c>")]
            ],
            "output": ["this", "is", "good", "example"]
        },
        {
            "input": [
                "</a>this<c></b>is<b><a>good</a><a>example</c>",
                [("<a>", "</a>"), ("</a>", "<a>"), ("</b>", "<b>"), ("<c>", "</c>")]
            ],
            "output": ["is", "good"]
        },
        {
            "input": [
                "</a><a></b>complex</b>int<b><b>",
                [("</a>", "<a>"), ("</b>", "<b>")]
            ],
            "output": ["int"]
        },
        {
            "input": [
                "</z><z></x>complex</x>int<x><x>",
                [("</a>", "<a>"), ("</b>", "<b>")]
            ],
            "output": []
        }
    ],

    "check_comand": [
        # блок укороченных команд
        {
            "input": [
                "gt", ["cd", "ls", "git"]
            ],
            "output": True
        },
        {
            "input": [
                "gt", ["cd", "ls", "git", "get"]
            ],
            "output": False
        },
        {
            "input": [
                "c", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "d", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "it", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "gi", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },

        # блок удлиненных команд
        {
            "input": [
                "getting", ["cd", "ls", "git", "get"]
            ],
            "output": False
        },
        {
            "input": [
                "wget", ["cd", "ls", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "geto", ["cd", "ls", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "geet", ["cd", "ls", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "geet", ["cd", "ls", "git"]
            ],
            "output": False
        },

        # блок ошибок в одной букве
        {
            "input": [
                "get", ["cd", "ls", "git"]
            ],
            "output": True
        },
        {
            "input": [
                "get", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },
        {
            "input": [
                "gid", ["cd", "ls", "git", "get", "gil"]
            ],
            "output": False
        },
        {
            "input": [
                "gid", ["cd", "ls", "git", "get"]
            ],
            "output": True
        },

        # блок обычных команд
        {
            "input": [
                "wget", ["cd", "ls", "get", "wget"]
            ],
            "output": True
        },
        {
            "input": [
                "rm", ["cd", "ls", "git", "wget"]
            ],
            "output": False
        }
    ]
}
