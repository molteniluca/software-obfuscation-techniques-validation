	.file	"matrixMul.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB23:
	.cfi_startproc
	testl	%esi, %esi
	jne	.L2
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	leaq	20(%rdi), %rbp
	movq	%rdi, %rbx
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
.L3:
	xorl	%eax, %eax
	addq	$4, %rbx
	call	rand
	movl	%eax, -4(%rbx)
	cmpq	%rbx, %rbp
	jne	.L3
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L2:
	xorl	%eax, %eax
.L4:
	movl	%eax, (%rdi,%rax,4)
	addq	$1, %rax
	cmpq	$5, %rax
	jne	.L4
	rep ret
	.cfi_endproc
.LFE23:
	.size	fill_array, .-fill_array
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
