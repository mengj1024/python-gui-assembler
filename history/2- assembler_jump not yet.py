"""
"""

from tkinter import *
import tkinter.filedialog
from tkinter.filedialog import askopenfilename
root = Tk()
root.title("G7 assembler")
#root.geometry("500x500")
root.resizable(width=False,height=False)
opcode =                    {
                                            'R-TYPE' : { #function this case
                                                    'add': 32,
                                                    'and': 36,
                                                    'or': 37,
                                                    'sub': 34,
                                                    'sll': 0,
                                                    'slt': 42,
                                                    'srl' : 2,
                                                    'jr': 8,
                                                    'nor' : 39
                                            },
                                            'I-TYPE': {
                                                    'addi': 8,
                                                    'andi': 12,
                                                    'ori': 13,
                                                    'slti': 10,
                                                  # 'subi': 7, ##??
                                                    'lw': 35,
                                                    'sw': 43,
                                                    'lui': 15,
                                                    'lb': 32,
                                                    'sb': 40,
                                                    'lh': 33,
                                                    'sh': 41,
                                                    'beq': 4,
                                                    'bne': 5
                                            },
                                            'J-TYPE': {
                                                    'j': 2,
                                                    'jal': 3
                                            }
                            }
REGISTERS = {
        '$zero': '0',
        '$at': '1',
        '$v0': '2',
        '$v1': '3',
        '$a0': '4',
        '$a1': '5',
        '$a2': '6',
        '$a3': '7',
        '$t0': '8',
        '$t1': '9',
        '$t2': '10',
        '$t3': '11',
        '$t4': '12',
        '$t5': '13',
        '$t6': '14',
        '$t7': '15',
        '$s0': '16',
        '$s1': '17',
        '$s2': '18',
        '$s3': '19',
        '$s4': '20',
        '$s5': '21',
        '$s6': '22',
        '$s7': '23',
        '$t8': '24',
        '$t9': '25',
        '$k0': '26',
        '$k1': '27',
        '$gp': '28',
        '$sp': '29',
        '$fp': '30',
        '$ra': '31'
        }
def get_key_from_val(dicto,val):
    return list(dicto.keys())[list(dicto.values()).index(val)]
def label_to_num(ins_list):
    label = ':'
    label_count = 0
    num =0 ##returnee
    global labels
    global adr_count
    if(ins_list.__len__()>2):
        label = ins_list[3]+label
        label_count = get_key_from_val(labels,label)
        num = int(label_count) - (int(adr_count)+1)
    else: 
        pass
    return num

def fill_labels(lb_dict): ##old labels in machine
    fob = open("machine.txt",'r')
    mls = fob.readlines()
    fob.close()
    global adr_count
    for ml in mls:
        if("//" in ml):
            temp_l = ml.split("//")
            temp_s = temp_l[1]
            temp_s = temp_s.replace('\n','')
            lb_dict[str(adr_count)]=temp_s
        else:
            adr_count = adr_count+1
    return lb_dict

def handle_label(ins_list): ##new labels -> removes labels from ins and adds it to dict labels
    global labels
    global adr_count
    local_count = adr_count
    for i,line in enumerate(ins_list):
        t = line.split()
        if(not(t[0] in opcode['R-TYPE'] or t[0] in opcode['I-TYPE'] or t[0] in opcode['J-TYPE'])):
            labels[str(local_count)]=t[0]
            if(t.__len__()>1):
                t=line.split(t[0]+' ') ##removing label
                line = t[1]
                local_count += 1
            else:
                line = ''
            ##change current line in ins_list
            ins_list[i] = line
        else:
            local_count += 1
    return ins_list
    
def ask_open_file(event):
    filename = askopenfilename(parent=root,filetypes=[("Text files","*.txt")])
    assembly_f = open(filename,'r')
    assembly_list = assembly_f.readlines()
    assembly_lines = ''.join(assembly_list)
    entry.replace("1.0","end-1c",assembly_lines)
    assembly_f.close()
    
def add_zeros_32(mc):
    zes = ''
    if(mc.__len__()<32):
        diff = 32 - mc.__len__()
        zes = '0'*diff
    return (zes + mc)

def read_Entry(event):
    global labels
    labels = {}
    global adr_count
    adr_count = 0
    if(is_added.get()== True):
        labels = fill_labels(labels) ##also upadates adr_count
    #print(labels,adr_count)
    lines = entry.get("1.0","end-1c")
    if(lines!=''):
        lines_list = lines.split('\n')
        old_labels = labels
        lines_list = handle_label(lines_list) #new labels dealing, adr_count,labels is updated
        print(labels)
        mc_list = []
        for i,line in enumerate(lines_list) :
            if(line!=''):
                line = to_Machine(line)
                temp = line.split('0b')
                line = temp[1]
                ##adding zeros to the left
                line = add_zeros_32(line)
                ## if address in labels dict put comment in machine
                #print(adr_count,labels)
                if(str(adr_count) in labels and not(str(adr_count) in old_labels and i==0 and adr_count>0)): ##related , excluding if label is old and appending
                    #print(adr_count)
                    line = '//'+labels[str(adr_count)]+'\n'+line
                mc_list.append(line)
                adr_count+=1
            elif(str(adr_count) in labels and (i==lines_list.__len__()-1)):##deleted_last_label
                #print(adr_count)
                mc_list.append('//'+labels[str(adr_count)])
        if(is_added.get()==True):
            mode = 'a'
        else :
            mode = 'w'
        fob = open("machine.txt",mode)
        for mc in mc_list:
            fob.write(mc+'\n')
        fob.close
    
def to_Machine(ins) :
    ins = ins.replace(',','') #removing commas
    ins = ins.replace('(',' ') #removing bracket
    ins = ins.replace(')','') #removing bracket
    l = ins.split()
    machine = 0
    ## most cases size of l = 4
    if( l.__len__()==4):
        if(opcode['R-TYPE'].get(l[0]) or opcode['R-TYPE'].get(l[0])==0):
            #print("R type")
            ##fn
            machine = machine + opcode['R-TYPE'][l[0]] ##function in reality
            ##sh_amt
            if(l[0]=='sll' or l[0]=='srl'):
             machine = machine + (int(l[3]))* (2**6)
            else:
             pass
            ##rd
            machine = machine + (int(REGISTERS[l[1]]))* (2**11)
            ##rt
            if(l[0]=='sll' or l[0]=='srl'):
             machine = machine + (int(REGISTERS[l[2]]))* (2**16)
            else:
             machine = machine + (int(REGISTERS[l[3]]))* (2**16)
            ##rs
            if(l[0]=='sll' or l[0]=='srl'):
             pass
            else:
             machine = machine + (int(REGISTERS[l[2]]))* (2**21)
            return(bin(machine))
        if(opcode['I-TYPE'].get(l[0]) or opcode['I-TYPE'].get(l[0])==0):
            #print("I type")
            ##2 categs num is last or before last
            if(l[0]=='slti' or l[0]=='addi' or l[0]=='andi' or l[0]=='ori' or l[0]=='beq' or l[0]=='bne'):
             #const
             if(l[0]=='beq' or l[0]=='bne'):
              machine = machine + label_to_num(l)
              print(label_to_num(l))
             else:
              machine = machine + (int(l[3]))
             #rt
             machine = machine + (int(REGISTERS[l[1]]))* (2**16)
             #rs
             machine = machine + (int(REGISTERS[l[2]]))* (2**21)
             #op
             machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
             return(bin(machine))
            else:##second cat contains lw, sw,...
             #const
             machine = machine + (int(l[2]))
             #rt
             machine = machine + (int(REGISTERS[l[1]]))* (2**16)
             #rs
             machine = machine + (int(REGISTERS[l[3]]))* (2**21)
             #op
             machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
             return(bin(machine))
    elif(l.__len__() ==2):   ## special cases when size of l = 2 (j,jr,jal)
        if(l[0]=='jr'):
            ##funct
            machine = machine + opcode['R-TYPE'][l[0]]
            ##rs
            machine = machine + (int(REGISTERS[l[1]]))* (2**21)
        else: #j,jal
            #const
            machine = machine + (int(l[1]))
            #op_code
            machine = machine + (opcode['J-TYPE'][l[0]]) * (2**26)
        return(bin(machine))
    elif(l.__len__()==3):  ##lui
        #const
        machine = machine + (int(l[2]))
        #rt
        machine = machine + (int(REGISTERS[l[1]]))* (2**16)
        #op
        machine = machine + (opcode['I-TYPE'][l[0]])* (2**26)
        return(bin(machine))
    
                                      
    
Label(root,text = "write assembly instructions",padx=5,pady = 5).grid(row=1)
ask_open = Button(root,text = 'or import from file ..')
ask_open.grid(row=2)
ask_open.bind("<Button-1>",ask_open_file)
entry = Text(root,width=30,height=7)
entry.grid(row=3,column =0,columnspan = 3,sticky = E + W )
entry.config(undo=True)
scroll = Scrollbar(command=entry.yview)
entry['yscrollcommand'] = scroll.set
scroll.grid(row=3,column=3,sticky='nsew')
add = Button(root,text = "CONVERT!")
is_added= BooleanVar()
append = Checkbutton(root, text="append", variable=is_added)
add.grid(row=4,column=1,columnspan=3,sticky= E + W)
append.grid(row=4,column=0,sticky= E + W)
add.bind("<Button-1>",read_Entry)
root.mainloop()
