from random import randint


def print_questions_ids() -> None:
    start = 1
    question_amount_block1 = 19
    question_amount_block2_3 = 13
    listing_amount = 35

    line_len, placeholder = 80, "="

    print(
        "START QUESTIONS ROLLING".center(line_len, placeholder),
        f"[ROLL]: language basics: {randint(start, question_amount_block1)};",
        f"[ROLL]: functions: {randint(start, question_amount_block2_3)};",
        f"[ROLL]: OOP: {randint(start, question_amount_block2_3)};",
        f"[ROLL]: code listing: {randint(start, listing_amount)};",
        "CHOICE WAS DONE".center(line_len, placeholder),
        sep="\n",
        end="\n\n",
    )


if __name__ == '__main__':
    print_questions_ids()
