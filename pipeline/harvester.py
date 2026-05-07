import os

def generate_dataset():
    if not os.path.exists("raw_c"):
        os.makedirs("raw_c")
    
    # Modèles de code pour le DNS Tunneling et les Syscalls
    templates = [
        ("dns_core_{i}.c", """
void dns_build_{i}(unsigned char *b) {{
    b[0] = 0x{i:02x}; b[1] = 0xAA; // ID
    b[2] = 0x01; b[3] = 0x00; // Standard Query
    for(int i=4; i<12; i++) b[i] = 0; 
}}"""),
        ("syscall_write_{i}.c", """
void stealth_msg_{i}() {{
    const char *m = "MSG_{i}\\n";
    asm volatile("mov rax, 1; mov rdi, 1; mov rsi, %0; mov rdx, 6; syscall;" : : "r"(m) : "rax","rdi","rsi","rdx");
}}""")
    ]

    for i in range(10, 30):
        for name, code in templates:
            with open(f"raw_c/{name.format(i=i)}", "w") as f:
                f.write(code.format(i=i))
    print("✅ 40 nouveaux fichiers C (DNS/Syscalls) générés dans raw_c/")

if __name__ == "__main__":
    generate_dataset()