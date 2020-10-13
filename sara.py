print("pudding ni zen me zhe me ke ai ya!!!!")

print("xjs zen me zhe me chou a!!!!")

def is_pldrm(s):
    for i in range(len(s)):
        if s[i] != s[::-1][i]:
            return False
    return True


assert is_pldrm("12345") is False, "Failed test case 12345"
assert is_pldrm("12321") is True, "Failed test case 12321"
assert is_pldrm("33333") is True, "Failed test case 33333"
assert is_pldrm("99199") is True, "Failed test case 99199"
assert is_pldrm("0") is True, "Failed test case 0"


def extract_alphas(seq):
    alphas = set()
    out = {}
    place = 1
    for c in range(len(seq)):
        change_made = False
        for alpha in seq[c]:
            if alpha not in alphas:
                out[alpha] = place
                change_made = True
                alphas.add(alpha)
        if change_made:
            place += 1
    return out

print(extract_alphas(["a", "ab", "cd", "efgh"]))


