
void stealth_msg_24() {
    const char *m = "MSG_24\n";
    asm volatile("mov rax, 1; mov rdi, 1; mov rsi, %0; mov rdx, 6; syscall;" : : "r"(m) : "rax","rdi","rsi","rdx");
}