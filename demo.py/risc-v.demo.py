import sys

class RISCVSimulator:
    def __init__(self, memory_size=0x10000):
        self.registers = [0] * 32
        self.memory = bytearray(memory_size)
        self.pc = 0

    def load_program(self, program):
        self.memory[:len(program)] = program

    def fetch(self):
        instr = int.from_bytes(self.memory[self.pc:self.pc+4], 'little')
        self.pc += 4
        return instr

    def decode_execute(self, instr):
        opcode = instr & 0x7F
        rd = (instr >> 7) & 0x1F
        rs1 = (instr >> 15) & 0x1F
        rs2 = (instr >> 20) & 0x1F
        imm = (instr >> 20)

        if opcode == 0x13:  # ADDI
            self.registers[rd] = self.registers[rs1] + imm

        elif opcode == 0x33:  # ADD
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]

        elif opcode == 0x37:  # LUI
            self.registers[rd] = imm << 12

        elif opcode == 0x63:  # BEQ
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += imm << 1

        else:
            print(f"Error: Unsupported opcode 0x{opcode:x}")
            sys.exit(1)

    def run(self):
        while self.pc < len(self.memory):
            instr = self.fetch()
            self.decode_execute(instr)


# 示例程序: 计算 3 + 5，结果存储在寄存器 x1 中
program = [
    0x93, 0x01, 0x00, 0x00,  # addi x1, x0, 3
    0x93, 0x02, 0x05, 0x00,  # addi x2, x0, 5
    0x33, 0x01, 0x01, 0x00,  # add x1, x1, x2
]

simulator = RISCVSimulator()
simulator.load_program(program)
simulator.run()

print("Result in register x1:", simulator.registers[1])
