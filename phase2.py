# OP_code table in which instructions and the op code code of each instruction are seperated based on number of bits of it's opperands
# and wheter they are pointing to a memory location or not(True: Memory, Flase: Register)  
opcode_table = {
    "ADD": {8: {False: "00", True: "02"}, 16: {False: "66 01", True: "66 03"}, 32: {False: "01", True: "03"}},
    "SUB": {8: {False: "28", True: "2A"}, 16: {False: "66 29", True: "66 2B"}, 32: {False: "29", True: "2B"}},
    "AND": {8: {False: "20", True: "22"}, 16: {False: "66 21", True: "66 23"}, 32: {False: "21", True: "23"}},
    "OR": {8: {False: "08", True: "0A"}, 16: {False: "66 09", True: "66 0B"}, 32: {False: "09", True: "0B"}},
    "XOR": {8: {False: "30", True: "32"}, 16: {False: "66 31", True: "66 33"}, 32: {False: "31", True: "33"}},
    "INC": {8: "FE 00", 16: "66 FF 00", 32: "FF 00"},
    "DEC": {8: "FE 08", 16: "66 FF 08", 32: "FF 08"},
}

REG_values_of_registers = {  
        "AL": "000", "AX": "000", "EAX": "000",
        "CL": "001", "CX": "001", "ECX": "001",
        "DL": "010", "DX": "010", "EDX": "010",
        "BL": "011", "BX": "011", "EBX": "011",
        "AH": "100", "SP": "100", "ESP": "100",
        "CH": "101", "BP": "101", "EBP": "101",
        "DH": "110", "SI": "110", "ESI": "110",
        "BH": "111", "DI": "111", "EDI": "111"
    }

reg_8 = ["AL", "CL", "DL", "BL", "AH", "CH", "DH", "BH"]
reg_16 = ["AX", "CX", "DX", "BX", "SP", "BP", "SI", "DI"]
reg_32 = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]

supported_instructions = ["ADD", "SUB", "AND", "OR","INC", "DEC", "XOR", "PUSH", "POP" ,"JMP"]

def littlEndian(dstOP):
    res = ""
    hexedReversed = format(int(hex(int(dstOP)), 16), '08X')[::-1]
    
    for i in range(0, len(hexedReversed), 2):
        res += hexedReversed[i+1] + hexedReversed[i] + " "
        
    return res


def getPushCode(dstOP):
    if dstOP in reg_32:
        return binaryToHexConvertor("1010" + REG_values_of_registers[dstOP]).strip()
    elif dstOP in reg_16:
        return "66" + binaryToHexConvertor("1010" + REG_values_of_registers[dstOP])
    elif dstOP.startswith('['):
        return "FF " + binaryToHexConvertor("110" + REG_values_of_registers[dstOP[1:-1]]).strip()
    else:
        if int(dstOP) > 127:
            return "68 " + littlEndian(dstOP)
        else:
            return "6A " + littlEndian(dstOP)[:2]      

def getPopCode(dstOP):
    if dstOP in reg_32:
        return binaryToHexConvertor("1011" + REG_values_of_registers[dstOP]).strip()
    elif dstOP in reg_16:
        return "66" + binaryToHexConvertor("1011" + REG_values_of_registers[dstOP]) 


def getIncCode(dstOP):
    if dstOP in reg_32:
        return binaryToHexConvertor("1000" + REG_values_of_registers[dstOP]).strip()
    elif dstOP in reg_16:
        return "66" + binaryToHexConvertor("1000" + REG_values_of_registers[dstOP])
    else:
        return "FE" + binaryToHexConvertor("11000" + REG_values_of_registers[dstOP])

def getDecCode(dstOP):
    if dstOP in reg_32:
        return binaryToHexConvertor("1001" + REG_values_of_registers[dstOP]).strip()
    elif dstOP in reg_16:
        return "66" + binaryToHexConvertor("1001" + REG_values_of_registers[dstOP])                         
    else:
        return "FE" + binaryToHexConvertor("11001" + REG_values_of_registers[dstOP])


# A function that convert decimal number to hexadecimal.
def decimalToHexConvertor(Decimal):
    
    convertedNumber = str(hex((Decimal) & (2**8-1)))[2:].upper()
    #return  " " + convertedNumber if len(convertedNumber) == 1 else " " + convertedNumber
    return  " " + convertedNumber

# A function that convert binary to hexadecimal.
def binaryToHexConvertor(binaryNumber):
    
    convertedNumber = str(hex(int(binaryNumber, 2)))[2:].upper()
    #return  " " + convertedNumber if len(convertedNumber) == 1 else " " + convertedNumber
    return  " " + convertedNumber


# A function to find REG & R/M byte with the help of REG values of registers.
def REG_RM_builder(dstOP,srcOp):

    if (dstOP.startswith('[') and dstOP.endswith(']') and is_reg(dstOP[1:][:-1])):
        REG = REG_values_of_registers[srcOp]
        RM = REG_values_of_registers[dstOP[1:][:-1]]
        
    elif (srcOp.startswith('[') and srcOp.endswith(']') and is_reg(srcOp[1:][:-1])):
        REG = REG_values_of_registers[dstOP]
        RM = REG_values_of_registers[srcOp[1:][:-1]]
        
    else:
        REG = REG_values_of_registers[srcOp] #d = 0 like shell storm 
        RM = REG_values_of_registers[dstOP]

    return REG + RM


# Mod finder function for distinguishing between memory and register.
def modBuilder(dstOP,srcOp):
    
    if (dstOP.startswith('[') and dstOP.endswith(']')
        and is_reg(dstOP[1:][:-1])) or (srcOp.startswith('[')
                                          and srcOp.endswith(']') and is_reg(srcOp[1:][:-1])):
        return "00"
    else:
        return "11"


# The counter which
def label_looking_counter(testCase,test_cases,destOp):

    counter = 0
    for j in test_cases:
        j = j.split()
        
        if j[0][:-1] == destOp:
            break
        
        else:
            if test_case_validity(testCase) and not j[0].endswith(':'):

                if j[0] == "JMP":
                    counter += 2
                elif j[0] in ["INC", "DEC"]:
                    if j[1] in reg_32:
                        counter += 1
                    else: 
                        counter += 2 
                elif j[0] in ["PUSH", "POP"]: 
                    if j[1] in reg_16:
                        counter += 2 
                    elif j[1] in reg_32:    
                        counter += 1     
                    else:                       #push immediate
                        counter += len(getPushCode(j[1]).strip().split(' '))         
                else:
                    if j[1][:-1] in reg_16 or j[2] in reg_16:
                        counter += 3  
                    else:
                        counter += 2
                
    return counter


# This function return the number of bits of the entered register. 
def x_bits(register_n):
    
    if (register_n.startswith('[') and register_n.endswith(']')) and is_reg(register_n[1:][:-1]):
        register_n = register_n[1:][:-1]
    
    if register_n in reg_8:
        return 8
    
    elif register_n in reg_16:
        return 16
    
    elif register_n in reg_32:
        return 32


# A function that help us with OPCODE-table to build the opcode of the entered instruction.
def opcodeBuilder(instruction,destOp,srcOp):
    if instruction == "JMP":
        return "EB"
    elif instruction in ["PUSH", "POP", "INC", "DEC"]:
        return opcode_table[instruction][x_bits(destOp)]  
    elif srcOp in reg_16 and destOp.startswith('['):
          return opcode_table[instruction][x_bits(srcOp)][srcOp.startswith('[') and srcOp.endswith(']') and is_reg(srcOp[1:][:-1])]
    elif srcOp in reg_8 and destOp.startswith('['):
          return opcode_table[instruction][x_bits(srcOp)][srcOp.startswith('[') and srcOp.endswith(']') and is_reg(srcOp[1:][:-1])]
    else:
        return opcode_table[instruction][x_bits(destOp)][srcOp.startswith('[') and srcOp.endswith(']') and is_reg(srcOp[1:][:-1])]


# This function is the one that turns our test case to machine code
def toMachineCode(instruction,destOp,srcOp,test_cases,thisTestCase, finisherCounter):

    if instruction == "JMP":
        opcode = opcodeBuilder(instruction,destOp,srcOp)
        main_counter_helper = label_looking_counter(thisTestCase,test_cases,destOp) - finisherCounter #length between label and our JMP        
        machine_code = opcode + decimalToHexConvertor(main_counter_helper)

    else:
        if instruction in ["PUSH", "POP", "INC", "DEC"]:
            opcode = opcodeBuilder(instruction, destOp, None)
            machine_code = opcode + " " + REG_values_of_registers[destOp]
        else:
            opcode = opcodeBuilder(instruction,destOp,srcOp)
            MOD = modBuilder(destOp,srcOp)
            REG_RM = REG_RM_builder(destOp,srcOp)
            machine_code = opcode + binaryToHexConvertor(MOD + REG_RM)

    return machine_code


# A function that check if the entered name is a valid Register.
def is_reg(var):
    var = var
    return_value = False
    if var in reg_8 or var in reg_16 or var in reg_32:
        return_value = True
    return return_value


# A function that check if the entered name is a valid Memory.
def is_memory(var):
    return (var.startswith('[') and var.endswith(']')) and is_reg(var[1:][:-1])


# The validity test case checker function.
def test_case_validity(project_test_case):

    if not project_test_case[0] in supported_instructions:
        print("Input:", project_test_case)
        print("Entered instruction is'nt valid!\n")
        return False

    if project_test_case[1].startswith('[') and project_test_case[0] in ["POP", "INC", "DEC"]:
        print("Unsupported Input: " + ' '.join(project_test_case))
        return False       


    two_able_instructions = ["JMP", "PUSH", "POP", "INC", "DEC"]
    three_able_instructions = ["ADD", "SUB", "AND", "OR", "XOR"]
    
    if project_test_case[0] in two_able_instructions:
        if len(project_test_case) != 2:
            print(f"Incorrect number of operands for {project_test_case[0]}'s instruction!\n")
            return False

    elif project_test_case[0] in three_able_instructions:
        if len(project_test_case) != 3:
            print("Input:", project_test_case)
            print(f"Incorrect number of operands for {project_test_case[0]}'s instruction!\n")
            return False

        if not ((is_reg(project_test_case[1][:-1]) or (project_test_case[1][:-1].startswith('[') and
                                                       project_test_case[1][:-1].endswith(']')) and is_reg(project_test_case[1][:-1][1:][:-1])
                                                        ) and ((is_reg(project_test_case[2])
                                                        or (project_test_case[2].startswith('[') and
                                                        project_test_case[2].endswith(']')) and is_reg(project_test_case[2][1:][:-1])))):
            print("Input:", ' '.join(project_test_case))
            print("Invalid type for destination or source operand!\nMust be a valid register or memory.\n")
            return False

        if project_test_case[1].startswith('['):
            if not (project_test_case[1][1:-2] in reg_32):
                print("Addressess must by 32 bit: " + ' '.join(project_test_case))
                return False 

        if project_test_case[2].startswith('['):
            if not (project_test_case[2][1:-1] in reg_32):
                print("Addressess must by 32 bit: " + ' '.join(project_test_case))
                return False     

        if project_test_case[1].startswith('[') and project_test_case[2].startswith('['):
            print("Input:", ' '.join(project_test_case))
            print("Both operands can not be memory!")
            return False

        if is_reg(project_test_case[1][:-1]) and is_reg(project_test_case[2]):
            if x_bits(project_test_case[1][:-1]) != x_bits(project_test_case[2]):
                print("Input:", ' '.join(project_test_case))
                print("Both operands must be the same size!")
                return False
    return True


# A function that help us to make our project file readable.
def read_file():
    input_file = open('inp.txt', 'r')
    test_cases = [test_case[:-1].upper() if test_case.endswith("\n")
             else test_case.upper() for test_case in input_file.readlines()]
    input_file.close()
    return test_cases



def main(terminal, test_cases):
    # A counter to count passed bytes for using in JMP and memory location printed before machine codes
    finisher_counter = 0
    finisher_counter_temp = 0
    finisher_counter_copy = 0
    repeat = 0
    if not terminal:
        test_cases = read_file()

    for i in range(len(test_cases)):
        #finisher_counter_temp = finisher_counter  #for memory location printed before machine codes
        finisher_counter_temp = finisher_counter_copy
        thisTestCase = test_cases[i].split(' ')   
        if not thisTestCase[0].endswith(':') and test_case_validity(thisTestCase):

            if thisTestCase[0] == "JMP":
                finisher_counter += 2
                finisher_counter_copy += 2
                repeat = 2
            elif thisTestCase[0] in ["INC", "DEC"]:
                if thisTestCase[1] in reg_32:
                    finisher_counter += 1
                    finisher_counter_copy += 1
                    repeat = 1
                else: 
                    finisher_counter += 2
                    finisher_counter_copy += 2 
                    repeat = 2
            elif thisTestCase[0] in ["PUSH", "POP"]: 
                if thisTestCase[1] in reg_16:
                    finisher_counter += 2
                    finisher_counter_copy += 2
                    repeat = 2 
                elif thisTestCase[1] in reg_32:    
                    finisher_counter += 1
                    finisher_counter_copy += 1
                    repeat = 1     
                else:                       #push immediate
                    temp = len(getPushCode(thisTestCase[1]).strip().split(' '))
                    finisher_counter += temp
                    finisher_counter_copy += temp
                    repeat = temp
            else:
                if thisTestCase[1][:-1] in reg_16 or thisTestCase[2] in reg_16:
                    finisher_counter += 3
                    finisher_counter_copy += 3
                    repeat = 3 
                else:
                    finisher_counter += 2
                    finisher_counter_copy += 2
                    repeat = 2

                    
            instruction = thisTestCase[0]
            if instruction == "JMP":
                dstOp = thisTestCase[1]
                srcOp = ""
                Mcode = toMachineCode(instruction,dstOp,srcOp,test_cases,thisTestCase, finisher_counter)
            #elif instruction in ["PUSH"] and thisTestCase[1].startswith("["): #we don't support this condition
             #   print("Not Supported")
              #  return
            elif instruction in ["INC", "DEC", "PUSH", "POP"]:
                dstOp = thisTestCase[1]
                if instruction == "PUSH" : 
                    Mcode = getPushCode(dstOp)
                    fillStack(dstOp) #for phase two to add print elements for each push instruction 
                elif instruction == "POP" : 
                    Mcode = getPopCode(dstOp)
                    stackToPrint.pop() #for removing the last element of stack to print
                    stackToPrint.pop()
                    stackToPrint.pop()
                    stackToPrint.pop()
                elif instruction == "INC":
                    Mcode = getIncCode(dstOp)
                    
                elif instruction == "DEC":
                    Mcode = getDecCode(dstOp)
                    
            else:
                dstOp = thisTestCase[1][:-1].upper()
                srcOp = thisTestCase[2].upper()
                Mcode = toMachineCode(instruction,dstOp,srcOp,test_cases,thisTestCase, finisher_counter)

            if Mcode != None:
                if finisher_counter_temp % 2 == 1: # because each instruction should start at an even memory address
                    codeToPrint.append("MM")
                    finisher_counter_copy += 1
                #for i in range(repeat):
                #    codeToPrint.append(Mcode)
                Mcode = Mcode.strip().split(" ")
                Mcode.reverse()
                for i in range(len(Mcode)): #filling codeToPrint in littel endian
                    if len(Mcode[i]) == 1:
                        codeToPrint.append('{:02d}'.format(int(Mcode[i])))
                    else:
                        codeToPrint.append(Mcode[i])

                #print(str(hex(finisher_counter_temp)) + ":   ", Mcode, "      (" + test_cases[i] + ")" , end="\n--------------------------------------\n")
 
#function to read and add data print elements
def read__and_fill_data():
    input_file = open('inp.txt', 'r')
    dataReadFlag = False
    while True:
        if dataReadFlag == True: break

        line = input_file.readline()
        if ".DATA" in line.upper():
            while True:
                dataLine = input_file.readline().strip()
                if ".STACK" in dataLine.upper() or ".CODE" in dataLine.upper():
                    dataReadFlag = True
                    break

                if dataLine.endswith("\n"):
                    dataLine = dataLine.split(' ')[:-1]
                else:
                    dataLine = dataLine.split(' ')

                if dataLine[1].upper() == "BYTE":
                    dataToPrint.append(dataLine[0])
                if dataLine[1].upper() == "WORD":
                    dataToPrint.append(dataLine[0])
                    dataToPrint.append(dataLine[0])
                if dataLine[1].upper() == "DWORD":
                    dataToPrint.append(dataLine[0])
                    dataToPrint.append(dataLine[0])
                    dataToPrint.append(dataLine[0])
                    dataToPrint.append(dataLine[0])
    input_file.close() 


def fillStack(dstOP):
    if dstOP in reg_32:
        stackToPrint.append(dstOP) #for phase2
        stackToPrint.append(dstOP) #for phase2
        stackToPrint.append(dstOP) #for phase2
        stackToPrint.append(dstOP) #for phase2
    elif dstOP in reg_16:
        stackToPrint.append(dstOP) #for phase2
        stackToPrint.append(dstOP) #for phase2
        stackToPrint.append("MM") #for phase2
        stackToPrint.append("MM") #for phase2

    elif dstOP.startswith('['):
        what = "TODO"
    else:
        if int(dstOP) < 256:
                stackToPrint.append(dstOP) #for phase2
                stackToPrint.append("MM") #for phase2
                stackToPrint.append("MM") #for phase2
                stackToPrint.append("MM") #for phase2
        elif int(dstOP) < 65536:
            stackToPrint.append(dstOP) #for phase2
            stackToPrint.append(dstOP) #for phase2
            stackToPrint.append("MM") #for phase2
            stackToPrint.append("MM") #for phase2
        elif int(dstOP) < 4294967296:
            stackToPrint.append(dstOP) #for phase2
            stackToPrint.append(dstOP) #for phase2
            stackToPrint.append(dstOP) #for phase2
            stackToPrint.append(dstOP) #for phase2

#a function to extract labeles that JMP was used on in the code and add to data segment
def read_and_add_labelnames():
    input_file = open('inp.txt', 'r')
    while True:
        line = input_file.readline().strip()
        if line == "":
            break 

        line = line.split(" ")
        if line[0].upper() == "JMP":
            dataToPrint.append(line[1])
    input_file.close()  


#function for making the 32 byte of each segment MM and fill the finalPrint with stack and data and codeto print
def makeFinal(stackIndex, codeIndex, dataIndex):

    for i in range(stackIndex, stackIndex + 32):
        finalPrint[i] = "MM"
    for i in range(dataIndex, dataIndex + 32):    
        finalPrint[i] = "MM"
    for i in range(codeIndex, codeIndex + 32):
        finalPrint[i] = "MM"

    j = 0
    for i in range(stackIndex, stackIndex + len(stackToPrint)):
        finalPrint[i] = stackToPrint[j]
        j += 1
    j = 0
    for i in range(dataIndex, dataIndex + len(dataToPrint)):
        finalPrint[i] = dataToPrint[j]
        j += 1
    j = 0
    for i in range(codeIndex, codeIndex + len(codeToPrint)):
        finalPrint[i] = codeToPrint[j]
        j += 1

def printFinal(stackIndex, codeIndex, dataIndex):
    for i in range(len(finalPrint)):
        if i == 0:
            print("          ----", end="")
            for j in range(len(finalPrint[i])):
                print("-", end="")
            print("----")


        if i == codeIndex:
            toPrint = finalPrint[i]
            if i+1 != len(finalPrint) and len(finalPrint[i]) < len(finalPrint[i+1]):
                toPrint = finalPrint[+1]
            print("CS  " + '{:03d}'.format(i) + ":" + " |    " + finalPrint[i] + "    |")
            print("          ----", end="")
            for j in range(len(toPrint)):
                print("-", end="")
            print("----")


        elif i == stackIndex:
            toPrint = finalPrint[i]
            if i+1 != len(finalPrint) and len(finalPrint[i]) < len(finalPrint[i+1]):
                toPrint = finalPrint[i+1]
            print("SS  " + '{:03d}'.format(i) + ":" + " |    " + finalPrint[i] + "    |")
            print("          ----", end="")
            for j in range(len(toPrint)):
                print("-", end="")
            print("----")


        elif i == dataIndex:
            toPrint = finalPrint[i]
            if i+1 != len(finalPrint) and len(finalPrint[i]) < len(finalPrint[i+1]):
                toPrint = finalPrint[i+1]
            print("DS  " + '{:03d}'.format(i) + ":" + " |    " + finalPrint[i] + "    |")
            print("          ----", end="")
            for j in range(len(toPrint)):
                print("-", end="")
            print("----")


        else:
            toPrint = finalPrint[i]
            if i+1 != len(finalPrint) and len(finalPrint[i]) < len(finalPrint[i+1]):
                toPrint = finalPrint[i+1]
            print("    " + '{:03d}'.format(i) + ":" + " |    " + finalPrint[i] + "    |")
            print("          ----", end="")
            for j in range(len(toPrint)):
                print("-", end="")
            print("----")


stackIndex = 0
dataIndex = 0
codeIndex = 0

stackToPrint = []
dataToPrint = []
codeToPrint = []

finalPrint = ["XX"] * 256   #not part of a segment = "XX"


def main2():
    lines = read_file()
    test_cases = []
    read__and_fill_data() #to handel .data
    read_and_add_labelnames() #to add labels to data segment

    #for loop to determin the memory address of each data or stack or code segment
    for i in range(len(lines)):
        if ".STACK" in lines[i]:
            stackIndex = int(lines[i].strip()[7:-1])
        if ".DATA" in lines[i]:
            dataIndex = int(lines[i].strip()[6:-1])
        if ".CODE" in lines[i]:
            codeIndex = int(lines[i].strip()[6:-1])
            for j in range(i+1, len(lines)):
                test_cases.append(lines[j].strip())
    
    main(True, test_cases)
    makeFinal(stackIndex, codeIndex, dataIndex)
    printFinal(stackIndex, codeIndex, dataIndex)


# BOOM BOOM !
main2() 
    






