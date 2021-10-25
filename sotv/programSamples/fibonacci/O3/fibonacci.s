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
	leaq	0(,%rax,4), %rsi
	movl	$0, 0(,%rax,4)
	movl	$1, 4(,%rax,4)
	jle	.L6
	cmpl	$3, %edi
	jle	.L8
	leal	-4(%rdi), %eax
	leaq	8(%rsi), %rdx
	xorl	%r8d, %r8d
	movl	$1, %ecx
	shrl	%eax
	leal	4(%rax,%rax), %r9d
	movl	$2, %eax
	.p2align 4,,10
	.p2align 3
.L4:
	addl	%ecx, %r8d
	addl	$2, %eax
	addq	$8, %rdx
	addl	%r8d, %ecx
	movl	%r8d, -8(%rdx)
	movl	%ecx, -4(%rdx)
	cmpl	%r9d, %eax
	jne	.L4
	.p2align 4,,10
	.p2align 3
.L5:
	leal	-2(%rax), %ecx
	leal	-1(%rax), %edx
	movslq	%eax, %r8
	addl	$1, %eax
	movslq	%ecx, %rcx
	movslq	%edx, %rdx
	movl	(%rsi,%rdx,4), %edx
	addl	(%rsi,%rcx,4), %edx
	cmpl	%eax, %edi
	movl	%edx, (%rsi,%r8,4)
	jge	.L5
.L6:
	movslq	%edi, %rdi
	movl	(%rsi,%rdi,4), %eax
	movq	-8(%rbp), %rdi
	xorq	%fs:40, %rdi
	jne	.L15
	leave
	.cfi_remember_state
	.cfi_def_cfa 7, 8
	ret
.L8:
	.cfi_restore_state
	movl	$2, %eax
	jmp	.L5
.L15:
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
