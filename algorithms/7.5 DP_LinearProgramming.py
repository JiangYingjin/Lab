# %%
fLst = [[[] for _ in range(16)] for _ in range(9)]
Path = [["" for _ in range(16)] for _ in range(9)]

P1, P2 = 8, 7
W11, W12 = 2, 5
W21, W22 = 1, 2
M1, M2 = 8, 15


def f(M1, M2):
    if not (M1 >= W11 and M2 >= W12) and not (M1 >= W21 and M2 >= W22):
        strp = f"    f({M1}, {M2}) = 0"
        print(strp)
        return (0, "")

    tmpF = []
    strp = f"    f({M1}, {M2}) = max" + "{"
    if M1 >= W11 and M2 >= W12:
        # print(f"f({M1} - {W11}, {M2} - {W12}) + {P1}")
        tmpF.append(
            (getF(M1 - W11, M2 - W12)[0] + P1, getF(M1 - W11, M2 - W12)[1] + "x1")
        )
        strp += f" f({M1} - {W11}, {M2} - {W12}) + {P1},"
    if M1 >= W21 and M2 >= W22:
        # print(f"f({M1} - {W21}, {M2} - {W22}) + {P2}")
        tmpF.append(
            (getF(M1 - W21, M2 - W22)[0] + P2, getF(M1 - W21, M2 - W22)[1] + "x2")
        )
        strp += f" f({M1} - {W21}, {M2} - {W22}) + {P2} "
    if strp[-1] == ",":
        strp = strp[:-1] + " "
    strp += "}\n"

    strp += " " * strp.find("=") + "= max{ "
    for res in tmpF:
        strp += f"{res[0]}({res[1]}), "
    strp = strp[:-2] + " }\n"

    tmpF.sort(key=lambda x: x[0], reverse=True)
    strp += " " * strp.find("=") + f"= {tmpF[0][0]}({tmpF[0][1]})"

    print(strp,'\n')
    # print(f"\nFor f({M1}, {M2}):", tmpF, "\n")
    return tmpF[0]


def getF(M1, M2):
    if fLst[M1][M2] != []:
        # print(f"f({M1}, {M2}) already exists.", (fLst[M1][M2], Path[M1][M2]))
        return (fLst[M1][M2], Path[M1][M2])
    else:
        # print(f"f({M1}, {M2}) does not exists. Search for it.")
        print(f'Calculate f({M1}, {M2})')
        res = f(M1, M2)
        fLst[M1][M2] = res[0]
        Path[M1][M2] = res[1]
        return res


f(8, 15)
