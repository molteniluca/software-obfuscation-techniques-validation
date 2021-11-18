	.file	"fibonacci.c"
	.text
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
	leaq	0(,%rax,4), %r9
	movl	$0, 0(,%rax,4)
	movl	$1, 4(,%rax,4)
	cmpl	$1, %edi
	jle	.L2
	movq	%r9, %rsi
	movl	$2, %eax
.L3:
	movslq	%eax, %r8
	leal	-1(%rax), %ecx
	movslq	%ecx, %rcx
	leal	-2(%rax), %edx
	movslq	%edx, %rdx
	movl	(%rsi,%rdx,4), %edx
	addl	(%rsi,%rcx,4), %edx
	movl	%edx, (%rsi,%r8,4)
	addl	$1, %eax
	cmpl	%eax, %edi
	jge	.L3
.L2:
	movslq	%edi, %rdi
	movl	(%r9,%rdi,4), %eax
	movq	-8(%rbp), %rdi
	xorq	%fs:40, %rdi
	je	.L4
	call	__stack_chk_fail
.L4:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE23:
	.size	fib, .-fib
	.globl	main
	.type	main, @function
main:
.LFB24:
	.cfi_startproc
	movl	$0, %eax
	ret
	.cfi_endproc
.LFE24:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
