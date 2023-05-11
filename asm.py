#!/usr/bin/python3

"""
Fatima Mehdi
Project 1
CS-UY 2214
Jeff Epstein
asm.py
"""

import argparse

def handle_labels(filename):
  """
    Find a label in a file, store it in a dictionary.
    Label is a dictionary where:
    {key:value} -> {label:address}
    Parameters:
        filename: assemble file
    For example: 
        >>> handle_labels(filename) 
    I am additionally incrementing my address, 
    hence keeping track of pc.
  """
  labels = {}
  address = 0
  #{key:value}
  #{label:address}
  
  with open(filename) as f:
    for line in f:
      line = line.split("#",1)[0].strip() 
      new_list = line.split(":")

      # no labels: single elements
      
      for i in new_list[:-1]:
        i = i.strip()
        #key = i
        labels[i] = address
        
      #increment address when we dont have label  , 
      if new_list[-1] != "":
        address += 1
        
  return labels

def get_elements(line):
  ''' 
  get_elements(line)
  Takes your instruction line and stores each part in a list.

  Parameters:
    line -> str
  '''
  line = line.split(",")
  split_args = line[0].split()
  if len(split_args) == 1:
    return split_args
  elements = [split_args[0], split_args[1]]
  for word in line[1:]:
    elements.append(word.strip())
  return elements
  
def assemble(line,labels, address):
  '''
  Assemble a line of code, access labels dictionary,
  and address.
  Parameters:
    line  -> string
    labels -> key:value
  '''
  op = 0
  opcode = line.split()[0]
  elements = get_elements(line)
  
  if opcode == "add":
    return assemble_add(elements)
  elif opcode == "sub":
    return assemble_sub(elements)
  elif opcode == "or":
    return assemble_or(elements)
  elif opcode == "and":
    return assemble_and(elements)
  elif opcode == "slt":
    return assemble_slt(elements)
  elif opcode == "jr":
    return assemble_jr(elements)
  elif opcode == "slti":
    return assemble_slti(elements, labels)
  elif opcode == "lw":
    return assemble_lw(elements, labels)
  elif opcode == "sw":
    return assemble_sw(elements, labels)
  elif opcode == "jeq":
    return assemble_jeq(elements, labels, address)
  elif opcode == "addi":
    return assemble_addi(elements, labels)
  elif opcode == "j":
    return assemble_j (elements, labels)
  elif opcode == "jal":
    return assemble_jal(elements,labels)
  elif opcode =="movi":
    return assemble_movi(elements, labels)
  elif opcode == "nop":
    return assemble_nop()
  elif opcode == "halt":
    return assemble_halt(address)
  else:
    return assemble_fill(elements, labels)  
  return op

def make_int(number, bitwidth):
  ''' 
  make_int(number, bitwidth)
  Parameters:
    Number -> Str
    Bitwidth - > int : describes how large the bitwidth should be
  '''
  return int(number) % (2**bitwidth)
  
def get_registers(elements):
  ''' 
  cleans a list of elements that stores the registers, in order, in a list.
  Paramter:
    elements -> lst: of items in line 
  '''
  reg_list = [] #list of registers in order
  for i in elements:
    if i[0] == "$":
      reg_list.append(int(i[1:]))
  return reg_list

#Functions that take 3 register arguments
def assemble_add(elements):
  ''' 
    Applied add instruction.
    add $regDst, $regSrcA, $regSrcB
  '''
  reg_list = get_registers(elements)
  return (0 << 13) | (reg_list[1]<< 10) | (reg_list[2] << 7) | (reg_list[0]<<4) | 0

def assemble_sub(elements):
  ''' 
  sub: Subtract
  sub $regDst, $regSrcA, $regSrcB
  '''
  reg_list = get_registers(elements)
  return (0 << 13) | (reg_list[1]<< 10) | (reg_list[2] << 7) | (reg_list[0]<<4) | 1

def assemble_or(elements):
  '''
  or: or 
  or $regDst, $regSrcA, $regSrcB
  '''
  reg_list = get_registers(elements)
  return (0 << 13) | (reg_list[1]<< 10) | (reg_list[2] << 7) | (reg_list[0]<<4) | 0b0010  
def assemble_and(elements):
  '''
   and $regDst, $regSrcA, $regSrcB
   '''
  reg_list = get_registers(elements)
  return (0 << 13) | (reg_list[1]<< 10) | (reg_list[2] << 7) | (reg_list[0]<<4) | 0b0011

def assemble_slt(elements):
  '''
  slt = set if less than
  slt $regDst, $regSrcA, $regSrcB
  '''
  reg_list = get_registers(elements)
  return (0 << 13) | (reg_list[1]<< 10) | (reg_list[2] << 7) | (reg_list[0]<<4) | 0b0100

def assemble_jr(elements):
  '''
  jr = jump to register
  jr $reg
  '''
  reg_list = get_registers(elements)
  return (reg_list[0]<<10) | 0b1000

def get_immediate(imm, labels): 
  if imm in labels:
    imm = labels[imm]
  else:
    imm = int(imm)
  return imm
  
def make_assemble_7bit_imm(imm, labels):
  return make_int(get_immediate(imm,labels), 7)
  
def make_assemble_13bit_imm(imm, labels):
  return make_int(get_immediate(imm,labels), 13)

#instructions with 2 register arguments 
def assemble_slti(elements, labels):
  '''
  slti = set if less thann, immediate
  slti $regDst, $regSrc, imm
  '''
  reg_list = get_registers(elements)
  imm = make_assemble_7bit_imm(elements[-1], labels)
  return (0b111<< 13) | (reg_list[1] << 10) | (reg_list[0] << 7) | imm

def assemble_lw(elements, labels):
  '''
  lw = oad word
  lw $regDst, imm($regAddr)
  '''
  last_thing = elements[-1]
  bad = last_thing.split("(") 
  imm = make_assemble_7bit_imm(bad[0].strip(), labels)
  reg_addr = int(bad[1].strip()[1])
  reg_Dst = int(elements[1][1])
  
  return (0b100 << 13) | (reg_addr << 10) | (reg_Dst << 7 )| imm
  

def assemble_sw(elements, labels):
  '''
  sw = store word
  sw $regSrc, imm($regAddr)
  '''
  sw_list = elements[-1]
  a_new_lst = sw_list.split("(")
  imm = make_assemble_7bit_imm(a_new_lst[0].strip(), labels)
  reg_Addr_sw = int(a_new_lst[1].strip()[1])
  reg_src_sw = int(elements[1][1])
  return (0b101 << 13) |(reg_Addr_sw << 10) | (reg_src_sw  << 7 )| imm

def assemble_jeq(elements, labels, address):
  '''
  jeq = jump if equal to
  jeq $regA, $regB, imm
  '''
  reg_list = get_registers(elements)
  imm = get_immediate(elements[-1], labels)
  rel_imm = imm - address - 1
  rel_imm = make_int(rel_imm, 7)

  return (0b110 << 13) |(reg_list[0]<< 10) | (reg_list[1] << 7 )| rel_imm

def assemble_addi(elements, labels):
  '''
  addi = add immediate
  addi $regDst, $regSrc, imm
  '''
  reg_list = get_registers(elements)
  imm = make_assemble_7bit_imm(elements[-1], labels)
  return (0b001 << 13) | (reg_list[1]<< 10) | (reg_list[0]<< 7) | imm

#Instructions with no register arguments
def assemble_j(elements, labels):
  '''
  j = jump
  j imm
  '''
  imm = make_assemble_13bit_imm(elements[-1], labels)
  return (0b010 << 13) | imm

def assemble_jal(elements, labels):
  '''
  jal = jump and link
  jal imm
  '''
  imm = make_assemble_13bit_imm(elements[-1], labels)
  return (0b011 << 13) | imm

def assemble_movi(elements, labels):
  ''' 
  Movi: Move Immediate
  movi $reg, imm
  '''
  reg_list = get_registers(elements)
  imm = make_assemble_7bit_imm(elements[-1], labels)
  return (0b001 << 13) | (0 << 10) | (reg_list[0]<< 7) | imm


def assemble_nop():
  '''
  nop = no operation
  '''
  return 0
  
def assemble_halt(address):
  '''
  No operation. Transalated by j.
  '''
  return (0b010 << 13) | address

def assemble_fill(elements,labels):
  return get_immediate(elements[-1], labels)
  
def print_machine_code(address, num):
    """
    print_line(address, num)
    Print a line of machine code in the required format.
    Parameters:
        address: int = RAM address of the instructions
        num: int = numeric value of machine instruction 

    For example: 
        >>> print_machine_code(3, 42)
        ram[3] = 16'b0000000000101010;    
    """
    instruction_in_binary = format(num,'016b')
    print("ram[%s] = 16'b%s;" % (address, instruction_in_binary))


def main():
    parser = argparse.ArgumentParser(description='Assemble E20 files into machine code')
    parser.add_argument('filename', help='The file containing assembly language, typically with .s suffix')
    cmdline = parser.parse_args()
    
    
    labels = handle_labels(cmdline.filename)
    

    # our final output is a list of ints values representing
    # machine code instructions
    instructions=[]

    # iterate through the line in the file, construct a list
    # of numeric values representing machine code

    with open(cmdline.filename) as f:
        for line in f:
            line = line.split("#",1)[0].strip()    # remove comments
            line = line.split(":")[-1].strip()
          
            if line == "":
              continue
             
            instructions.append(assemble(line, labels, len(instructions)))  # TODO change this. generate the machine code

    
    # # print out each instruction in the required format
    for address, instruction in enumerate(instructions):
        print_machine_code(address, instruction) 

  
if __name__ == "__main__":
    main()

#ra0Eequ6ucie6Jei0koh6phishohm9

#python ./main.py ./loop2.s
