import unittest

class TestCase(unittest.TestCase):
    def test_1(self):


       
        # Begin Test Case Contents

        from Project7.project import generate_LMAOcode_from_LOLcode
        from Project7.project import generate_ROFLcode_from_LOLcode
        from Project7.interpreter import interpret

        SEED = 0
        STANDARD_INPUT = "abcdef"

        def strip_leading_whitespace(text):
            lines = [line.lstrip() for line in text.splitlines()]
            return '\n'.join(lines)

        def expect_exception(lolcode_str):
            print(f"LOLcode str:\n{lolcode_str}")
            with self.assertRaises(Exception) as e:
                generate_LMAOcode_from_LOLcode(lolcode_str)
            with self.assertRaises(Exception) as e:
                generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Correctly raised exception")

        def check_output(lolcode_str, expected_output):
            print(f"LOLcode str:\n{lolcode_str}")
            lmaocode = generate_LMAOcode_from_LOLcode(lolcode_str)
            print("Generated LMAOcode:")
            print(lmaocode)
            executed_lmao_output = interpret(lmaocode, 'LMAOcode', seed=SEED, standard_input=STANDARD_INPUT)

            self.assertEqual(expected_output, executed_lmao_output)
            roflcode = generate_ROFLcode_from_LOLcode(lolcode_str)
            print("Generated ROFLcode:")
            print(roflcode)
            executed_rofl_output = interpret(roflcode, 'ROFLcode', seed=SEED, standard_input=STANDARD_INPUT)

            self.assertEqual(expected_output, executed_rofl_output)

        import re

        def sanitize(lmaocode_str):
            out = []
            outstr = []
            split_lmao = lmaocode_str.split('\n')
            count = 0
            indx = 0
            for i in split_lmao:
                count = 0
                i_str = i.split(" ")
                while count < len(i_str):
                    if not i_str[count]:
                        del i_str[count]
                    else:
                        count += 1
                out.append(i_str)
            indx = 0
            while indx < len(out):
                if not out[indx]:
                    del out[indx]
                else:
                    indx += 1
            for j in out:
                indx = 0
                while indx < len(j):
                    if '\t' in j[indx]:
                        count = 0
                        temp_str = j[indx].split('\t')
                        while count < len(temp_str):
                            if not temp_str[count]:
                                del temp_str[count]
                            else:
                                count += 1
                        j[indx] = temp_str[0]
                    indx += 1
            for k in out:
                comment = 0
                count = 0
                for l in k:
                    if '#' in l:
                        comment = 1
                    if comment == 1:
                        while count < len(k):
                            del k[count]
                    count += 1
                outstr.append(k)
            for i in outstr:
                count = 0
                while count < len(i) - 1:
                    if i[count] == "'" and i[count + 1] == "'":
                        i[count] = "' '"
                        del i[count + 1]
                    else:
                        count += 1
            indx = 0
            while indx < len(outstr):
                if not outstr[indx]:
                    del outstr[indx]
                else:
                    indx += 1
            return outstr

        def convert_to_basic_blocks(lmaocode_str):
            out = sanitize(lmaocode_str)
            temp = []
            final_out = []
            count = 0
            label = re.compile("[a-z][a-z](.*):")
            label_present = False
            for i in out:
                if label.match(i[0]):
                    final_out.append(temp)
                    temp = []
                    #if label_present:
                    #    final_out.append(temp)
                    #    temp = []
                    label_present = True
                temp.append(i)
                if "JUMP" in i[0]:
                    final_out.append(temp)
                    temp = []
            final_out.append(temp)
            if not final_out and lmaocode_str:
                final_out = [out]
            indx = 0
            while indx < len(final_out):
                if not final_out[indx]:
                    del final_out[indx]
                else:
                    indx += 1
            return final_out

        result = convert_to_basic_blocks(r"""
        OUT_NUM 34
        label:
        OUT_CHAR '\n'
        JUMP_IF_0 5 label
        """)
        print(result)

        # End Test Case Contents


if __name__ == '__main__':
    unittest.main()