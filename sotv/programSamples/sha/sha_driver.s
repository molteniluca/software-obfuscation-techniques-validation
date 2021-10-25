	.file	"sha_driver.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"rb"
.LC1:
	.string	"input_small.asc"
.LC2:
	.string	"error opening %s for reading\n"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB3:
	.section	.text.startup,"ax",@progbits
.LHOTB3:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB60:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	movq	%rsi, %rbp
	movl	$.LC1, %edi
	movl	$.LC0, %esi
	subq	$200, %rsp
	.cfi_def_cfa_offset 224
	movq	%fs:40, %rax
	movq	%rax, 184(%rsp)
	xorl	%eax, %eax
	call	fopen
	testq	%rax, %rax
	je	.L7
	movq	%rax, %rsi
	movq	%rsp, %rdi
	movq	%rax, %rbx
	call	sha_stream
	movq	%rsp, %rdi
	call	sha_print
	movq	%rbx, %rdi
	call	fclose
.L3:
	xorl	%eax, %eax
	movq	184(%rsp), %rcx
	xorq	%fs:40, %rcx
	jne	.L8
	addq	$200, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L7:
	.cfi_restore_state
	movq	0(%rbp), %rdx
	movl	$.LC2, %esi
	movl	$1, %edi
	xorl	%eax, %eax
	call	__printf_chk
	jmp	.L3
.L8:
	call	__stack_chk_fail
	.cfi_endproc
.LFE60:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE3:
	.section	.text.startup
.LHOTE3:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
