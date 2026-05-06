	.intel_syntax noprefix
dns_build_13:
	push	rbp
	mov	rbp, rsp
	mov	QWORD PTR -24[rbp], rdi
	mov	rax, QWORD PTR -24[rbp]
	mov	BYTE PTR [rax], 13
	mov	rax, QWORD PTR -24[rbp]
	add	rax, 1
	mov	BYTE PTR [rax], -86
	mov	rax, QWORD PTR -24[rbp]
	add	rax, 2
	mov	BYTE PTR [rax], 1
	mov	rax, QWORD PTR -24[rbp]
	add	rax, 3
	mov	BYTE PTR [rax], 0
	mov	DWORD PTR -4[rbp], 4
	jmp	.L2
.L3:
	mov	eax, DWORD PTR -4[rbp]
	movsx	rdx, eax
	mov	rax, QWORD PTR -24[rbp]
	add	rax, rdx
	mov	BYTE PTR [rax], 0
	add	DWORD PTR -4[rbp], 1
.L2:
	cmp	DWORD PTR -4[rbp], 11
	jle	.L3
	nop
	nop
	pop	rbp
	ret
0:
1:
2:
3:
4:
