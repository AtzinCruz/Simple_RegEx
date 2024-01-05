class RegEx:
    ALPHABETSIZE = 128

    def __init__(self):
        self.globe = True
        self.insensitive = False
        self.text = ""
        self.path = ""

    def set_path(self, path):
        self.path = path
        self.set_text()

    # Getting file text
    def set_text(self):
        with open(self.path, 'r') as file:
            self.text = file.read()

    # Calculate match table
    def __calculate_badmatch_table(self, pattern):
        table = [len(pattern)] * RegEx.ALPHABETSIZE
        for i in range(len(pattern) - 1):
            table[ord(pattern[i])] = len(pattern) - i - 1
        return table

    def ast(self, pattern):
        text = self.text
        if self.insensitive:
            text = text.lower()
            pattern = pattern.lower()
        matches_inicial = []
        matches_total = []
        bad_matching_table = self.__calculate_badmatch_table(pattern)
        patt_size = len(pattern)
        text_index = patt_size - 1
        index = 0
        for i in range(patt_size):
            if pattern[i] == '*':
                index = i
        for i in range(95, 123):
            if bad_matching_table[i] > patt_size - 1 - index:
                bad_matching_table[i] = patt_size - 1 - index
        while text_index < len(text):
            shared_substr = 0
            while shared_substr < patt_size:
                if text[text_index - shared_substr] == pattern[patt_size - shared_substr - 1] or (pattern[patt_size - shared_substr - 1] == "*" and ord(text[text_index - shared_substr]) >= 97 and ord(text[text_index - shared_substr]) <= 122):
                    shared_substr += 1
                else:
                    break
                if shared_substr == patt_size:
                    matches_inicial.append(text_index - patt_size + 1)
            text_index += bad_matching_table[ord(text[text_index])]
        for i in matches_inicial:
            for j in range(i, i + patt_size):
                matches_total.append(j)
        if self.globe:
            return matches_inicial, matches_total
        if matches_inicial != [] and matches_total != []:
            return [matches_inicial[0]], matches_total[0:patt_size]

    def repetition(self, pattern):
        i = 0
        result = ""
        flag = False
        while i < len(pattern):
            if pattern[i] == "{":
                char = pattern[i - 1]
                mult = int(pattern[i + 1])
                result += pattern[:i - 1]
                result += char * mult
                i = i + 3
                flag = True
            elif flag:
                result += pattern[i]
                i += 1
            else:
                i += 1
        return self.ast(result)

    def contained(self, pattern):
        text = self.text
        if self.insensitive:
            text = text.lower()
            pattern = pattern.lower()
        contained = False
        clean_pattern = []
        contained_letters = []
        matches_inicial = []
        matches_total = []
        for i in range(len(pattern)):
            if pattern[i] == "]":
                contained = False
            if contained:
                contained_letters.append(pattern[i])
            if not contained and (pattern[i] != "[" and pattern[i] != "]"):
                clean_pattern.append(pattern[i])
            if pattern[i] == "[":
                contained = True
                index = i
        clean_pattern.insert(index, "x")
        badmatch_table = self.__calculate_badmatch_table(clean_pattern)
        patt_size = len(clean_pattern)
        for i in contained_letters:
            if badmatch_table[ord(i)] > patt_size - 1 - index:
                badmatch_table[ord(i)] = patt_size - 1 - index
        print(clean_pattern)
        print(contained_letters)

        text_index = patt_size - 1

        while text_index < len(text):
            shared_substring = 0
            while shared_substring < patt_size:
                if text[text_index - shared_substring] == clean_pattern[patt_size - 1 - shared_substring] or (
                        clean_pattern[patt_size - 1 - shared_substring] == 'x' and text[
                    text_index - shared_substring] in contained_letters):
                    shared_substring += 1
                else:
                    break

            if shared_substring == patt_size:
                matches_inicial.append(text_index - patt_size + 1)

            text_index += badmatch_table[ord(text[text_index])]

        for i in matches_inicial:
            for j in range(i, i + patt_size):
                matches_total.append(j)

        if self.globe:
            return matches_inicial, matches_total
        if matches_inicial != [] and matches_total != []:
            return [matches_inicial[0]], matches_total[0: patt_size]

    def range(self, pattern):
        text = self.text
        if self.insensitive:
            text = text.lower()
            pattern = pattern.lower()
        matches = []
        matches2 = []
        word = ""
        first = ""
        last = ""
        inside_brackets = False
        for i in range(len(pattern)):
            if pattern[i] == "[":
                inside_brackets = True
                first = pattern[i + 1]
                word += " "
                index = len(word) - 1
            elif pattern[i] == "]":
                inside_brackets = False
                last = pattern[i - 1]
            elif not inside_brackets:
                word += pattern[i]

        pat_size = len(word)
        bad_match_table = self.__calculate_badmatch_table(word)
        c_range = [chr(i) for i in range(ord(first), ord(last) + 1)]

        for i in c_range:
            if bad_match_table[ord(i)] > pat_size - 1 - index:
                bad_match_table[ord(i)] = pat_size - 1 - index

        text_idx = pat_size - 1
        while text_idx < len(text):
            shared_substr = 0
            while shared_substr < pat_size:
                if (text[text_idx - shared_substr] == word[pat_size - shared_substr - 1] and word[
                    pat_size - shared_substr - 1] != " ") or (
                        pat_size - shared_substr - 1 == index and text[text_idx - shared_substr] in c_range):
                    shared_substr += 1
                else:
                    break
            if shared_substr == pat_size:
                idx_aux = text_idx - pat_size + 1
                matches.append(idx_aux)
                for i in range(pat_size):
                    matches2.append(idx_aux + i)
                text_idx += pat_size
            elif text_idx + bad_match_table[ord(text[text_idx])] < len(text):
                text_idx += bad_match_table[ord(text[text_idx])]
            else:
                break
        if self.globe:
            return matches, matches2
        if matches != [] and matches2 != []:
            return [matches[0]], matches2[0:pat_size]

    def question_mark(self, pattern):
        pattern1 = ""
        pattern2 = ""
        index = 0
        for i in range(len(pattern)):
            if pattern[i].isalpha():
                pattern1 += pattern[i]
            else:
                index = i - 1

        for i in range(len(pattern)):
            if pattern[i].isalpha() and i != index:
                pattern2 += pattern[i]

        print(pattern1)
        print(pattern2)
        matches1_inicial, matches1_total = self.ast(pattern1)
        matches2_inicial, matches2_total = self.ast(pattern2)

        if self.globe:
            matches1_inicial.extend(matches2_inicial)
            matches1_total.extend(matches2_total)
            return matches1_inicial, matches1_total
        if matches1_inicial[0] < matches2_inicial[0]:
            return [matches1_inicial[0]], matches1_total[0:len(pattern1)]
        else:
            return [matches2_inicial[0]], matches2_total[0: len(pattern2)]

    def detect_operator(self, pattern):
        if pattern.isalpha():
            return 1
        if '*' in pattern:
            return 2
        if '{' in pattern:
            return 3
        if '?' in pattern:
            return 4
        if '-' in pattern:
            return 5
        if '[' in pattern:
            return 6
        if '|' in pattern:
            return 7

    def operator_or(self, pattern):
        left = ""
        right = ""
        matches1_inicial = []
        matches1_total = []
        matches2_inicial = []
        matches2_total = []
        flag = False
        for i in pattern:
            if i == "|":
                flag = True
                continue
            if flag == False and i != " ":
                left += i
            elif i != " ":
                right += i
        left_final = self.detect_operator(left)
        right_final = self.detect_operator(right)
        match left_final:
            case 1:
                matches1_inicial, matches1_total = self.ast(left)
            case 2:
                matches1_inicial, matches1_total = self.ast(left)
            case 3:
                matches1_inicial, matches1_total = self.repetition(left)
            case 4:
                matches1_inicial, matches1_total = self.question_mark(left)
            case 5:
                matches1_inicial, matches1_total = self.range(left)
            case 6:
                matches1_inicial, matches1_total = self.contained(left)
        match right_final:
            case 1:
                matches2_inicial, matches2_total = self.ast(right)
            case 2:
                matches2_inicial, matches2_total = self.ast(right)
            case 3:
                matches2_inicial, matches2_total = self.repetition(right)
            case 4:
                matches2_inicial, matches2_total = self.question_mark(right)
            case 5:
                matches2_inicial, matches2_total = self.range(right)
            case 6:
                matches2_inicial, matches2_total = self.contained(right)
        if self.globe:
            matches1_inicial.extend(matches2_inicial)
            matches1_total.extend(matches2_total)
            return matches1_inicial, matches1_total
        if matches1_inicial[0] < matches2_inicial[0] and matches1_inicial != []:
            return [matches1_inicial[0]], matches1_total[0:len(left)]
        else:
            if matches2_inicial != []:
                return [matches2_inicial[0]], matches2_total[0: len(right)]

    def query_management(self, query):
        matches_inicial = []
        matches_total = []
        arr_query = query.split()
        orOpreator = False
        """
        for i in range(len(query)):
            if query[i] == ' ':
                arr_query.append(query[flag:i])
                flag += i
            if query[i] == '|':
                orOpreator = True
        """
        print(arr_query)

        if 'i' in arr_query:
            self.insensitive = True
        else:
            self.insensitive = False
        if 'g' in arr_query:
            self.globe = True
        else:
            self.globe = False

        if '|' in arr_query:
            orOpreator = True
        else:
            orOpreator = False
        if not orOpreator:
            match self.detect_operator(arr_query[1]):
                case 1:
                    matches_inicial, matches_total = self.ast(arr_query[1])
                case 2:
                    matches_inicial, matches_total = self.ast(arr_query[1])
                case 3:
                    matches_inicial, matches_total = self.repetition(arr_query[1])
                case 4:
                    matches_inicial, matches_total = self.question_mark(arr_query[1])
                case 5:
                    matches_inicial, matches_total = self.range(arr_query[1])
                case 6:
                    matches_inicial, matches_total = self.contained(arr_query[1])
        else:
            pattern = ""
            pattern += arr_query[1] + arr_query[2] + arr_query[3]
            matches_inicial, matches_total = self.operator_or(pattern)

        if arr_query[0] == 'f':
            return matches_inicial
        if arr_query[0] == 'fr':
            if not orOpreator:
                self.find_and_replace(arr_query[2], matches_total, matches_inicial)
            else:
                self.find_and_replace(arr_query[4], matches_total, matches_inicial)
            return matches_inicial

    # replace = palabra nueva
    # name_text = nombre del archivo
    # matches = array original
    # begining = array de solo el inicio

    def find_and_replace(self, replace, matches, begining):
        contador = 0
        flag = 0
        content = self.text
        str_new = ""
        flag_final = True
        final = []
        contador_aux = 1
        print(matches)
        for i in range(len(matches)):
            if matches[i] == begining[contador_aux - 1]:
                final.append(matches[i - 1])
                if contador_aux < len(begining):
                    contador_aux += 1
        final.sort()
        while True:
            if len(matches) == 0:
                flag_final = False
                break
            str_new += content[flag:begining[contador]]
            str_new += replace
            if final[contador] == matches[-1]:
                str_new += content[final[-1] + 1:]
                break
            flag = final[contador] + 1
            contador += 1

        if flag_final:
            with open(self.path, 'w') as archivo:
                archivo.write(str_new)