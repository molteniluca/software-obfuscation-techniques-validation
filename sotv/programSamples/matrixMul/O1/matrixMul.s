	.file	"matrixMul.c"
	.text
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB23:
	.cfi_startproc
	testl	%esi, %esi
	je	.L2
	movl	$0, %eax
.L3:
	movl	%eax, (%rdi,%rax,4)
	addq	$1, %rax
	cmpq	$5, %rax
	jne	.L3
	rep ret
.L2:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, %rbx
	leaq	20(%rdi), %rbp
.L5:
	movl	$0, %eax
	call	rand
	movl	%eax, (%rbx)
	addq	$4, %rbx
	cmpq	%rbp, %rbx
	jne	.L5
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE23:
	.size	fill_array, .-fill_array
	.globl	main
	.type	main, @function
main:
.LFB24:
	.cfi_startproc
	subq	$232, %rsp
	.cfi_def_cfa_offset 240
	movq	%fs:40, %rax
	movq	%rax, 216(%rsp)
	xorl	%eax, %eax
	movl	$25, %esi
	movq	%rsp, %rdi
	call	fill_array
	movl	$25, %esi
	leaq	112(%rsp), %rdi
	call	fill_array
	movq	216(%rsp), %rdx
	xorq	%fs:40, %rdx
	je	.L10
	call	__stack_chk_fail
.L10:
	movl	$0, %eax
	addq	$232, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE24:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
