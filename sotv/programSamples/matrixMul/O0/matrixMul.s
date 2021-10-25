	.file	"matrixMul.c"
	.text
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$40, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -40(%rbp)
	movl	%esi, -44(%rbp)
	cmpl	$0, -44(%rbp)
	je	.L2
	movl	$0, -20(%rbp)
	jmp	.L3
.L4:
	movl	-20(%rbp), %eax
	cltq
	leaq	0(,%rax,4), %rdx
	movq	-40(%rbp), %rax
	addq	%rax, %rdx
	movl	-20(%rbp), %eax
	movl	%eax, (%rdx)
	addl	$1, -20(%rbp)
.L3:
	cmpl	$4, -20(%rbp)
	jle	.L4
	jmp	.L8
.L2:
	movl	$0, -20(%rbp)
	jmp	.L6
.L7:
	movl	-20(%rbp), %eax
	cltq
	leaq	0(,%rax,4), %rdx
	movq	-40(%rbp), %rax
	leaq	(%rdx,%rax), %rbx
	movl	$0, %eax
	call	rand
	movl	%eax, (%rbx)
	addl	$1, -20(%rbp)
.L6:
	cmpl	$4, -20(%rbp)
	jle	.L7
.L8:
	nop
	addq	$40, %rsp
	popq	%rbx
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	fill_array, .-fill_array
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$352, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$0, -340(%rbp)
	leaq	-336(%rbp), %rax
	movl	$25, %esi
	movq	%rax, %rdi
	call	fill_array
	leaq	-224(%rbp), %rax
	movl	$25, %esi
	movq	%rax, %rdi
	call	fill_array
	movl	$0, -352(%rbp)
	jmp	.L10
.L15:
	movl	$0, -348(%rbp)
	jmp	.L11
.L14:
	movl	$0, -344(%rbp)
	jmp	.L12
.L13:
	movl	-344(%rbp), %eax
	movslq	%eax, %rcx
	movl	-352(%rbp), %eax
	movslq	%eax, %rdx
	movq	%rdx, %rax
	salq	$2, %rax
	addq	%rdx, %rax
	addq	%rcx, %rax
	movl	-336(%rbp,%rax,4), %ecx
	movl	-348(%rbp), %eax
	movslq	%eax, %rsi
	movl	-344(%rbp), %eax
	movslq	%eax, %rdx
	movq	%rdx, %rax
	salq	$2, %rax
	addq	%rdx, %rax
	addq	%rsi, %rax
	movl	-224(%rbp,%rax,4), %eax
	imull	%ecx, %eax
	addl	%eax, -340(%rbp)
	addl	$1, -344(%rbp)
.L12:
	cmpl	$4, -344(%rbp)
	jle	.L13
	movl	-348(%rbp), %eax
	movslq	%eax, %rcx
	movl	-352(%rbp), %eax
	movslq	%eax, %rdx
	movq	%rdx, %rax
	salq	$2, %rax
	addq	%rdx, %rax
	leaq	(%rax,%rcx), %rdx
	movl	-340(%rbp), %eax
	movl	%eax, -112(%rbp,%rdx,4)
	movl	$0, -340(%rbp)
	addl	$1, -348(%rbp)
.L11:
	cmpl	$4, -348(%rbp)
	jle	.L14
	addl	$1, -352(%rbp)
.L10:
	cmpl	$4, -352(%rbp)
	jle	.L15
	movl	$0, %eax
	movq	-8(%rbp), %rdi
	xorq	%fs:40, %rdi
	je	.L17
	call	__stack_chk_fail
.L17:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
