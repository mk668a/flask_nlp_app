import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


class Analyzer:
    def tense_analyze(self, value_str):
        if(len(value_str) > 0 and "." != value_str[-1]):
            value_str = value_str+"."
        s = value_str
        morph = nltk.word_tokenize(value_str)
        result = nltk.pos_tag(morph)
        tense = ''
        q = 0
        will = re.search('will', value_str)
        for i in range(len(s.split())):
            b = int(i)
            if result[b][1] != 'VBP' and result[b][1] != 'VBZ' and result[b][1] != 'VBG' and result[b][1] != 'VB' and result[b][1] != 'VBD' and result[b][1] != 'VBN':
                q = q+1
            elif (result[b][1] == 'VBP' or result[b][1] == 'VBZ' or result[b][1] == 'VBD' or result[b][1] == 'VB') and (result[b][0] != 'am' and result[b][0] != 'are' and result[b][0] != 'was' and result[b][0] != 'were' and result[b][0] != "be" and result[b][0] != 'is'):
                if result[b][0] == 'have' or result[b][0] == 'has' or result[b][0] == 'had':
                    if result[b+1][1] == 'VBN' or result[b+2][1] == 'VBN' or result[b+1][1] == 'VBD' or result[b+2][1] == 'VBD':
                        if result[b+1][0] == 'been':
                            if result[b+2][1] == 'VBG' or result[b+3][1] == 'VBG':
                                tense = '完了進行形'
                                break
                            else:
                                tense = '完了形'
                                break
                        else:
                            tense = '完了形'
                            break
                    else:
                        tense = '現在形'
                        break
                else:
                    tense = '現在形'
            elif result[b][1] == "VBP" or result[b][0] == "was" or result[b][0] == "were" or result[b][1] == "VBZ" or result[b][0] == "be" or result[b][0] == "is" or result[b][0] == "VBD":
                if result[b+1][1] == 'VBG':
                    tense = '進行形'
                    break
                else:
                    tense = '現在形'
                    break

        for j in range(len(s.split())):
            c = int(j)
            if tense == '現在形':
                if result[c][1] == 'VBD':
                    tense = '過去形'
                    break
                elif result[c][1] == 'VBD' and (result[c-1][1] == 'VBP' or result[c-1][1] == 'VBD' or result[c-1][1] == 'VBZ'):
                    tense = '過去形'
                    break
                elif (not will) and result[c][1] == "VBP" or result[c][1] == "VBZ":
                    tense = "現在形"
                elif will and (result[c-1][1] != 'VBP' or result[c-1][1] != 'VBD' or result[c-1][1] != 'VBZ'):
                    tense = "未来形"
                else:
                    q = q+1
            elif tense == "完了形":
                if result[c][0] == 'had':
                    tense = '過去完了形'
                    break
                elif not will and (result[c][0] == "have" or result[c][0] == "has"):
                    tense = "現在完了形"
                elif will and result[c][0] == "have":
                    tense = "未来完了形"
            elif tense == "進行形":
                if result[c][0] == 'was' or result[c][0] == 'were':
                    tense = '過去進行形'
                    break
                elif (not will) and result[c][1] == "VBP" or result[c][1] == "VBZ":
                    tense = "現在進行形"
                elif will:
                    tense = "未来進行形"
                else:
                    q = q+1
            elif tense == "完了進行形":
                if result[c][0] == 'had':
                    tense = "過去完了進行形"
                elif not will and (result[c][0] == 'have' or result[c][0] == "has"):
                    tense = '現在完了進行形'
                elif will:
                    tense = "未来完了進行形"
            else:
                q = q+1
        value_str.strip()

        return value_str, tense
