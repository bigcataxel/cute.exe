	.intel_syntax noprefix
.LC0:
stealth_msg_12:
	push	rbp
	mov	rbp, rsp
	lea	rax, .LC0[rip]
	mov	QWORD PTR -8[rbp], rax
	mov	rcx, QWORD PTR -8[rbp]
#APP
# 4 "raw_c/syscall_write_12.c" 1
	mov rax, 1; mov rdi, 1; mov rsi, rcx; mov rdx, 6; syscall;
# 0 "" 2
#NO_APP
	nop
	pop	rbp
	ret
0:
1:
2:
3:
4:
