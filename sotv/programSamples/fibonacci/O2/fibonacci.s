	.file	"fibonacci.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	fib
	.type	fib, @function
fib:
.LFB23:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leal	2(%rdi), %eax
	cltq
	leaq	18(,%rax,4), %rax
	andq	$-16, %rax
	subq	%rax, %rsp
	leaq	3(%rsp), %rax
	shrq	$2, %rax
	cmpl	$1, %edi
	leaq	0(,%rax,4), %r8
	movl	$0, 0(,%rax,4)
	movl	$1, 4(,%rax,4)
	jle	.L2
	leal	-2(%rdi), %edx
	leaq	8(%r8), %rax
	xorl	%ecx, %ecx
	leaq	8(%r8,%rdx,4), %rsi
	movl	$1, %edx
	jmp	.L3
	.p2align 4,,10
	.p2align 3
.L9:
	movl	-4(%rax), %ecx
	addq	$4, %rax
.L3:
	addl	%ecx, %edx
	cmpq	%rsi, %rax
	movl	%edx, (%rax)
	jne	.L9
.L2:
	movslq	%edi, %rdi
	movl	(%r8,%rdi,4), %eax
	movq	-8(%rbp), %rdi
	xorq	%fs:40, %rdi
	jne	.L10
	leave
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
.L10:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE23:
	.size	fib, .-fib
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.section	.text.startup,"ax",@progbits
.LHOTB1:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB24:
	.cfi_startproc
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE24:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE1:
	.section	.text.startup
.LHOTE1:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
